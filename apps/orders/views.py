from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer
class OrderViewSet(viewsets.ModelViewSet):
 serializer_class=OrderSerializer; permission_classes=[IsAuthenticated]
 def get_queryset(self): return Order.objects.select_related('package','customer') if self.request.user.is_staff else Order.objects.filter(customer=self.request.user)
 def partial_update(self,request,*a,**k):
  if not request.user.is_staff:return Response({'detail':'Admin only'},status=403)
  o=self.get_object(); new=request.data.get('status'); allowed={'PENDING':['ACCEPTED','CANCELLED'],'ACCEPTED':['IN_PROGRESS','CANCELLED'],'IN_PROGRESS':['COMPLETED'],'COMPLETED':[],'CANCELLED':[]}
  if new not in allowed[o.status]:return Response({'detail':'Invalid status transition'},status=400)
  o.status=new;o.save(update_fields=['status','updated_at']);return Response(self.get_serializer(o).data)
