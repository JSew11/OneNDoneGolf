from django.urls import path

from ..views.pick_views import PickViewSet

pick_list_view = PickViewSet.as_view({
    'get': 'list',
})

pick_details_view = PickViewSet.as_view({
    'get': 'retrieve',
})

urlpatterns = [
    path('', pick_list_view, name='picks_list'),
    path('<int:pick_id>/', pick_details_view, name='pick_details'),
]