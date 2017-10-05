"""
    Public hack roster
"""

from hackfsu_com.views.generic import PageView


class HacksPage(PageView):
    allowed_after_current_hackathon_ends = False
    template_name = 'hacks/index.html'
