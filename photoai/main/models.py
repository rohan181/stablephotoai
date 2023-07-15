from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class UserItem(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
   

    modelid = models.CharField(max_length=500,blank=True,null=True)
    image = models.CharField(max_length=500,blank=True,null=True)
    