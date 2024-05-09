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
    """
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, type=openapi.TYPE_INTEGER, description="User ID")
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'mobile_number': openapi.Schema(type=openapi.TYPE_STRING),
                # Add other properties as needed for profile update
            }
        ),
        responses={
            200: 'Profile updated successfully',
            400: 'Bad Request. Invalid input. Check the error message for details.',
            403: 'Forbidden. You are not allowed to update this profile.'
        },
        operation_description="Update user profile details."
    )
    def put(self, request, id, *args, **kwargs):
        """
        Update user profile details.

        **Path Parameters**:
        - `id` (integer): User ID.

        **Example Request**:
        ```json
        {
            "mobile_number": "1234567890"
        }
        ```

        **Example Response**:
        - 200 OK: Profile updated successfully.
          ```json
          {
              "message": "Profile updated successfully"
          }
          ```

        - 400 Bad Request: Invalid input.
          ```json
          {
              "error": "Invalid input. Check the error message for details."
          }
          ```

        - 403 Forbidden: You are not allowed to update this profile.
          ```json
          {
              "detail": "আপনার এই প্রোফাইল আপডেট করার অনুমতি নেই।"
          }
          ```
        """
        user = self.get_object(id)
        if request.user.id != id and not request.user.is_superuser:
            return Response({'detail': 'আপনার এই প্রোফাইল আপডেট করার অনুমতি নেই।'}, status=status.HTTP_403_FORBIDDEN)
        serializer = ProfileUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profile updated successfully'})
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

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL),
            }
        ),
        responses={
            200: 'Password reset link sent successfully',
            404: 'User not found'
        },
        operation_description="Send a password reset link to the user's email.",
    )
    def post(self, request):
        """
        Send a password reset link to the user's email.

        **Example Request**:
        ```json
        {
            "email": "user@example.com"
        }
        ```

        **Example Response**:
        - 200 OK: Password reset link sent successfully.
          ```json
          {
              "message": "Password reset link sent successfully"
          }
          ```

        - 404 Not Found: User not found.
          ```json
          {
              "error": "User not found"
          }
          ```
        """
        email = request.data.get('email')
        user = UserModel.objects.filter(email=email).first()
        if user:
            token = default_token_generator.make_token(user)
            # Get the current site domain
            current_site = get_current_site(request)
            domain = current_site.domain
            # Construct the reset link
            reset_link = f"http://{domain}/custom/v1/reset-password/{token}/"
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

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'new_password'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL),
                'new_password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD),
            }
        ),
        responses={
            200: 'Password reset successfully',
            400: 'Bad Request. Invalid token.',
            404: 'User not found',
        },
        operation_description="Reset the user's password using the provided token.",
    )
    def post(self, request, token):
        """
        Reset the user's password using the provided token.

        **Example Request**:
        ```json
        {
            "email": "user@example.com",
            "new_password": "new_password_here"
        }
        ```

        **Example Response**:
        - 200 OK: Password reset successfully.
          ```json
          {
              "message": "Password reset successfully"
          }
          ```

        - 400 Bad Request: Invalid token.
          ```json
          {
              "error": "Invalid token"
          }
          ```

        - 404 Not Found: User not found.
          ```json
          {
              "error": "User not found"
          }
          ```
        """
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