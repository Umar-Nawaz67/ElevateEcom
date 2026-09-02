from django.contrib import admin
from django.urls import path,include
urlpatterns=[path('admin/',admin.site.urls),path('api/v1/auth/',
                                                 include('apps.accounts.urls')),
                                                 path('api/v1/services/',
                                                      include('apps.services.urls')),path('api/v1/packages/',include('apps.packages.urls')),path('api/v1/orders/',include('apps.orders.urls'))]
