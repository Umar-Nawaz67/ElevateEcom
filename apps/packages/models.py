from django.db import models
from apps.services.models import Service
class Package(models.Model):
 service=models.ForeignKey(Service,on_delete=models.CASCADE,related_name='packages');
 name=models.CharField(max_length=160);
 description=models.TextField(blank=True); 
 price=models.DecimalField(max_digits=12,decimal_places=2); 
 duration_minutes=models.PositiveIntegerField(default=60); 
 image=models.ImageField(upload_to='packages/',blank=True,null=True); 
 is_active=models.BooleanField(default=True)
 created_at = models.DateTimeField(auto_now_add=True)
 updated_at = models.DateTimeField(auto_now=True)

 def __str__(self):
        return f"{self.service.name} - {self.name}"
