import requests
from django.core.files.base import ContentFile
from django.dispatch import receiver
from allauth.socialaccount.signals import social_account_updated, pre_social_login
from allauth.account.signals import user_signed_up


@receiver(social_account_updated)
@receiver(pre_social_login)
@receiver(user_signed_up)
def update_user_avatar_from_social_account(sender, **kwargs):
    """
    Update user profile with data from social account, including avatar.
    """
    # For pre_social_login
    if "sociallogin" in kwargs:
        sociallogin = kwargs["sociallogin"]
        user = sociallogin.user
        account = sociallogin.account
    # For user_signed_up and social_account_updated
    elif "user" in kwargs and "socialaccount" in kwargs:
        user = kwargs["user"]
        account = kwargs["socialaccount"]
    else:
        return

    # Handle Google provider
    if account.provider == "google":
        # Get profile data
        data = account.extra_data

        # Update user's name if not already set
        if not user.name:
            user.name = data.get("name", "")

        # Update avatar if picture URL is available
        picture_url = data.get("picture")
        if picture_url and (
            not user.avatar or "googleusercontent.com" in str(user.avatar)
        ):
            try:
                response = requests.get(picture_url)
                if response.status_code == 200:
                    # Create a unique filename
                    filename = f"google_{user.id}.jpg"
                    user.avatar.save(filename, ContentFile(response.content), save=True)
            except Exception as e:
                print(f"Error saving Google profile picture: {e}")

        user.save()
