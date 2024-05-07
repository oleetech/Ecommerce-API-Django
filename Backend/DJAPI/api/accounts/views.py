from django.shortcuts import get_object_or_404
from rest_framework import status,permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken

# Register View
class RegisterView(APIView):
    permission_classes = [AllowAny]

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