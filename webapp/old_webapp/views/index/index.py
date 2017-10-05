"""
    Website Home
"""

from hackfsu_com.views.generic import PageView


class IndexPage(PageView):
    template_name = 'index/index.html'
