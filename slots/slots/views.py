from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
import json
from .process import *
@api_view(['POST'])
def slot_values(request):
    body_unicode = request.body.decode('utf-8')
    content = json.loads(body_unicode)
    resp = validate_finite_values_entity(content['values'],content['supported_values'],content['invalid_trigger'],content['key'],content['support_multiple'],content['pick_first'])
    return Response(resp)

@api_view(['POST'])
def slot_numeric(request):
    body_unicode = request.body.decode('utf-8')
    content = json.loads(body_unicode)
    resp = validate_numeric_entity(content['values'],content['invalid_trigger'],content['key'],content['support_multiple'],content['pick_first'],content['constraint'],content['var_name'])
    return Response(resp)