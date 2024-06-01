from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
class profile(models.Model):
    User = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="user")
    image=models.ImageField(upload_to="images",blank=True,null=True,verbose_name="Image")
    address=models.CharField( max_length=90,blank=True,null=True,verbose_name="Address")

    def __str__(self):
        return str(self.User)

def create_profile(sender,**kwargs):
    if kwargs["created"]:
        user_profile=profile.objects.create(User=kwargs['instance'])
post_save.connect(create_profile,sender=User)











# Create your models here.
