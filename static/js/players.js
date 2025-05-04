// This file is correctly named 'players.js' (with an 's')
// We'll check the HTML files to update references to this script

// Gestionnaire de lecture audio
document.addEventListener('DOMContentLoaded', function() {
    // Variables globales
    let currentAudio = null;
    let isPlaying = false;
    
    // Fonction pour jouer un morceau
    window.playTrack = function(trackId, button) {
        console.log("playTrack appelée avec trackId:", trackId);
        
        // Si on clique sur le même morceau qui est en cours de lecture
        if (currentAudio && currentAudio.dataset.trackId === trackId && isPlaying) {
            console.log("Pause du morceau en cours de lecture");
            currentAudio.pause();
            button.innerHTML = '<i class="fas fa-play"></i>';
            isPlaying = false;
            return;
        }
        
        // Si un morceau est déjà en cours de lecture, l'arrêter
        if (currentAudio && currentAudio.dataset.trackId !== trackId) {
            console.log("Arrêt du morceau précédent pour jouer un nouveau");
            currentAudio.pause();
            // Réinitialiser tous les boutons de lecture/pause
            document.querySelectorAll('.play-pause-btn, .play-track').forEach(btn => {
                btn.innerHTML = '<i class="fas fa-play"></i>';
            });
        }
        
        // Si le morceau est déjà chargé mais en pause
        if (currentAudio && currentAudio.dataset.trackId === trackId && !isPlaying) {
            console.log("Reprise du morceau en pause");
            currentAudio.play()
                .then(() => {
                    button.innerHTML = '<i class="fas fa-pause"></i>';
                    isPlaying = true;
                })
                .catch(error => {
                    console.error("Erreur lors de la reprise de la lecture:", error);
                });
            return;
        }
        
        // Charger un nouveau morceau
        console.log("Chargement d'un nouveau morceau:", trackId);
        fetch(`/play/${trackId}/`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erreur réseau lors du chargement du morceau');
                }
                return response.json();
            })
            .then(data => {
                console.log("Données du morceau reçues:", data);
                if (!data.file_url) {
                    throw new Error('URL du fichier audio non trouvée');
                }
                
                // Créer un nouvel élément audio
                const audio = new Audio(data.file_url);
                audio.dataset.trackId = trackId;
                
                // Configurer les événements
                audio.addEventListener('ended', function() {
                    button.innerHTML = '<i class="fas fa-play"></i>';
                    isPlaying = false;
                });
                
                // Mettre à jour les informations globales avant la lecture
                currentAudio = audio;
                
                // Jouer le morceau
                console.log("Début de la lecture du morceau");
                const playPromise = audio.play();
                
                if (playPromise !== undefined) {
                    playPromise
                        .then(() => {
                            console.log("Lecture démarrée avec succès");
                            button.innerHTML = '<i class="fas fa-pause"></i>';
                            isPlaying = true;
                            
                            // Afficher la barre de lecteur si nécessaire
                            const playerBar = document.querySelector('.player-bar');
                            if (playerBar) {
                                playerBar.classList.remove('d-none');
                                
                                // Mettre à jour les informations du morceau
                                const trackTitle = playerBar.querySelector('.track-title');
                                const trackArtist = playerBar.querySelector('.track-artist');
                                
                                if (trackTitle && data.titre) {
                                    trackTitle.textContent = data.titre;
                                }
                                
                                if (trackArtist && data.artiste) {
                                    trackArtist.textContent = data.artiste;
                                }
                            }
                        })
                        .catch(error => {
                            console.error("Erreur lors du démarrage de la lecture:", error);
                            button.innerHTML = '<i class="fas fa-play"></i>';
                            isPlaying = false;
                        });
                }
            })
            .catch(error => {
                console.error('Erreur lors du chargement du morceau:', error);
                button.innerHTML = '<i class="fas fa-play"></i>';
                alert('Erreur lors du chargement du morceau. Veuillez réessayer.');
            });
    };
    
    // Fonction pour mettre en pause ou reprendre la lecture
    window.togglePlayPause = function() {
        console.log("togglePlayPause appelée");
        if (!currentAudio) {
            console.log("Aucun audio en cours");
            return;
        }
        
        const pauseBtn = document.querySelector('.pause-btn');
        const playButtons = document.querySelectorAll('.play-track');
        
        if (isPlaying) {
            console.log("Mise en pause");
            currentAudio.pause();
            pauseBtn.innerHTML = '<i class="fas fa-play"></i>';
            isPlaying = false;
            
            // Mettre à jour le bouton correspondant dans la liste
            playButtons.forEach(btn => {
                if (btn.getAttribute('data-track-id') === currentAudio.dataset.trackId) {
                    btn.innerHTML = '<i class="fas fa-play"></i>';
                }
            });
        } else {
            console.log("Reprise de la lecture");
            const playPromise = currentAudio.play();
            
            if (playPromise !== undefined) {
                playPromise
                    .then(() => {
                        pauseBtn.innerHTML = '<i class="fas fa-pause"></i>';
                        isPlaying = true;
                        
                        // Mettre à jour le bouton correspondant dans la liste
                        playButtons.forEach(btn => {
                            if (btn.getAttribute('data-track-id') === currentAudio.dataset.trackId) {
                                btn.innerHTML = '<i class="fas fa-pause"></i>';
                            }
                        });
                    })
                    .catch(error => {
                        console.error("Erreur lors de la reprise de la lecture:", error);
                    });
            }
        }
    };
    
    // Fonction pour arrêter la lecture
    window.stopPlayback = function() {
        console.log("Fonction stopPlayback appelée");
        
        if (!currentAudio) {
            console.log("Aucun audio en cours de lecture");
            return;
        }
        
        console.log("Arrêt de la lecture audio");
        currentAudio.pause();
        currentAudio.currentTime = 0;
        isPlaying = false;
        
        // Réinitialiser tous les boutons
        const playButtons = document.querySelectorAll('.play-pause-btn, .play-track');
        console.log("Nombre de boutons de lecture trouvés:", playButtons.length);
        playButtons.forEach(btn => {
            btn.innerHTML = '<i class="fas fa-play"></i>';
        });
        
        // Mettre à jour le bouton de pause si présent
        const pauseBtn = document.querySelector('.pause-btn');
        if (pauseBtn) {
            pauseBtn.innerHTML = '<i class="fas fa-play"></i>';
        }
        
        // Masquer le lecteur si nécessaire
        const playerBar = document.querySelector('.player-bar');
        console.log("Barre de lecteur trouvée:", playerBar !== null);
        if (playerBar) {
            playerBar.classList.add('d-none');
        }
        
        // Réinitialiser l'audio
        currentAudio = null;
    };
});