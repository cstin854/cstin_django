"""mysite URL Configuration

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
from . import views

#Added to remove potential namespace conflicts
app_name = 'music'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    #Automatically looks for album_form.html
    #I think I'd like to eventually make my own isntead of relying
    url(r'album/add/$', views.AlbumCreate.as_view(), name='album-add'),
    #/music/url/<album_id>/update
    url(r'^album/(?P<pk>[0-9]+)/$', views.AlbumUpdate.as_view(), name='album-update'),
    #/music/album/<pk>/delete
    url(r'^album/(?P<pk>[0-9]+)/delete/$', views.AlbumDelete.as_view(), name='album-delete'),
    #Generic test of POST data
    url(r'post_test/$', views.post_test, name='post-test'),
]
