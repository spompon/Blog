from django.db import models
from django.contrib.auth.models import AbstractUser

# (1): Évitez d’utiliser null pour des champs textuels comme CharField ou TextField

class User(AbstractUser):
    profile_picture = models.ImageField(upload_to='profiles', default='default.jpg', verbose_name='Image du profil')  # (1)
    city = models.CharField(max_length=30, blank=True, verbose_name="Ville")
    country = models.CharField(max_length=30, blank=True, verbose_name="Pays")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Date de naissance")
    website = models.URLField(blank=True)
    bio = models.TextField(max_length=500, blank=True, verbose_name='Biographie')

    def __str__(self):
        return self.username









#(1) Le fichier sera automatiquement uploadé dans le répertoire : MEDIA_ROOT/profiles/.