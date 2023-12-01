from django.contrib import admin

from .models import (
    Season,
    Tournament,
    TournamentSeason,
    Golfer,
    GolferSeason,
    TournamentGolfer,
    Pick
)

# Register your models here.
admin.site.register(Golfer)
admin.site.register(Tournament)
admin.site.register(Pick)