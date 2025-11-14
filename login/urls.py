from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    #path('webauthn/register/begin/', views.register_begin, name='webauthn_register_begin'),
    #path('webauthn/register/complete/', views.register_complete, name='webauthn_register_complete'),
    #path('webauthn/auth/begin/', views.auth_begin, name='webauthn_auth_begin'),
    #path('webauthn/auth/complete/', views.auth_complete, name='webauthn_auth_complete'),
    #path('webauthn/register/ui/', views.webauthn_register_ui, name='webauthn_register_ui'),
    #path('webauthn/login/ui/', views.webauthn_login_ui, name='webauthn_login_ui'),
]

