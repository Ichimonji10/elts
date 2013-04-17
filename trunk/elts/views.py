from django import http, template
from elts.models import Item

# TODO: flesh out all the things!

def index(request):
    tplate = template.loader.get_template('elts/base.html')
    ctext = template.RequestContext(
        request,
        {}
    )
    return http.HttpResponse(tplate.render(ctext))

def calendar(request):
    tplate = template.loader.get_template('elts/base.html')
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
    tplate = template.loader.get_template('elts/base.html')
    ctext = template.RequestContext(
        request,
        {}
    )
    return http.HttpResponse(tplate.render(ctext))

def lend(request):
    tplate = template.loader.get_template('elts/base.html')
    ctext = template.RequestContext(
        request,
        {}
    )
    return http.HttpResponse(tplate.render(ctext))

def tag(request):
    tplate = template.loader.get_template('elts/base.html')
    ctext = template.RequestContext(
        request,
        {}
    )
    return http.HttpResponse(tplate.render(ctext))
