from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=20,unique=True)
    password = models.CharField(max_length=20)

class Share(models.Model):
    shareTo = models.ForeignKey(User,on_delete=models.CASCADE,related_name="shareTo")
    sharedBy  = models.ForeignKey(User,on_delete=models.CASCADE,related_name="sharedBy")
    imagelink = models.CharField(max_length=100)