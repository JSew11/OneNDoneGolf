from django.urls import path

from ..views import (
    SeasonViewSet,
    SeasonGolfersViewset,
    SeasonTournamentsViewSet,
)

season_list_views = SeasonViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

season_details_views = SeasonViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy',
})

season_golfers_list_views = SeasonGolfersViewset.as_view({
    'get': 'list',
})

season_golfers_detail_views = SeasonGolfersViewset.as_view({
    'get': 'retrieve',
})

season_tournaments_list_views = SeasonTournamentsViewSet.as_view({
    'get': 'list',
})

season_tournaments_detail_views = SeasonTournamentsViewSet.as_view({
    'get': 'retrieve'
})

urlpatterns = [
    path('', season_list_views, name='seasons_list'),
    path('<int:season_id>/', season_details_views, name='season_details'),
    path('<int:season_id>/golfers/', season_golfers_list_views, name='season_golfers_list'),
    path('<int:season_id>/golfers/<int:golfer_id>/', season_golfers_detail_views, name='season_golfers_details'),
    path('<int:season_id>/tournaments/', season_tournaments_list_views, name='season_tournaments_list'),
    path('<int:season_id>/tournaments/<int:tournament_id>/', season_tournaments_detail_views, name='season_tournament_details'),
]