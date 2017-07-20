from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^space-invaders/', include('space_invaders.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^.*$', RedirectView.as_view(url='space-invaders/', permanent=False), name='main_index'),
]
