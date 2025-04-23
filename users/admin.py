from django.contrib import admin
from .models import User, Morceau, Playlist, MorceauPlaylist

# Register your models here.
admin.site.register(User)
admin.site.register(Morceau)
admin.site.register(Playlist)
admin.site.register(MorceauPlaylist)
admin.site.site_header = "Musique Project Admin"
admin.site.index_title = "Welcome to the Musique Project Admin Portal" 
