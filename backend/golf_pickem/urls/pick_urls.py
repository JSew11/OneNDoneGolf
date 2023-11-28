from django.urls import path

from ..views.pick_views import PickViewSet

pick_list_view = PickViewSet.as_view({
    'get': 'list',
})

urlpatterns = [
    path('', pick_list_view, name='picks_list'),
]