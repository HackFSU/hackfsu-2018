"""
    Public hack roster
"""

from hackfsu_com.views.generic import PageView


class HacksPage(PageView):
    template_name = 'hacks/index.html'
