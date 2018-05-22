"""choose_elec URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.http import HttpResponse

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^robots.txt', lambda x: HttpResponse("User-Agent: *\nDisallow: /admin\nDisallow: /index/output\nDisallow: /index/contact_thanks", content_type="text/plain"), name="robots_file")
]

from django.conf.urls import include

urlpatterns += [
    url(r'^index/', include('choose_electricity.urls')),
]

# Add URL maps to redirect the base URL to the application
from django.views.generic import RedirectView
urlpatterns += [
    url(r'^$', RedirectView.as_view(url = '/index/', permanent = True)),
]

