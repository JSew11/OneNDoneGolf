from django.urls import path

from ..views.pick_views import PickViewSet

pick_list_view = PickViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

pick_details_view = PickViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy',
})

urlpatterns = [
    path('', pick_list_view, name='picks_list'),
    path('<int:pick_id>/', pick_details_view, name='pick_details'),
]