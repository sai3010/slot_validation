from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
import json
from .process import *
@api_view(['POST'])
def slot_values(request):
    try:
        body_unicode = request.body.decode('utf-8')
        content = json.loads(body_unicode)
        resp = validate_finite_values_entity(content['values'],content['supported_values'],content['invalid_trigger'],content['key'],content['support_multiple'],content['pick_first'])
        return Response(resp)
    except KeyError as k:
        return Response({"error":str(k),"message":"Key Error"},status=500)
    except Exception as e:
        return Response({"error":str(e),"message":"Server Error"},status=500)

@api_view(['POST'])
def slot_numeric(request):
    try:
        body_unicode = request.body.decode('utf-8')
        content = json.loads(body_unicode)
        resp = validate_numeric_entity(content['values'],content['invalid_trigger'],content['key'],content['support_multiple'],content['pick_first'],content['constraint'],content['var_name'])
        return Response(resp)
    except KeyError as k:
        return Response({"error":str(k),"message":"Key Error"},status=500)
    except Exception as e:
        return Response({"error":str(e),"message":"Server Error"},status=500)