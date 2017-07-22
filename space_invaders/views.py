import json
import logging
from datetime import datetime
from django.http import HttpResponse
from django.template import loader
from rest_framework.decorators import api_view
from modules.accio import accio_space_data, accio_image_data

__author__ = "hemil"
logger = logging.getLogger("space")


@api_view(["GET"])
def index(request):
    try:
        space_data = accio_space_data()
        astronauts_data = accio_image_data(space_data[0].json().get("people"))
        context = {
            "astronauts_data": astronauts_data,
            "iss_data": space_data[1].json()
        }
        context["iss_data"]["timestamp"] = str(datetime.utcfromtimestamp(context["iss_data"]["timestamp"]))

        template = loader.get_template('index.html')
        return HttpResponse(template.render(context, request))
    except Exception as e:
        logger.error("Exception. 500. cause: {e}".format(e=str(e)))
        response = HttpResponse(json.dumps({
            'status': 0,
            'message': "The Google Key Limit has been exceeded. Please drop a mail to hemil.sha@gmail.com to refresh "
                       "them.",
            'error_code': 500,
            'data': None
        }), content_type="application/json", status=500)
    return response


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def ping(request):
    try:
        return HttpResponse(data="Invasion is on.", status=200, data_count=1)
    except Exception as e:
        return HttpResponse(json.dumps({
            'status': 0,
            'message': "Exception: {e}".format(e=e),
            'error_code': 500,
            'data': None
        }), content_type="application/json", status=500)
