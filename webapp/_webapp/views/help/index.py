"""
    Help request submission page
"""

from hackfsu_com.views.generic import PageView
from api.models import Hackathon


class HelpPage(PageView):
    allowed_after_current_hackathon_ends = False
    template_name = 'help/index.html'

    def work(self, request):
        # Make sure in current hackathon
        if not Hackathon.objects.current().is_today():
            self.template_name = 'help/closed.html'

