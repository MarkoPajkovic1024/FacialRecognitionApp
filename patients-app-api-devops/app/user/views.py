"""
Views for the user API.
"""
from .compare import face_comparing
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view


from rest_framework.renderers import JSONRenderer


#from .compare import face_comparing
from base64 import urlsafe_b64decode, urlsafe_b64encode
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from threading import Thread


from django.conf import settings
from .mail_verify import get_email_token, send_mail,verify_token

from user.serializers import (
    EmailVerifiySerializer,
    FaceCompareTestSerializer,
    UserSerializer,
    AuthTokenSerializer,
    ChangePasswordSerializer
)


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer
    # added colorfull api views
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user

class ChangePasswordView(generics.UpdateAPIView):
    """An endpoint for changing password"""
    serializer_class = ChangePasswordSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self,queryset = None):
        return self.request.user
    def update(self,request,*args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

        return Response(response)
          


class EmailVerifyView(generics.CreateAPIView):
    serializer_class = EmailVerifiySerializer

    def create(self,request):
        email= request.data['email']
        from_Email = settings.EMAIL_FROM

        token = get_email_token(email)
        t = Thread(target=send_mail, args=(token,'Please click this verify link','Verify token',from_Email ,[email]))
        t.start()

        return Response({"email_token" :token ,"status" : True},status = status.HTTP_201_CREATED)

#check receive email_token and activate user

@api_view(['GET'])
def activate(request, email_token):  
        flag = verify_token(email_token)
        if flag :
            return Response({"message" : 'Thank you for your email confirmation. Now you can login your account.',
            "status" : True},status = status.HTTP_201_CREATED)  
        else:  
            return Response({"message" : 'Activation link is invalid!', "status" : False})  



class FaceCompareView(generics.CreateAPIView):
   
    serializer_class = FaceCompareTestSerializer
    def create(self,request):
       
        image1 = request.data['image1']
        image2 = request.data['image2']

      
        #return Response({"success" : "true"})
        cp = face_comparing(image1,image2)
       
        return Response({"T":cp},status = status.HTTP_201_CREATED)