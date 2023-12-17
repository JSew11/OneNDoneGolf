from django.urls import path

from ..views import SeasonViewSet

season_list_views = SeasonViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

season_details_views = SeasonViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy',
})

urlpatterns = [
    path('', season_list_views, name='seasons_list'),
    path('<int:season_id>/', season_details_views, name='season_details'),
]