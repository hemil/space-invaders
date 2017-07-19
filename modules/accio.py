import grequests
from django.conf import settings


def accio_space_data():
    space_url = "http://api.open-notify.org/astros.json"
    iss_url = "http://api.open-notify.org/iss-now.json"
    urls = [space_url, iss_url]
    rs = (grequests.get(u) for u in urls)
    space_data = grequests.map(rs)
    return space_data


def accio_image_data(astronauts_data):
    api_key = settings.GOOGLE_API_KEY
    search_id = settings.GOOGLE_SEARCH_ID
    urls = []
    for astronaut in astronauts_data:
        q = astronaut.get("name", "Cartoon") + " astronaut wiki"
        google_url = "https://www.googleapis.com/customsearch/v1?q={q}&cx={search_id}&fileType=jpg&imgSize=large" \
                     "&num=10&key={api_key}".format(q=q, search_id=search_id, api_key=api_key)
        urls.append(google_url)
    rs = (grequests.get(u) for u in urls)
    image_data = grequests.map(rs)
    for astronaut, image in zip(astronauts_data, image_data):
        try:
            print image.json().get("items")[0].get("link")
            # return astronauts_data
            astronaut["image_url"] = image.json().get("items")[0].get("pagemap").get("cse_image")[0].get("src")
        except Exception as e:
            print "EXCEPTION!!!: {e}".format(e=str(e))
            astronaut["image_url"] = "http://bit.ly/2vDf5Mb"
    return astronauts_data
