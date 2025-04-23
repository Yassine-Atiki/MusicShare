// Gestionnaire de lecture audio
document.addEventListener('DOMContentLoaded', function() {
    // Variables globales
    let currentAudio = null;
    let isPlaying = false;
    
    // Fonction pour jouer un morceau
    window.playTrack = function(trackId, button) {
        // Si un morceau est déjà en cours de lecture, l'arrêter
        if (currentAudio) {
            currentAudio.pause();
            // Réinitialiser tous les boutons de lecture/pause
            document.querySelectorAll('.play-pause-btn').forEach(btn => {
                btn.innerHTML = '<i class="fas fa-play"></i>';
            });
        }
        
        // Si on clique sur le même morceau qui est en cours de lecture
        if (currentAudio && currentAudio.dataset.trackId === trackId && isPlaying) {
            currentAudio.pause();
            button.innerHTML = '<i class="fas fa-play"></i>';
            isPlaying = false;
            return;
        }
        
        // Si le morceau est déjà chargé mais en pause
        if (currentAudio && currentAudio.dataset.trackId === trackId && !isPlaying) {
            currentAudio.play();
            button.innerHTML = '<i class="fas fa-pause"></i>';
            isPlaying = true;
            return;
        }
        
        // Charger un nouveau morceau
        fetch(`/play/${trackId}/`)
            .then(response => response.json())
            .then(data => {
                // Créer un nouvel élément audio
                const audio = new Audio(data.file_url);
                audio.dataset.trackId = trackId;
                
                // Configurer les événements
                audio.addEventListener('ended', function() {
                    button.innerHTML = '<i class="fas fa-play"></i>';
                    isPlaying = false;
                });
                
                // Jouer le morceau
                audio.play();
                button.innerHTML = '<i class="fas fa-pause"></i>';
                
                // Mettre à jour les variables globales
                currentAudio = audio;
                isPlaying = true;
            })
            .catch(error => {
                console.error('Erreur lors du chargement du morceau:', error);
                alert('Erreur lors du chargement du morceau. Veuillez réessayer.');
            });
    };
    
    // Fonction pour mettre en pause ou reprendre la lecture
    window.togglePlayPause = function() {
        if (!currentAudio) return;
        
        const pauseBtn = document.querySelector('.pause-btn');
        const closeBtn = document.querySelector('.close-btn');
        
        if (isPlaying) {
            currentAudio.pause();
            pauseBtn.innerHTML = '<i class="fas fa-play"></i>';
            isPlaying = false;
        } else {
            currentAudio.play();
            pauseBtn.innerHTML = '<i class="fas fa-pause"></i>';
            isPlaying = true;
        }
    };
    
    // Fonction pour arrêter la lecture
    window.stopPlayback = function() {
        if (!currentAudio) return;
        
        currentAudio.pause();
        currentAudio.currentTime = 0;
        isPlaying = false;
        
        // Réinitialiser tous les boutons
        document.querySelectorAll('.play-pause-btn').forEach(btn => {
            btn.innerHTML = '<i class="fas fa-play"></i>';
        });
        
        // Masquer le lecteur si nécessaire
        const playerBar = document.querySelector('.player-bar');
        if (playerBar) {
            playerBar.classList.add('d-none');
        }
    };
});