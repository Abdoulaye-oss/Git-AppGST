from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.shortcuts import render,redirect
from django.contrib.auth import logout
from django.urls import reverse
from . forms import UserForm
from .forms import LoginForm


User = get_user_model()
def signup(request):
    # Vérifier si l'utilisateur est déjà authentifié
    #if request.user.is_authenticated:
        #return redirect('interfaces:accueil')

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            # Rediriger vers la page de connexion (login form) après une inscription réussie
            return redirect('accounts:login')
    else:
        form = UserForm()
        
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)

# Dans votre fichier views.py



def logout_view(request):
    """
    Vue pour gérer la déconnexion de l'utilisateur.
    """
    logout(request)
    # Redirection vers une page de confirmation ou une autre page après la déconnexion
    return HttpResponseRedirect(reverse('accounts:login'))  # Redirige vers la page d'accueil par exemple



"""def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Rediriger l'utilisateur vers une page appropriée après la connexion
                return redirect('interfaces:index')  # Remplacez 'home' par le nom de votre page d'accueil
            else:
                # Gérer le cas où l'authentification échoue
                return render(request, 'accounts/login.html', {'form': form, 'error_message': 'Nom d\'utilisateur ou mot de passe incorrect.'})
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})
"""