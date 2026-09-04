from django.contrib.auth.models import AbstractUser
from django.db import models
class User(AbstractUser):
 class Roles(models.TextChoices): CUSTOMER='CUSTOMER','Customer'; STAFF = 'STAFF', 'Staff';ADMIN='ADMIN','Admin'
 email=models.EmailField(blank=True);
 phone=models.CharField(max_length=30,blank=True); 
 
 role=models.CharField(max_length=20,choices=Roles.choices,default=Roles.CUSTOMER)
 firebase_uid = models.CharField(
         max_length=255,
         unique=True,
         null=True,
         blank=True,
     )
 
 firebase_provider = models.CharField(
         max_length=50,
         null=True,
         blank=True,
     )
 registration_completed = models.BooleanField(
    default=False
) 
class SocialAccount(models.Model):
 user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='social_accounts'); 
 provider=models.CharField(max_length=20); 
 provider_user_id=models.CharField(max_length=255);
 email=models.EmailField(blank=True)
 class Meta: constraints=[models.UniqueConstraint(fields=['provider','provider_user_id'],name='unique_social_account')]
