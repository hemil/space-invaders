from datetime import datetime
from django.http import HttpResponse
from django.template import loader
from rest_framework.decorators import api_view
from rest_framework.response import Response
from modules.accio import accio_space_data, accio_image_data

__author__ = "hemil"


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
        response = Response({
            'status': 0,
            'message': str(e),
            'error_code': 500,
            'data': None
        }, status=500)
        return response
#
