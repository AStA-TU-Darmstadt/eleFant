from django.conf.urls import url

from . import views

app_name = 'antraege'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^new$', views.new_application, name='new'),
    url(r'^(?P<pk>([a-z0-9]+-)+[a-z0-9]+)/$', views.ApplicationDetail.as_view(), name='detail'),
    url(r'^search$', views.search_application, name='search'),
]
