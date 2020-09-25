from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .forms import RegisterForm, LoginForm, UpdateForm, UpdatePassword
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User
from django.urls import resolve
from Posts.models import Post


# Fonction retournant le name de l'url ex: name='post-detail'
def get_url_name(url):
    return resolve(url).url_name


###########
# Les views
############

def register_view(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False) # L'instance est crée mais pas encore enregistrée
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()

            auth_user = authenticate(username=user.username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                print('Utilisateur loggé')
                return redirect('accounts:edit-profile')
            else:
                print('Utilisateur non enregistrer dans la BDD')
                return redirect('index')

    context = {
        'title': 'Inscription',
        'form': form,
    }
    return render(request, 'accounts/register.html', context=context)


def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                print('Utilisateur loggé')
                return redirect('accounts:edit-profile')
            else:
                print('Utilisateur non enregistrer dans la BDD')
                return redirect('index')

    context = {
        'title': 'Connectez-vous',
        'form': form,
    }
    return render(request, 'accounts/login.html', context=context)


@login_required()
def logout_view(request):
    logout(request)
    return redirect('index')


@login_required()
def member_account(request):
    form = UpdateForm(request.POST or None, request.FILES or None, instance=request.user)
    member = get_object_or_404(User, id=request.user.id) # (1)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.info(request, 'Votre compte a été mis à jour')
            return redirect('accounts:myaccount')

    context = {
        'title': 'Mon compte',
        'form': form,
        'member': member,

    }
    return render(request, 'accounts/account-settings.html', context=context)


"""
(1)
id doit correspondre à l'id de l'utilisateur qui est connecté
"""

#####################
# Accounts settings
#####################

@login_required()
def change_password(request):
    member = get_object_or_404(User, id=request.user.id)  # (1)
    form = UpdatePassword(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            print("Formulaire valide")
            password = form.cleaned_data.get('password')
            new_password = form.cleaned_data.get('new_password')
            confirm_password = form.cleaned_data.get('confirm_password')
            if member.check_password(password) and new_password == confirm_password:
                print("Mot de passe existant et 2 champs idnetiques")
                member.set_password(new_password) # On redifinit le mot de passe
                member.save()
                messages.info(request, 'Mot de passe mis à jour')
                auth_user = authenticate(username=member.username, password=password)
                if auth_user is not None:
                    login(request, auth_user)
                    print('Utilisateur loggé')
                    return redirect('accounts:change-password')

    context = {
        'title': 'Changer de mot de passe',
        'form': form,
        'page': request.path,
    }
    return render(request, 'accounts/change-password.html', context=context)


@login_required()
def edit_profile(request):
    form = UpdateForm(request.POST or None, request.FILES or None, instance=request.user)
    member = get_object_or_404(User, id=request.user.id)  # (1)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.info(request, 'Votre compte a été mis à jour')
            return redirect('accounts:edit-profile')

    context = {
        'title': 'Modifier le profil',
        'form': form,
        'member': member,
        'page': request.path,

    }
    return render(request, 'accounts/edit-profile.html', context=context)

@login_required()
def notifications_settings(request):
    return None

@login_required()
def favorites(request, slug):
    article = get_object_or_404(Post, slug=slug)
    member = request.user
    context = {
        'article': article
    }
    return render(request, 'accounts/favorites.html', context=context)