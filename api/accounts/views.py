from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework import status,permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# Register View
class RegisterView(APIView):
   

    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'username', 'password'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL),
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD),
            }
        ),
        responses={
            201: 'User registration successful',
            400: 'Bad Request. Invalid input. Check the error message for details.',
        },
        operation_description="Register a new user.",
    )
    def post(self, request):
       
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Logout View
class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        
from .serializers import ProfileUpdateSerializer
# class ProfileUpdateView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get_object(self):
#         return self.request.user

#     def put(self, request, *args, **kwargs):
#         user = self.get_object()
#         serializer = ProfileUpdateSerializer(user, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        

from django.contrib.auth import get_user_model
User = get_user_model()
class ProfileUpdateView(APIView):
    """
    Profile Update API

    This API endpoint enables authenticated users to update their user profile. It supports updating profile details such as mobile number and profile picture.

    ## HTTP Method: PUT

    Use the PUT method to submit profile updates.

    ## URL Parameters:

    - **id** (integer): The ID of the user whose profile is to be updated.

    ## Permissions:

    - **Authenticated Users**: Only authenticated users can access this endpoint.
    - **Superuser Privileges**: A superuser can update any user's profile.
    - **User-Specific Permission**: Users can only update their own profile unless they have superuser privileges.

    ## Request Format:

    Send a multipart form data request with the necessary profile fields that need to be updated.

    ## Headers:

    - **Authorization**: Include a valid bearer token to authenticate the request.

        Example: 'Authorization: Bearer <your_access_token>'

    ## Body:

    - **mobileNo**: The new mobile number.
    - **profile_pic**: A file upload field for the profile picture.

    ## Example Request:

    ```bash
    PUT http://example.com/wp-json/wp/v2/users/123/
    Headers:
        Authorization: Bearer <your_access_token>
    Body:
        mobileNo: 017xxxxxxxx
        profile_pic: (attach image file)
    ```

    ## Responses:

    - **200 OK**: The request was successful, and the profile was updated.
    - **400 Bad Request**: The request was malformed. Check the error message for more details.
    - **403 Forbidden**: You do not have permission to update this profile.
    - **404 Not Found**: No user found with the provided ID.

    ## Error Handling:

    Responses will include a JSON object with error details should there be an issue with the request.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
  
        user = get_object_or_404(User, pk=pk)
        self.check_object_permissions(self.request, user)
        return user

    def put(self, request, id, *args, **kwargs):

        user = self.get_object(id)
        if request.user.id != id and not request.user.is_superuser:
            return Response({'detail': 'আপনার এই প্রোফাইল আপডেট করার অনুমতি নেই।'}, status=status.HTTP_403_FORBIDDEN)
        serializer = ProfileUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
from .serializers import UserSerializer
class GetAllUsersView(APIView):
    permission_classes = [permissions.AllowAny]  

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)    
    
class GetUserView(APIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny] 

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)    
    

#   _____                _     _____                                    _ 
#  |  __ \              | |   |  __ \                                  | |
#  | |__) |___  ___  ___| |_  | |__) |_ _ ___ _____      _____  _ __ __| |
#  |  _  // _ \/ __|/ _ \ __| |  ___/ _` / __/ __\ \ /\ / / _ \| '__/ _` |
#  | | \ \  __/\__ \  __/ |_  | |  | (_| \__ \__ \\ V  V / (_) | | | (_| |
#  |_|  \_\___||___/\___|\__| |_|   \__,_|___/___/ \_/\_/ \___/|_|  \__,_|
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

def generate_reset_token(user):
    return default_token_generator.make_token(user)

from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
UserModel = get_user_model()

class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        user = UserModel.objects.filter(email=email).first()
        if user:
            token = default_token_generator.make_token(user)
            # Get the current site domain
            current_site = get_current_site(request)
            domain = current_site.domain
            # Construct the reset link
            reset_link = f"http://{domain}/wp-json/wp/v2/users/reset-password/{token}/"
            send_mail(
                'Password Reset Request',
                f'Use the following link to reset your password: {reset_link}',
                'admin@kreatech.ca',  
                [email],
                fail_silently=False,
            )
            return Response({'message': 'Password reset link sent successfully'}, status=status.HTTP_200_OK)
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, token):
        new_password = request.data.get('new_password')
        email = request.data.get('email')  
        user = UserModel.objects.filter(email=email).first()  
        if not user:
            raise Http404("User does not exist")
        
        if default_token_generator.check_token(user, token):
            # Reset the user's password
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)                                                                           