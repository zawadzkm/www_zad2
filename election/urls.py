from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^login/$', auth_views.login, name='login', kwargs={'template_name': 'login.html'}),
    url(r'^logout/$', auth_views.logout, name='logout', kwargs={'next_page': '/'}),
    url(r'^search/$', views.search, name='search'),
    url(r'^$', views.country, name='index'),
    url(r'^(?P<id>[0-9]{1,2})/$', views.voivodeship),
    url(r'^(?P<vid>[0-9]{1,2})/(?P<id>[0-9]{1,2})/$', views.district),
    url(r'^(?P<vid>[0-9]{1,2})/(?P<did>[0-9]{1,2})/(?P<id>[0-9]{1,4})/$', views.commune),
    url(r'^(?P<vid>[0-9]{1,2})/(?P<did>[0-9]{1,2})/(?P<cid>[0-9]{1,4})/(?P<circid>[0-9]+)/(?P<candid>[0-9]+)/update$', views.vote_update)
]