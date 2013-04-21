from django import http, template
from elts.models import Item, Reservation, Lend, Tag

def index(request):
    tplate = template.loader.get_template('elts/index.html')
    ctext = template.RequestContext(
        request,
        {}
    )
    return http.HttpResponse(tplate.render(ctext))

def calendar(request):
    tplate = template.loader.get_template('elts/calendar.html')
    ctext = template.RequestContext(
        request,
        {}
    )
    return http.HttpResponse(tplate.render(ctext))

def item(request):
    tplate = template.loader.get_template('elts/item.html')
    ctext = template.RequestContext(
        request,
        {
            'items': Item.objects.all()
        }
    )
    return http.HttpResponse(tplate.render(ctext))

def reservation(request):
    tplate = template.loader.get_template('elts/reservation.html')
    ctext = template.RequestContext(
        request,
        {
            'reservations': Reservation.objects.all()
        }
    )
    return http.HttpResponse(tplate.render(ctext))

def lend(request):
    tplate = template.loader.get_template('elts/lend.html')
    ctext = template.RequestContext(
        request,
        {
            'lends': Lend.objects.all()
        }
    )
    return http.HttpResponse(tplate.render(ctext))

def tag(request):
    tplate = template.loader.get_template('elts/tag.html')
    ctext = template.RequestContext(
        request,
        {
            'tags': Tag.objects.all()
        }
    )
    return http.HttpResponse(tplate.render(ctext))
