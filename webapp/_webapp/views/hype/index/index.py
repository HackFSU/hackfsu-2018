"""
    Hype directory, linking to hype pages
"""

from hackfsu_com.views.generic import PageView


class HypeIndex(PageView):
    template_name = 'hype/index/index.html'
