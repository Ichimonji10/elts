"""URLs and HTTP operations provided by the ``main`` app.

This table summarizes what URLs are available for use and what types of HTTP
requests can be accepted by each. Details about each URL, including arguments,
are given after the table.

========== ======== ====== ======== ========
URL        POST     GET    PUT      DELETE
           (create) (read) (update) (delete)
========== ======== ====== ======== ========
``/``               *
``elts/``           *
========== ======== ====== ======== ========

``/``
    ``GET`` requests return a redirect to ``GET elts/``.

``elts/``
    ``GET`` requests are forwarded to the ``elts`` django app. See
    ``elts/urls.py`` for details on what URLs it provides.

"""
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns( # pylint: disable=C0103
    '',
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
