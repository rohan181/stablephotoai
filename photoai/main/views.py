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

from django.http import JsonResponse

@login_required
def index(request):
    user = request.user
    user_item =  Userprofile.objects.filter(user=user).first()  # Retrieve the UserItem object related to the current user
    context = {
        'user': user,
        'modelid': user_item.modelid if user_item else None,
        'image': user_item.image if user_item else None,
    }


    return render(request, 'form.html',context)


@login_required
def photoview(request):
    user = request.user
    user_item = UserItem.objects.filter(user=user).order_by('-id').first() # Retrieve the UserItem object related to the current user
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
    return JsonResponse(data)



def upload_photos(request):
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user  # Assuming you have authentication in place
            image_count = Photo.objects.filter(user=user).count()
            if image_count < 20:
                form.instance.user = user
                form.save()
            else:
                # Display an error message or handle the limit of 20 photos per user.
                pass

    else:
        form = PhotoUploadForm()

    return render(request, 'upload_photos.html', {'form': form})