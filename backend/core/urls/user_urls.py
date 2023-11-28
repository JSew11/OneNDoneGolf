from django.urls import path

from ..views.user_views import UserListView, UserViewSet

current_user_view = UserViewSet.as_view({
    'get': 'current_user',
})

user_viewset = UserViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
})

urlpatterns = [
    path('', UserListView.as_view(), name='users_list'),
    path('me/', current_user_view, name='current_user'),
    path('<int:user_id>/', user_viewset, name='user_details'),
]