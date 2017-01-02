"""
    User log in
"""

from ...generic import PageView


class LoginPage(PageView):
    template_name = 'user/login/index.html'
