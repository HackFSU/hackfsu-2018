"""
    User Profile
"""

from ...generic import PageView


class ProfilePage(PageView):
    template_name = 'user/profile/index.html'
