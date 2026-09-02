from django.conf import settings
from django.db import models
from apps.packages.models import Package
class Order(models.Model):
 class Status(models.TextChoices): PENDING='PENDING'; ACCEPTED='ACCEPTED'; IN_PROGRESS='IN_PROGRESS'; COMPLETED='COMPLETED'; CANCELLED='CANCELLED'
 order_number=models.CharField(max_length=30,unique=True,editable=False); customer=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name='orders'); package=models.ForeignKey(Package,on_delete=models.PROTECT); price=models.DecimalField(max_digits=12,decimal_places=2); customer_name=models.CharField(max_length=160); phone=models.CharField(max_length=30); address=models.TextField(); booking_date=models.DateField(); booking_time=models.TimeField(); notes=models.TextField(blank=True); status=models.CharField(max_length=20,choices=Status.choices,default='PENDING'); created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
 def save(self,*a,**k):
  if not self.order_number:
   from django.utils.crypto import get_random_string
   self.order_number='ELV-'+get_random_string(8,'0123456789')
  super().save(*a,**k)
