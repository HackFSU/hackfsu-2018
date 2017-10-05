"""hackfsu_com URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URL conf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from hackfsu_com.admin import hackfsu_admin


app_name = 'hackfsu'
handler404 = 'webapp.views.handler404'
handler500 = 'webapp.views.handler500'

urlpatterns = [
    url(r'^api/', include('api.urls', namespace='api')),
    url(r'^admin/django/', hackfsu_admin.urls),
    url('', include('webapp.urls', namespace='webapp'))
]

if settings.DEBUG:
    urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
