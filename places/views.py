from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from places.models import Place
from places.services import generate_point_feature, get_geo_json_template, add_feature_to_geo_json


def index(request):
    """
    Пример GeoJSON который должен отдавать view
    {
      "type": "FeatureCollection",
      "features": [
        {
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [37.62, 55.793676]
          },
          "properties": {
            "title": "«Легенды Москвы",
            "placeId": "moscow_legends",
            "detailsUrl": "./static/places/moscow_legends.json"
          }
        },
        {
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [37.64, 55.753676]
          },
          "properties": {
            "title": "Крыши24.рф",
            "placeId": "roofs24",
            "detailsUrl": "./static/places/roofs24.json"
          }
        }
      ]
    }
    """
    places = Place.objects.select_related('coordinates').all()
    geo_json_points = get_geo_json_template()

    for place in places:
        longitude = str(place.coordinates.longitude)
        latitude = str(place.coordinates.latitude)
        properties = {
            'title': place.title,
            'placeId': place.id,
            'detailsUrl': ''
        }
        geo_feature = generate_point_feature(longitude, latitude, properties)
        add_feature_to_geo_json(geo_json_points, geo_feature)

    return render(request, context={'geo_data': geo_json_points}, template_name='places/index.html')


def place_view(request, id):
    place = get_object_or_404(Place, pk=id)
    return HttpResponse(place.title)
