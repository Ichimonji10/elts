"""URLs for the ELTS application.

Sample URLs and explanations follow.

/
    The default index page. At the very least, it should show which items are
    going out and due back in today.

/item
/item?tag=laptop
/item?name=macbook
    A list of all items. It is possible to search for specific items from this
    URL. For example, `/item?tag=laptop` would display items with the tag
    "laptop".

/item/1
    Details about the item with an ID of 1. Some information can be edited from
    here, e.g. adding a new note about the item. However, not all fields can be
    edited.

/item/1/edit
    Details about the item with an ID of 1, plus the ability to edit that
    information.

/tag
    A place to create, read (view), update (rename), and delete tags.

/reservation
    TODO: flesh this out more

/lend
    TODO: flesh this out more

/calendar
    A page which displays all reservations and lends on a calendar. TODO: flesh
    this out more

"""
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'elts.views.index'),
)
