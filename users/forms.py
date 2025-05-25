from django import forms
from .models import User, Morceau, Playlist

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']
        widgets = {
            'password': forms.PasswordInput(),
            'confirm_password': forms.PasswordInput(),
        }

class MorceauForm(forms.ModelForm):
    class Meta:
        model = Morceau
        fields = ['titre', 'artiste', 'genre', 'fichier'] 

class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['nom', 'description', 'visibilite']