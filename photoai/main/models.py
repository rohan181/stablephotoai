from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Userprofile(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
   

    modelid = models.CharField(max_length=500,blank=True,null=True)
    image = models.CharField(max_length=500,blank=True,null=True)

class UserItem(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
   
    userprofile = models.ForeignKey(Userprofile, on_delete=models.CASCADE,null=True,related_name='userprofile')
    modelid = models.CharField(max_length=500,blank=True,null=True)
    image = models.CharField(max_length=500,blank=True,null=True)



class Photo(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s photo at {self.uploaded_at}"    



