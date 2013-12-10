from dajaxice.decorators import dajaxice_register
import json

@dajaxice_register
def sayhello(request, arg):
    return json.dumps({'message': 'Message: {}'.format(arg)})
