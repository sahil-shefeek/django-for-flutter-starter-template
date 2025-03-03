from dj_rest_auth.registration.views import VerifyEmailView
from django.urls import path, include

from authentication.views import GoogleLogin, GoogleLoginUrlView

urlpatterns = [
    path("", include("dj_rest_auth.urls")),
    path("google/callback/", GoogleLogin.as_view(), name="google_login"),
    path("google/url/", GoogleLoginUrlView.as_view(), name="google_login_url"),
    path("register/", include("dj_rest_auth.registration.urls")),
    path(
        "account-confirm-email/",
        VerifyEmailView.as_view(),
        name="account_email_verification_sent",
    ),
]
