from django.urls import path, include

from ..views.auth_views import (
    LoginUserView,
    LogoutUserView,
    UserRegistrationViewSet,
    RefreshTokenView
)

app_name = 'core'

urlpatterns = [
    path('login/', LoginUserView.as_view(), name='login'),
    path('login/refresh/', RefreshTokenView.as_view(), name='token_refresh'),
    path('register/', UserRegistrationViewSet.as_view(), name='register'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('users/', include('core.urls.user_urls')),
]