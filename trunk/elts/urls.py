"""URLs for the ELTS application.

A general description of the URLs used in this app follows.

/
    The default index page. At the very least, it should show which items are
    going out and due back in today.

/items
    A list of all items. It is possible to search for specific items from this
    URL. For example, `/item?tag=laptop` would display items with the tag
    "laptop".

/items/<item_number>
    Details about item <item_number>.

/items/<item_number>/edit_form
    A form for editing item <item_number>.

/tags
    A place to create, read (view), update (rename), and delete tags.

/reservations
    A list of all reservations. Should show whether the reserved item has
    actually been lent out or not.

/lends
    A list of all lends.

/calendar
    A calendar displaying all reservations and lends.

"""
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'elts.views.index'),
)
