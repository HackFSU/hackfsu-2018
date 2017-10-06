from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse


def logout_view(request):
    """
        Logs user out then redirects to login
    """
    logout(request)
    return redirect(to=reverse('webapp:user-login'))

