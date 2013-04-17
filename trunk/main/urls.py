"""URLs and URL operations provided by the main app.

The following documents what URLs are available for use, what messages can be
sent to each, and what type of information is returned from each.

URL "nouns"
===========

====== ======== ====== ======== ========
URL    POST     GET    PUT      DELETE
       (create) (read) (update) (delete)
====== ======== ====== ======== ========
\/              *
/elts/          *
====== ======== ====== ======== ========

GET /
    Redirects the user to ``/elts/``.

GET /elts/
    Makes available URLs in the ELTS application. See documentation on
    ``elts.urls`` for details.

URL "verbs"
===========

No URL "verbs" are provided by this app.

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
