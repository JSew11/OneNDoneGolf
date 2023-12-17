from django.urls import path

from ..views import PickViewSet

pick_list_views = PickViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

pick_details_views = PickViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy',
})

urlpatterns = [
    path('', pick_list_views, name='picks_list'),
    path('<int:pick_id>/', pick_details_views, name='pick_details'),
]