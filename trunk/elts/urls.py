from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'elts.views.index'),

    # READ items
    # * links for CRUD-ing each item
    #
    # READ item
    # * tools for CRUD-ing notes
    #
    # READ tags
    # * links for CRUD-ing each tag
    #
    # READ lends and reservations
    # * links for CRU-ing each lend
    # * links for CRUD-ing each reservation
    # * display lends and reservations using a calendar?
)
