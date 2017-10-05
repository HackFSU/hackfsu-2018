from . import registration
from . import user
from . import test
from . import hype
from . import organize
from . import mentor
from . import judge
from .index import IndexPage
from .help import HelpPage
from .links.index import LinksPage
from .hacks.index import HacksPage
from django.shortcuts import render


def handler404(request):
    response = render(request, 'error/404/index.html')
    response.status_code = 404
    return response


def handler500(request):
    response = render(request, 'error/500/index.html')
    response.status_code = 500
    return response
