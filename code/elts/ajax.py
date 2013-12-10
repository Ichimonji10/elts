from dajaxice.decorators import dajaxice_register
import json

@dajaxice_register
def sayhello(request):
    return json.dumps({'message': 'Hello World'})
