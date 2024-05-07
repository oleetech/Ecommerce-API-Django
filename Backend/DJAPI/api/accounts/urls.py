from django.urls import path
from .views import RegisterView, LogoutView,ProfileUpdateView,GetAllUsersView,GetUserView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('wp/v2/users/register/', RegisterView.as_view(), name='register'),
    path('wp/v2/users/logout/', LogoutView.as_view(), name='logout'),
    path('wp/v2/users/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('wp/v2/users/<int:id>/', ProfileUpdateView.as_view(), name='profile-update'),
    path('wp/v2/users/', GetAllUsersView.as_view(), name='get-all-users'),
    path('wp/v2/users/<int:pk>/', GetUserView.as_view(), name='get-user'),

    # path('wp/v2/users/update-profile/', ProfileUpdateView.as_view(), name='update-profile'),

    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]