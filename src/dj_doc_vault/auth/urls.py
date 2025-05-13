from django.urls import path
from dj_doc_vault.auth import views

app_name = "dj_doc_vault-auth"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("login/google/", views.signin_with_google_view, name="signin-with-google"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    path("settings/account/", views.account_settings_view, name="account-settings"),
    path("settings/email/", views.email_settings_view, name="email-settings"),
    path("settings/security/", views.security_settings_view, name="security-settings"),
]
