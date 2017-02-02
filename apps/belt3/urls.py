from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^success$',views.success),
    url(r'^wish_items/(?P<wish_id>\d+)', views.showitem),
    url(r'^home$', views.success),
    url(r'^logout$', views.logout),
    url(r'^create$', views.createwish),
    url(r'^addwish/(?P<wish_id>\d+)', views.addwish),
    url(r'^additem$', views.additem),
    url(r'^removewish/(?P<wish_id>\d+)', views.removewish),
    url(r'^deletewish/(?P<wish_id>\d+)', views.removewish),
    ]
