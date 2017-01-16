"""
    Help request submission page
"""

from hackfsu_com.views.generic import PageView


class HelpPage(PageView):
    template_name = 'help/index.html'
