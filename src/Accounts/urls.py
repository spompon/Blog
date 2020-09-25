import os
from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views
from .forms import PasswordResetFormMod, SetPasswordFormMod

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('password/change/', views.change_password, name='change-password'),
    path('profile/edit/', views.edit_profile,  name='edit-profile'),
    path('notifications/settings/', views.notifications_settings,  name='notifications-settings'),
    path('<slug>/favorites/add', views.favorites, name='favorites'),


    # Fonctionnalités intégrés django.contrib.auth.views permmettant le reset du mot de passe
    path('password_reset/', auth_views.PasswordResetView.as_view(form_class=PasswordResetFormMod,
                                                                 template_name='accounts/password_reset_form.html',
                                                                 email_template_name='accounts/password_reset_email.html',
                                                                 subject_template_name='accounts/password_reset_subject.txt',
                                                                 success_url=reverse_lazy('accounts:password_reset_done')), name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(form_class=SetPasswordFormMod,
                                                                                template_name='accounts/password_reset_confirm.html',
                                                                                success_url=reverse_lazy('accounts:password_reset_complete')), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete')

]