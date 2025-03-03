from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings


class CustomAccountAdapter(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, emailconfirmation):
        frontend_url = settings.FRONTEND_URL.rstrip('/')
        verification_path = settings.EMAIL_VERIFICATION_PATH.lstrip('/')
        return f"{frontend_url}/{verification_path}/{emailconfirmation.key}"

    def send_confirmation_mail(self, request, emailconfirmation, signup):
        # Override this method if you want to customize the email content
        return super().send_confirmation_mail(request, emailconfirmation, signup)
