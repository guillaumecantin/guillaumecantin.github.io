#!/usr/bin/env python3.5

"""
guillaumecantin.pythonanywhere.com/simulation
Web interface for simulating dynamical systems
Current file: urls.py
"""

from django.conf.urls import url
from django.contrib import admin
from . import views

from simulation.admin import admin_site

urlpatterns = [
    url(r'^myadmin/', admin_site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^error/$', views.error, name='error'),
    url(r'^about/', views.about, name='about'),
    url(r'^figures/', views.figures, name='figures'),
    url(r'^animations/', views.animations, name='animations'),
    url(r'^simulations/', views.simulations, name='simulations'),
    url(r'^figure/(?P<figure_id>[0-9]+)/$', views.figure, name='figure'),
    url(r'^animation/(?P<animation_id>[0-9]+)/$', views.animation, name='animation'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^bluesky/$', views.bluesky, name='bluesky'),
    url(r'^bazykin/$', views.bazykin, name='bazykin'),
    url(r'^vanderpol/$', views.vanderpol, name='vanderpol'),
    url(r'^hamiltonian/$', views.hamiltonian, name='hamiltonian'),
    url(r'^pcrsystem/$', views.pcrsystem, name='pcrsystem'),
    url(r'^poincaresphere/$', views.poincaresphere, name='poincaresphere'),
    url(r'^fhn/$', views.fhn, name='fhn'),
    url(r'^poincaremap/$', views.poincaremap, name='poincaremap'),
    url(r'^randomgraph/$', views.randomgraph, name='randomgraph'),
    url(r'^pcrnetwork/$', views.pcrnetwork, name='pcrnetwork'),
    url(r'^tsunami/$', views.tsunami, name='tsunami'),
    url(r'^admin/', admin.site.urls),
]
