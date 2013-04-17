from django import http, template

# TODO: flesh out all the things!

def index(request):
    tplate = template.loader.get_template('elts/base.html')
    ctext = template.RequestContext(
        request,
        {
            'title': 'index',
            'body': 'body',
        }
    )
    return http.HttpResponse(tplate.render(ctext))

def calendar(request):
    tplate = template.loader.get_template('elts/base.html')
    ctext = template.RequestContext(
        request,
        {
            'title': 'calendar',
            'body': 'body',
        }
    )
    return http.HttpResponse(tplate.render(ctext))

def item(request):
    tplate = template.loader.get_template('elts/base.html')
    ctext = template.RequestContext(
        request,
        {
            'title': 'item',
            'body': 'body',
        }
    )
    return http.HttpResponse(tplate.render(ctext))

def reservation(request):
    tplate = template.loader.get_template('elts/base.html')
    ctext = template.RequestContext(
        request,
        {
            'title': 'reservation',
            'body': 'body',
        }
    )
    return http.HttpResponse(tplate.render(ctext))

def lend(request):
    tplate = template.loader.get_template('elts/base.html')
    ctext = template.RequestContext(
        request,
        {
            'title': 'lend',
            'body': 'body',
        }
    )
    return http.HttpResponse(tplate.render(ctext))

def tag(request):
    tplate = template.loader.get_template('elts/base.html')
    ctext = template.RequestContext(
        request,
        {
            'title': 'tag',
            'body': 'body',
        }
    )
    return http.HttpResponse(tplate.render(ctext))
