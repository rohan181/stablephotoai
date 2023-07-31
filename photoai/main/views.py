from django.shortcuts import render
from rest_framework.decorators import api_view
# Create your views here.
from django.contrib.auth.decorators import login_required
import requests
import json
from .models import UserItem, Userprofile,Photo
from django.http import HttpResponse
from rest_framework.response import Response
from django.shortcuts import render, redirect
from .forms import PhotoUploadForm
from io import BytesIO
from django.http import JsonResponse
from PIL import Image, ImageOps
import tempfile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import get_object_or_404
import uuid
import requests
import json



@login_required
def index(request):
    user = request.user
    user_item =  Userprofile.objects.filter(user=user).first()  # Retrieve the prfile object related to the current user
    context = {
        'user': user,
        'modelid': user_item.modelid if user_item else None,
        'image': user_item.image if user_item else None,
    }


    return render(request, 'form.html',context)


@login_required
def photoview(request):
    user = request.user
    user_item = Userprofile.objects.filter(user=user).order_by('-id').first() # Retrieve the UserItem object related to the current user
    context = {
        'user': user,
        'modelid': user_item.modelid if user_item else None,
        'image': user_item.image if user_item else None,
    }


    return render(request, 'a.html',context)


@api_view(['POST'])
def create_user_item(request):
    data = request.data
    user = request.user
    modelid = data.get('modelid')
    image = data.get('image')
    
    # Create the UserItem object
    user_item = UserItem.objects.create(user=user, modelid=modelid, image=image)

    # Return a success response
    return Response({'message': 'success'})



@login_required
def image(request):
 

            url = "https://stablediffusionapi.com/api/v4/dreambooth"

            payload = json.dumps({
            "key": "qcAvUL9oteJVVsX8I8P2986GxkoSqGvTmejDQHpdMJChUKrVTnXJrcYVn4Rp",
    "model_id": "H6T5co3VwC0dJeBuLpXsWDhSG",
      
    
     "prompt": "abir_rohan1811 person,ed:1.15),shiny glitter party dress,whole full body,detailed high end fashion,formal dress,natural light, sharp, detailed face, magazine, photo, canon, nikon, focus, award winning photo,reminiscent of the works of Steve McCurry, 35mm, F/2.8, insanely detailed and intricate, character, hypermaximalist, elegant, ornate, hyper realistic, super detailed, trending on flickr, portrait photo,masterpiece,beach background,full body, best quality, high resolution, 8K , HDR, bloom, sun light, raytracing , detailed shadows, intricate tree shadow, bokeh, depth of field, film photography, film grain, glare, (wind:0.8), detailed hair, beautiful face, beautiful man, ultra detailed eyes, cinematic lighting, (hyperdetailed:1.15), outdoors,happy face,,ultra-realistic,clear facial features,natural features,captured with a phase one 35mm lens,f/ 3.2,agfa vista film ,film grain light,global illumination,intricate detail,wide shot,--upbeta --ar 4:5 --s 750 --q 2", 
  "negative_prompt": "(worst quality:2.00), (low quality:2.00), (normal quality:2.00), low-res,deformed face,(deformed iris, deformed pupils, semi-realistic, CGI, 3D, render, sketch, cartoon, drawing, anime:1.4), text, close up, cropped, out of frame, worst quality, low quality, JPEG artifacts, ugly, duplicate, morbid, mutilated, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, blurry, dehydrated, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, gross proportions, malformed limbs, missing arms, missing legs, extra arms, extra legs, fused fingers, too many fingers, long neck,blurry background,dslr,portrait,dark face,dark eye,make up,fat face, easynegative,flat face,red skin,bad skin, wrinkles, pustules",
            "width": "512",
            "height": "512",
            "samples": "1",
            "num_inference_steps": "30",
            "safety_checker": "no",
            "enhance_prompt": "yes",
            "seed": None,
            "guidance_scale": 7.5,
            "multi_lingual": "no",
            "panorama": "no",
            "self_attention": "no",
            "upscale": "no",
            "embeddings_model": None,
            "lora_model": None,
            "scheduler": "UniPCMultistepScheduler",
            "webhook": None,
            "track_id": None
            })

            headers = {
            'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            print(response.text)
            return render(request, 'a.html')



def retrieve_user_items(request):
    user = request.user
    user_items = UserItem.objects.filter(user=user).order_by('-id')   
    data = {
        'user_items': list(user_items.values())
    }



    user_items = Photo.objects.filter(user=request.user).order_by('-id')
    image_urls = [item.image.url for item in user_items]

# Convert image URLs to the desired format
    formatted_images = []
    for url in image_urls:
        formatted_images.append(url)   


    print(formatted_images)
    

# If you want to add the "images" key to the output, you can create a dictionary
   


    return JsonResponse(data)




def resize_image(image, username, max_size=(512, 512)):
    # Open the image using PIL to get an Image object that supports getexif()
    img = Image.open(image)

    # Rotate the image according to the Exif orientation tag
    img = ImageOps.exif_transpose(img)

    # Calculate the new size while maintaining the aspect ratio
    width, height = img.size
    max_dim = max(width, height)

    # Calculate the new dimensions
    new_width = int(max_size[0] * width / max_dim)
    new_height = int(max_size[1] * height / max_dim)

    # Resize the image without rotating
    img = img.resize((new_width, new_height), Image.LANCZOS)

    # Create a new BytesIO object to store the resized image data
    output_io = BytesIO()

    # Save the resized image to the BytesIO object in PNG format
    img.save(output_io, format='png')

    # Generate a unique identifier
    unique_id = uuid.uuid4().hex

    # Concatenate the username and the unique identifier to form the new filename
    new_filename = f"{username}_{unique_id}.png"

    # Create an InMemoryUploadedFile from the BytesIO data with the new filename
    image_file = InMemoryUploadedFile(
        output_io, None, new_filename, 'image/png', output_io.getbuffer().nbytes, None
    )

    return image_file



def upload_photos(request):
    if request.method == 'POST':
        images = request.FILES.getlist('images')
        selected_gender = request.POST.get('gender') 
        username = request.user.username

        for image in images:
            # Resize the image before creating the Photo object
            resized_image = resize_image(image, username)

            # Create a Photo object without saving it to the database yet
            photo = Photo(
                user=request.user,
                image=resized_image,
            )

            # Save the Photo object to the database
            photo.save()

        user_items = Photo.objects.filter(user=request.user).order_by('-id')
        image_urls = [item.image.url for item in user_items]

# Convert image URLs to the desired format
        formatted_images = []
        for url in image_urls:
            formatted_images.append(url)    


        

        url = "https://stablediffusionapi.com/api/v3/fine_tune_v2"

        payload = json.dumps({
        "key": "KhwsDivKGA4dhHDlbZQcVeGojvjTjIMNCebIV6iImfvgWPHpyW0E8ZWAjK33",
        "instance_prompt": "photo of abir_rohan1811",
        "class_prompt": "photo of person",
        "base_model_id": "realistic-vision-v13",
         "images": formatted_images,
        "seed": "0",
  "training_type": selected_gender ,
  "learning_rate_unet": "2e-6",
  "steps_unet": "1500",
  "learning_rate_text_encoder": "1e-6",
  "steps_text_encoder": "350",
  "webhook": ""
})

        headers = {
        'Content-Type': 'application/json'
        }

        
        response = requests.request("POST", url, headers=headers, data=payload)
        response_dict = json.loads(response.text)
        modelid=response_dict["model_id"]

        
       
        
        user_item = get_object_or_404(Userprofile, user=request.user)
        user_item.modelid = modelid
      
# Update the modelid attribute
        

        user_item.save()



    return render(request, 'upload_photos.html')
   

  

    















