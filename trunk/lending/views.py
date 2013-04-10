from django import http, template

def index(request):
    tplate = template.loader.get_template('lending/base.html')
    ctext = template.RequestContext(
        request,
        {
            'title': 'some random title',
            'body': 'body for file',
        }
    )
    return http.HttpResponse(tplate.render(ctext))
