from django.urls import path

from ..views import (
    SeasonViewSet,
    SeasonUsersViewset,
    SeasonGolfersViewset,
    SeasonTournamentsViewSet,
    SeasonTournamentGolferViewSet,
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

active_season_view = SeasonViewSet.as_view({
    'get': 'active_season',
})

next_tournament_view = SeasonViewSet.as_view({
    'get': 'next_tournament',
})

season_users_list_views = SeasonUsersViewset.as_view({
    'get': 'list',
    'post': 'create',
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

field_list_view = SeasonTournamentsViewSet.as_view({
    'get': 'field'
})

season_tournament_golfer_list_views = SeasonTournamentGolferViewSet.as_view({
    'get': 'list'
})

season_tournament_golfer_detail_views = SeasonTournamentGolferViewSet.as_view({
    'get': 'retrieve'
})

urlpatterns = [
    path('', season_list_views, name='seasons_list'),
    path('active/', active_season_view, name='active_season'),
    path('<int:season_id>/', season_details_views, name='season_details'),
    path('<int:season_id>/next-tournament/', next_tournament_view, name='next_tournament'),
    path('<int:season_id>/users/', season_users_list_views, name='season_users_list'),
    path('<int:season_id>/golfers/', season_golfers_list_views, name='season_golfers_list'),
    path('<int:season_id>/golfers/<int:golfer_id>/', season_golfers_detail_views, name='season_golfer_details'),
    path('<int:season_id>/tournaments/', season_tournaments_list_views, name='season_tournaments_list'),
    path('<int:season_id>/tournaments/<int:tournament_id>/', season_tournaments_detail_views, name='season_tournament_details'),
    path('<int:season_id>/tournaments/<int:tournament_id>/field/', field_list_view, name='field_list'),
    path('<int:season_id>/tournaments/<int:tournament_id>/golfers/', season_tournament_golfer_list_views, name='season_tournament_golfers_list'),
    path('<int:season_id>/tournaments/<int:tournament_id>/golfers/<int:golfer_id>/', season_tournament_golfer_detail_views, name='season_tournament_golfer_details'),
]