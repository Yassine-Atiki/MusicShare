from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from .models import User, Morceau, Playlist, MorceauPlaylist, Historique
from .forms import UserForm, MorceauForm, PlaylistForm

# Home view
class home(View):
    def get(self, request):
        return render(request, 'home.html')

# Registration view
class registre(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return redirect('users:register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Ce nom d'utilisateur est déjà pris.")
            return redirect('users:register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Cet email est déjà utilisé.")
            return redirect('users:register')
        
        user = User(username=username, email=email, password=password, confirm_password=confirm_password)
        user.save()
        
        request.session['user_id'] = user.id
        messages.success(request, "Inscription réussie! Bienvenue sur notre plateforme.")
        return redirect('users:login')

# Login view
class login(View):
    def get(self, request):
        return render(request, 'login.html')
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username, password=password)
            request.session['user_id'] = user.id
            return redirect('users:dashboard')
        except User.DoesNotExist:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
            return redirect('users:login')

# Dashboard view
class dashboard(View):
    def get(self, request):
        if 'user_id' not in request.session:
            return redirect('users:login')
        
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        
        recent_tracks = Morceau.objects.filter(user=user).order_by('-date')[:8]
        playlists = Playlist.objects.filter(user=user)[:4]
        
        context = {
            'user': user,
            'recent_tracks': recent_tracks,
            'playlists': playlists
        }
        
        return render(request, 'dashboard.html', context)

# Logout view
class logout(View):
    def get(self, request):
        if 'user_id' in request.session:
            del request.session['user_id']
        return redirect('users:home')

# Music upload view
class upload_music(View):
    def get(self, request):
        if 'user_id' not in request.session:
            return redirect('users:login')
        
        # Get the username from the database using the user_id in session
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        username = user.username
        
        return render(request, 'upload_music.html', {'username': username})
    
    def post(self, request):
        if 'user_id' not in request.session:
            return redirect('users:login')
        
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        
        # Get form data with validation
        titre = request.POST.get('titre', '').strip()
        if not titre:
            messages.error(request, "Le titre du morceau est obligatoire.")
            return redirect('users:upload_music')
            
        artiste = request.POST.get('artiste', '').strip()
        if not artiste:
            messages.error(request, "Le nom de l'artiste est obligatoire.")
            return redirect('users:upload_music')
            
        genre = request.POST.get('genre', 'Autre')
        
        # Check if file is provided
        if 'fichier' not in request.FILES:
            messages.error(request, "Le fichier audio est obligatoire.")
            return redirect('users:upload_music')
            
        fichier = request.FILES.get('fichier')
        
        # Create the track
        morceau = Morceau(
            titre=titre,
            artiste=artiste,
            genre=genre,
            fichier=fichier,
            user=user
        )
        
        # Add image if provided
        if 'image' in request.FILES:
            morceau.image = request.FILES.get('image')
        
        morceau.save()
        
        messages.success(request, "Morceau uploadé avec succès!")
        return redirect('users:dashboard')

# Track detail view
class track_detail(View):
    def get(self, request, track_id):
        if 'user_id' not in request.session:
            return redirect('users:login')
        
        track = get_object_or_404(Morceau, id=track_id)
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        
        # Add to history
        Historique.objects.create(user=user, morceau=track)
        
        user_playlists = Playlist.objects.filter(user=user)
        
        context = {
            'track': track,
            'user': user,
            'playlists': user_playlists
        }
        
        return render(request, 'track_detail.html', context)

# Play track view
class play_track(View):
    def get(self, request, track_id):
        if 'user_id' not in request.session:
            return JsonResponse({'error': 'User not logged in'}, status=401)
        
        track = get_object_or_404(Morceau, id=track_id)
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        
        # Add to history
        Historique.objects.create(user=user, morceau=track)
        
        # Return the file URL and image URL if available
        response_data = {
            'titre': track.titre,
            'artiste': track.artiste,
            'file_url': track.fichier.url,
        }
        
        if track.image:
            response_data['image_url'] = track.image.url
        
        return JsonResponse(response_data)

# Playlists view
class playlists(View):
    def get(self, request):
        if 'user_id' not in request.session:
            return redirect('users:login')
        
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        
        playlists = Playlist.objects.filter(user=user)
        
        context = {
            'user': user,
            'playlists': playlists
        }
        
        return render(request, 'playlists.html', context)

# Create playlist view
class create_playlist(View):
    def get(self, request):
        if 'user_id' not in request.session:
            return redirect('users:login')
        
        # Get the username from the database using the user_id in session
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        username = user.username
        
        return render(request, 'create_playlist.html', {'username': username})
    
    def post(self, request):
        if 'user_id' not in request.session:
            return redirect('users:login')
        
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        
        nom = request.POST.get('nom')
        description = request.POST.get('description', '')
        visibilite = request.POST.get('visibilite')
        
        # Create the new playlist
        playlist = Playlist(
            nom=nom,
            description=description,
            visibilite=visibilite,
            user=user
        )
        playlist.save()
        
        messages.success(request, "Playlist créée avec succès!")
        return redirect('users:playlist_detail', playlist_id=playlist.id)

# Playlist detail view
class playlist_detail(View):
    def get(self, request, playlist_id):
        if 'user_id' not in request.session:
            return redirect('users:login')
        
        playlist = get_object_or_404(Playlist, id=playlist_id)
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        
        # Check if the user owns the playlist or if it's public
        if playlist.user.id != user_id and playlist.visibilite != 'publique':
            messages.error(request, "Vous n'avez pas accès à cette playlist.")
            return redirect('users:playlists')
        
        # Get tracks in the playlist
        playlist_tracks = MorceauPlaylist.objects.filter(playlist=playlist).order_by('ordre')
        
        context = {
            'user': user,
            'playlist': playlist,
            'playlist_tracks': playlist_tracks
        }
        
        return render(request, 'playlist_detail.html', context)

# Add to playlist view
class add_to_playlist(View):
    def post(self, request, playlist_id, track_id):
        if 'user_id' not in request.session:
            return JsonResponse({'error': 'User not logged in'}, status=401)
        
        user_id = request.session['user_id']
        playlist = get_object_or_404(Playlist, id=playlist_id)
        track = get_object_or_404(Morceau, id=track_id)
        
        # Check if user owns the playlist
        if playlist.user.id != user_id:
            return JsonResponse({'error': 'Not authorized'}, status=403)
        
        # Check if track is already in playlist
        if MorceauPlaylist.objects.filter(playlist=playlist, morceau=track).exists():
            return JsonResponse({'error': 'Track already in playlist'}, status=400)
        
        # Get the next order number
        next_order = MorceauPlaylist.objects.filter(playlist=playlist).count() + 1
        
        # Add track to playlist
        MorceauPlaylist.objects.create(
            playlist=playlist,
            morceau=track,
            ordre=next_order
        )
        
        return JsonResponse({'success': True})

# Remove from playlist view
class remove_from_playlist(View):
    def post(self, request, playlist_id, track_id):
        if 'user_id' not in request.session:
            return JsonResponse({'error': 'User not logged in'}, status=401)
        
        user_id = request.session['user_id']
        playlist = get_object_or_404(Playlist, id=playlist_id)
        track = get_object_or_404(Morceau, id=track_id)
        
        # Check if user owns the playlist
        if playlist.user.id != user_id:
            return JsonResponse({'error': 'Not authorized'}, status=403)
        
        # Remove track from playlist
        MorceauPlaylist.objects.filter(playlist=playlist, morceau=track).delete()
        
        # Reorder remaining tracks
        remaining_tracks = MorceauPlaylist.objects.filter(playlist=playlist).order_by('ordre')
        for i, item in enumerate(remaining_tracks):
            item.ordre = i + 1
            item.save()
        
        return JsonResponse({'success': True})

# User profile view
class profile(View):
    def get(self, request):
        if 'user_id' not in request.session:
            return redirect('users:login')
        
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        
        # Get user's tracks
        uploaded_tracks = Morceau.objects.filter(user=user).order_by('-date')
        
        # Get user's playlists
        playlists = Playlist.objects.filter(user=user)
        
        # Get user's listening history
        history = Historique.objects.filter(user=user).order_by('-date')
        
        # Count statistics
        uploaded_tracks_count = uploaded_tracks.count()
        playlists_count = playlists.count()
        history_count = history.count()
        
        context = {
            'user': user,
            'uploaded_tracks': uploaded_tracks,
            'playlists': playlists,
            'history': history,
            'uploaded_tracks_count': uploaded_tracks_count,
            'playlists_count': playlists_count,
            'history_count': history_count
        }
        
        return render(request, 'profile.html', context)

# Edit profile view
class edit_profile(View):
    def get(self, request):
        if 'user_id' not in request.session:
            return redirect('users:login')
        
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        
        context = {
            'user': user
        }
        
        return render(request, 'edit_profile.html', context)
    
    def post(self, request):
        if 'user_id' not in request.session:
            return redirect('users:login')
        
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        
        username = request.POST.get('username')
        email = request.POST.get('email')
        
        # Check if username is taken by another user
        if User.objects.filter(username=username).exclude(id=user_id).exists():
            messages.error(request, "Ce nom d'utilisateur est déjà pris.")
            return redirect('users:edit_profile')
        
        # Check if email is taken by another user
        if User.objects.filter(email=email).exclude(id=user_id).exists():
            messages.error(request, "Cet email est déjà utilisé.")
            return redirect('users:edit_profile')
        
        user.username = username
        user.email = email
        
        # Update password if provided
        password = request.POST.get('password')
        if password:
            confirm_password = request.POST.get('confirm_password')
            if password != confirm_password:
                messages.error(request, "Les mots de passe ne correspondent pas.")
                return redirect('users:edit_profile')
            user.password = password
            user.confirm_password = confirm_password
        
        # Update profile photo if provided
        if 'photo' in request.FILES:
            user.photo = request.FILES['photo']
        
        user.save()
        
        messages.success(request, "Profil mis à jour avec succès!")
        return redirect('users:profile')

# History view
class history(View):
    def get(self, request):
        if 'user_id' not in request.session:
            return redirect('users:login')
        
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        
        # Get user's listening history
        history = Historique.objects.filter(user=user).order_by('-date')
        
        context = {
            'user': user,
            'history': history
        }
        
        return render(request, 'history.html', context)


class delete_account(View):
    def post(self, request):
        if 'user_id' not in request.session:
            return redirect('users:login')
        
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        
        # Verify password before deletion
        password = request.POST.get('password')
        if password != user.password:  # Note: In a real app, you should use proper password hashing
            messages.error(request, "Mot de passe incorrect. Suppression annulée.")
            return redirect('users:edit_profile')
        
        # Delete all related data
        # This will cascade to delete all related records due to on_delete=models.CASCADE
        user.delete()
        
        # Clear session
        if 'user_id' in request.session:
            del request.session['user_id']
        
        messages.success(request, "Votre compte a été supprimé avec succès.")
        return redirect('users:home')

# Edit playlist view
class edit_playlist(View):
    def get(self, request, playlist_id):
        if 'user_id' not in request.session:
            return redirect('users:login')
        
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        username = user.username
        
        playlist = get_object_or_404(Playlist, id=playlist_id)
        
        # Check if user owns the playlist
        if playlist.user.id != user_id:
            messages.error(request, "Vous n'avez pas l'autorisation de modifier cette playlist.")
            return redirect('users:playlists')
        
        context = {
            'username': username,
            'playlist': playlist
        }
        
        return render(request, 'edit_playlist.html', context)
    
    def post(self, request, playlist_id):
        if 'user_id' not in request.session:
            return redirect('users:login')
        
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        
        playlist = get_object_or_404(Playlist, id=playlist_id)
        
        # Check if user owns the playlist
        if playlist.user.id != user_id:
            messages.error(request, "Vous n'avez pas l'autorisation de modifier cette playlist.")
            return redirect('users:playlists')
        
        playlist.nom = request.POST.get('nom')
        playlist.description = request.POST.get('description', '')
        playlist.visibilite = request.POST.get('visibilite')
        
        # Remove image handling
        # if 'image' in request.FILES:
        #     playlist.image = request.FILES['image']
        
        playlist.save()
        
        messages.success(request, "Playlist mise à jour avec succès!")
        return redirect('users:playlist_detail', playlist_id=playlist.id)

# Delete playlist view
class delete_playlist(View):
    def post(self, request, playlist_id):
        if 'user_id' not in request.session:
            return redirect('users:login')
        
        user_id = request.session['user_id']
        playlist = get_object_or_404(Playlist, id=playlist_id)
        
        # Check if user owns the playlist
        if playlist.user.id != user_id:
            messages.error(request, "Vous n'avez pas l'autorisation de supprimer cette playlist.")
            return redirect('users:playlists')
        
        playlist.delete()
        
        messages.success(request, "Playlist supprimée avec succès!")
        return redirect('users:playlists')

# Nouvelle vue pour récupérer les morceaux de l'utilisateur
class user_tracks(View):
    def get(self, request):
        if 'user_id' not in request.session:
            return JsonResponse({'error': 'User not logged in'}, status=401)
        
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        
        tracks = Morceau.objects.filter(user=user)
        tracks_data = []
        
        for track in tracks:
            tracks_data.append({
                'id': track.id,
                'titre': track.titre,
                'artiste': track.artiste,
                'genre': track.genre,
                'fichier_url': track.fichier.url if track.fichier else None,
            })
        
        return JsonResponse({'tracks': tracks_data})

# Clear history view
class clear_history(View):
    def post(self, request):
        if 'user_id' not in request.session:
            return redirect('users:login')
        
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        
        # Supprimer tout l'historique de l'utilisateur
        Historique.objects.filter(user=user).delete()
        
        messages.success(request, "Votre historique d'écoute a été supprimé avec succès!")
        return redirect('users:history')

# Delete track view
class delete_track(View):
    def get(self, request, track_id):
        if 'user_id' not in request.session:
            return redirect('users:login')
        
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        
        # Get the track
        track = get_object_or_404(Morceau, id=track_id)
        
        # Check if user owns the track
        if track.user.id != user_id:
            messages.error(request, "Vous n'avez pas l'autorisation de supprimer ce morceau.")
            return redirect('users:profile')
        
        # Delete the track
        track.delete()
        
        messages.success(request, "Morceau supprimé avec succès!")
        return redirect('users:profile')