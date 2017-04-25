from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

app_name = 'antraege'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^new$', views.ApplicationCreate.as_view(), name='new'),
    url(r'^(?P<pk>([a-z0-9]+-)+[a-z0-9]+)/$', views.ApplicationDetail.as_view(), name='detail'),
    url(r'^(?P<pk>([a-z0-9]+-)+[a-z0-9]+)/edit$', views.application_edit_handler, name='edit'),
    url(r'^(?P<pk>([a-z0-9]+-)+[a-z0-9]+)/edit/a$', views.ApplicationEditAll.as_view(), name='edit_admin'),
    url(r'^(?P<pk>([a-z0-9]+-)+[a-z0-9]+)/edit/u$', views.ApplicationEdit.as_view(), name='edit_user'),
    url(r'^list$', views.ApplicationList.as_view(), name='list'),
    url(r'^search$', views.search_application, name='search'),
    # url(r'^login', views.login_view, name='login'),
    # url(r'^logout', views.logout_view, name='logout'),
    url(
        '^login$',
        auth_views.login,
        {'template_name': 'antraege/login.html'},
        name='login',
    ),
    url(
        '^logout$',
        auth_views.logout,
        name='logout',
    ),
]
