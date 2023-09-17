from django.contrib import admin

from .models.golfer import Golfer
from .models.tournament import Tournament
from .models.tournament_golfer import TournamentGolfer
from .models.pick import Pick

# Register your models here.
admin.site.register(Golfer)
admin.site.register(Tournament)
admin.site.register(TournamentGolfer)
admin.site.register(Pick)