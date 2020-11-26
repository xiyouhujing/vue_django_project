# -*- coding: UTF-8 -*-
from django.conf.urls import url, include
from vueapi import views

urlpatterns = [
    url('upload/', views.upload),
    url('showMap/', views.showMap),
    url('login/', views.login),
    url('addData/', views.addData),
    url('delData/', views.delData),
    url('uploadMonitor/', views.uploadMonitor),
    url('showMonitor/', views.showMonitor),
]
