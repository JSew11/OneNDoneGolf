from django.urls import path, include

app_name = 'golf_pickem'

urlpatterns = [
    path('picks/', include('golf_pickem.urls.pick_urls')),
]