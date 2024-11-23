from urllib.parse import urljoin

from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse


class CustomAccountAdapter(DefaultAccountAdapter):

    def get_email_confirmation_url(self, request, emailconfirmation):
        """Constructs the email confirmation (activation) url.

        Note that if you have architected your system such that email
        confirmations are sent outside of the request context `request`
        can be `None` here.
        """
        url = reverse("account_confirm_email", args=[emailconfirmation.key])  # /auth/registration/account-confirm-email/<str:key>
        # ret = build_absolute_uri(request, url)
        return urljoin("http://localhost:3000", url)
