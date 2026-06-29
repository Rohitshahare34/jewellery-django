from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import get_adapter as get_account_adapter
from django.contrib.auth import get_user_model


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """
        Invoked just after a user successfully authenticates via a
        social provider, but before the login is actually processed.
        This method can be used to prevent logins or connect accounts.
        """
        # Check if this social account is already connected to a user
        if sociallogin.is_existing:
            return

        # Try to find an existing user with the same email
        email = sociallogin.account.extra_data.get('email')
        if email:
            User = get_user_model()
            try:
                user = User.objects.get(email__iexact=email)
                # Connect the existing user to this social account
                sociallogin.connect(request, user)
            except User.DoesNotExist:
                pass
