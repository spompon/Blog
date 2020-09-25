from django import forms
from .models import User
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth import authenticate
from django.conf import settings

# user = settings.AUTH_USER_MODEL # Permet d'accéder à l'objet user

# Inscription
class RegisterForm(forms.ModelForm):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={
        'placeholder': "Nom d'utilisateur",
        'class': 'form-control',
    }))

    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={
        'placeholder': 'Adresse e-mail',
        'class': 'form-control',
    }))

    password = forms.CharField(label='', min_length=8, widget=forms.PasswordInput(attrs={
        'placeholder': 'Mot de passe',
        'class': 'form-control',
    }))
    terms = forms.BooleanField(label='',  widget=forms.CheckboxInput(attrs={ # champ du formumaire ajouté en plus de ceux du Model
        'class': 'custom-control-input',
    }))


    class Meta:
        model = User
        fields = ['username', 'email', 'password']


# Login
class LoginForm(forms.Form): # Ici pas de modelForm pour éviter les problèmes
    username = forms.CharField(label='', widget=forms.TextInput(attrs={
        'placeholder': "Nom d'utilisateur",
        'class': 'form-control',

    }))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={
        'placeholder': 'Mot de passe',
        'class': 'form-control',
    }))

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:  # Si les 2 champs ne sont pas vide
            user = authenticate(username=username, password=password)

            if not user or not user.check_password(password):  # Si l'utilisateur n'existe pas
                raise forms.ValidationError("Utilisateur ou mot de passe erroné")
        return super().clean(*args, **kwargs)



# Myaccount
class UpdateForm(forms.ModelForm):
    username = forms.CharField(label='Nom d’utilisateur', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'readonly': 'readonly'  # Champ non éditable (readonly{{
    }))

    email = forms.EmailField(label='Adresse e-mail', widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'id': 'email',
    }))

    first_name = forms.CharField(required=False, label='Prénom', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'first-name',
    }))

    last_name = forms.CharField(required=False, label='Nom', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'last-name',
    }))

    city = forms.CharField(required=False, label='Ville', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'city',
    }))

    country = forms.CharField(required=False, label='Pays', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'country',
    }))

    birth_date = forms.DateField(required=False, label='Date de naissance', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Sélectionner une date',
        'id': 'birthday',
        'type':  'date' # On modifie le rendu de champ pour les dates
    }))

    website = forms.URLField(required=False, label='Site internet', widget=forms.URLInput(attrs={
        'class': 'form-control',
        'id': 'website',
    }))

    bio = forms.CharField(required=False, label='Quelques mots sur vous', widget=forms.Textarea(attrs={
        'class': 'form-control',
        'id': 'bio',
        'rows': 6,
    }))

    profile_picture = forms.ImageField(required=False, label='Modifier image', widget=forms.FileInput(attrs={
        'class': 'form-control-file',
        'id': 'profile_picture',


    }))

    class Meta:
        model = User
        fields = ['username',
                  'email',
                  'first_name',
                  'last_name',
                  'profile_picture',
                  'city',
                  'country',
                  'birth_date',
                  'website',
                  'bio',
                  ]


# Modification du mot de passe
class UpdatePassword(forms.ModelForm):
    password = forms.CharField(label="Mot de passe actuel", widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'password'
    }))
    new_password = forms.CharField(label="Nouveau mot de passe", widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'new_password'
    }))
    confirm_password = forms.CharField(label="Confirmer nouveau mot de passe", widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'confirm_password'
    }))
    class Meta:
        model = User
        fields = ['password'] # En base de donnée, on ne modifie que password


#########################
# Reset du mot de passe (modification form par défaut)
##########################
class PasswordResetFormMod(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={
            'autocomplete': 'email',
            'class': 'form-control',
            'placeholder': 'Votre adresse e-mail'
        })
    )


class SetPasswordFormMod(SetPasswordForm):
    new_password1 = forms.CharField(label= 'Nouveau mot de passe',
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'class': 'form-control',
            'id': 'new_password1',
        }),
        strip=False,


    )
    new_password2 = forms.CharField(label= 'Confirmer mot de passe',
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'class': 'form-control',
            'id': 'new_password2',

        }),
        strip=False,
    )
