"""URLs and URL operations provided by the ``main`` app.

This table summarizes what URIs are available for use and what types of HTTP
requests can be accepted by each. Details about each URI, including arguments,
are given after the table.

========== ======== ====== ======== ========
URI        POST     GET    PUT      DELETE
           (create) (read) (update) (delete)
========== ======== ====== ======== ========
``/``               *
``elts/``           *
========== ======== ====== ======== ========

``/``
    ``GET`` redirects the user to ``GET elts/``.

``elts/``
    ``GET`` requests are forwarded to the ``elts`` django app. See
    ``elts/urls.py`` for details on what URIs it provides.

"""
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

# pylint: disable=C0103
# "Invalid name "urlpatterns" for type constant (should match
# (([A-Z_][A-Z0-9_]*)|(__.*__))$)"
urlpatterns = patterns('',
    url(r'^$', 'main.views.index'),
    url(r'^elts/', include('elts.urls')),
    # Examples:
    # url(r'^$', 'main.views.home', name='home'),
    # url(r'^main/', include('main.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
