from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^hourly_form/$', views.hourly_form, name = 'hourly_form'),
    url(r'^monthly_form/$', views.monthly_form, name = 'monthly_form'),
    url(r'^housing_form/$', views.housing_form, name = 'housing_form'),
    url(r'^contact/$', views.contact, name = 'contact'),
    url(r'^output/$', views.output, name = 'output'),
    url(r'^calculation/$', views.calculation, name = 'calculation'),
    ]

from django.conf.urls import include

urlpatterns += [
    url(r'^tellme/', include("tellme.urls")),
]
