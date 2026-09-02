from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import CompleteRegistrationView, DeleteAccountView, FirebaseAuthView, RegisterView,LoginView,MeView,GoogleView,AppleView,FacebookView
urlpatterns=[path('register/',RegisterView.as_view()),
             path('login/',LoginView.as_view()),
             path('token/refresh/',TokenRefreshView.as_view()),
             path('me/',MeView.as_view()),path('social/google/',GoogleView.as_view()),
             path('social/apple/',AppleView.as_view()),path('social/facebook/',FacebookView.as_view()),
             path(
                         "firebase/",
                         FirebaseAuthView.as_view(),
                         name="firebase-auth",
                     ), 
             path(
        "complete-registration/",
        CompleteRegistrationView.as_view(),
        name="complete-registration",
    ),
             path(
        "delete-account/",
        DeleteAccountView.as_view(),
        name="delete-account",
    ),
             ]
         