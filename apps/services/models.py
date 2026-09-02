from django.db import models
class Service(models.Model):
 name=models.CharField(max_length=120); description=models.TextField(blank=True); 
 image=models.ImageField(upload_to='services/',blank=True,null=True); 
 is_active=models.BooleanField(default=True); 
 sort_order=models.PositiveIntegerField(default=0)
 created_at = models.DateTimeField(auto_now_add=True)
 updated_at = models.DateTimeField(auto_now=True)

 class Meta:
        ordering = ["sort_order", "name"]
 def __str__(self): return self.name
