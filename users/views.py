from django.shortcuts import render, redirect
from django.views import View
from .models import User
from django.contrib import messages

class home(View):
    def get(self, request):
        return render(request, 'base.html')

class dashboard(View):
    def get(self, request):
        return render(request, 'dashboard.html')

class registre(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        # Récupérer les données du formulaire
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Vérifier si les mots de passe correspondent
        if password != confirm_password:
            messages.error(request, 'Les mots de passe ne correspondent pas')
            return redirect('register')

        # Vérifier si l'utilisateur existe déjà
        if User.objects.filter(username=username).exists():
            messages.error(request, "Ce nom d'utilisateur existe déjà")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Cette adresse email est déjà utilisée")
            return redirect('register')

        # Créer un nouvel utilisateur
        try:
            user = User(
                username=username,
                email=email,
                password=password,
                confirm_password=confirm_password
            )
            user.save()
            messages.success(request, 'Inscription réussie!')
            return redirect('login')
        except Exception as e:
            messages.error(request, "Une erreur s'est produite lors de l'inscription")
            return redirect('register')

class login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username, password=password)
            # Si l'utilisateur est trouvé, on le redirige vers le dashboard
            return redirect('users:dashboard')
        except User.DoesNotExist:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect")
            return redirect('users:login')

class logout(View):
    def get(self, request):
        # Ici, nous redirigeons simplement vers la page d'accueil
        # Dans une implémentation complète avec Django Auth, nous utiliserions auth.logout(request)
        messages.success(request, "Vous avez été déconnecté avec succès")
        return redirect('users:home')