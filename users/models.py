from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    confirm_password = models.CharField(max_length=128)
    # photo field removed

    def __str__(self):  # Fixed method name from _str_ to __str__
        return self.username

class Morceau(models.Model):
    titre = models.CharField(max_length=100)
    artiste = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    fichier = models.FileField(upload_to='morceaux/')
    image = models.ImageField(upload_to='morceaux_images/', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.titre} - {self.artiste}"

class Playlist(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    visibilite = models.CharField(max_length=10, choices=[('publique', 'Publique'), ('privee', 'PrivĂ©e')])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nom

class MorceauPlaylist(models.Model):
    morceau = models.ForeignKey(Morceau, on_delete=models.CASCADE)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    ordre = models.PositiveIntegerField()

class Historique(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    morceau = models.ForeignKey(Morceau, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)