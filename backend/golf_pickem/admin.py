from django.contrib import admin

from .models.golfer import Golfer
from .models.tournament import Tournament

# Register your models here.
admin.site.register(Golfer)
admin.site.register(Tournament)