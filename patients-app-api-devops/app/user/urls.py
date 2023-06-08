"""
URL mappings for the user API.
"""
from django.urls import path

from user import views
from .views import activate

app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('changepwd/',views.ChangePasswordView.as_view(),name = "changepwd"),
    path('emailverify/',views.EmailVerifyView.as_view(),name = "emailverify"),
    path('email/verify/<str:email_token>',activate, name = "activate"),

    path('faceCompare/',views.FaceCompareView.as_view(),name = "face_compare")
    ]
