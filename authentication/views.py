from urllib.parse import urlencode

import environ
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

# Initialize environ
env = environ.Env()


class CustomGoogleOAuth2Client(OAuth2Client):
    def __init__(
            self,
            request,
            consumer_key,
            consumer_secret,
            access_token_method,
            access_token_url,
            callback_url,
            _scope,
            scope_delimiter=" ",
            headers=None,
            basic_auth=False,
    ):
        super().__init__(
            request,
            consumer_key,
            consumer_secret,
            access_token_method,
            access_token_url,
            callback_url,
            scope_delimiter,
            headers,
            basic_auth,
        )


class GoogleLoginUrlView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        google_oauth_url = f"https://accounts.google.com/o/oauth2/v2/auth"
        client_id = env('GOOGLE_CLIENT_ID')
        redirect_uri = env('GOOGLE_CALLBACK_URL')

        params = {
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            'response_type': 'code',
            'scope': 'email profile',
            'access_type': 'offline',
            'prompt': 'consent',
        }

        params_encoded = urlencode(params)
        auth_url = f"{google_oauth_url}?{params_encoded}"
        return Response({'auth_url': auth_url})


class GoogleLogin(SocialLoginView):
    authentication_classes = []
    adapter_class = GoogleOAuth2Adapter
    callback_url = env('GOOGLE_CALLBACK_URL')
    client_class = CustomGoogleOAuth2Client
