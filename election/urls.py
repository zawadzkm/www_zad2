from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^login/$', auth_views.login, name='login', kwargs={'template_name': 'login.html'}),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^search/$', views.search, name='search'),
    url(r'^$', views.country, name='index'),
    url(r'^(?P<vno>[0-9]{1,2})/$', views.voivodeship, name='voivodeship'),
    url(r'^(?P<vno>[0-9]{1,2})/(?P<dno>[0-9]{1,2})/$', views.district, name='district'),
    url(r'^(?P<vno>[0-9]{1,2})/(?P<dno>[0-9]{1,2})/(?P<ccode>[0-9]+)/$', views.commune, name='commune'),
    url(r'^(?P<vno>[0-9]{1,2})/(?P<dno>[0-9]{1,2})/(?P<ccode>[0-9]+)/(?P<circid>[0-9]+)/(?P<candid>[0-9]+)/update$', views.vote_update, name="update")
]