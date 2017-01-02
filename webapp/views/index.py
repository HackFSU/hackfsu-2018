"""
    Website Home
"""

from .generic import PageView


class IndexPage(PageView):
    template_name = 'index.html'
