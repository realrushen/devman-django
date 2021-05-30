from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from places.models import Place
from places.services import generate_point_feature, get_empty_feature_collection


def index(request):
    """
    Main page view
    """
    places = Place.objects.select_related('coordinates').all()
    geo_json_points = get_empty_feature_collection()

    for place in places:
        longitude = str(place.coordinates.longitude)
        latitude = str(place.coordinates.latitude)
        properties = {
            'title': place.title,
            'placeId': place.id,
            'detailsUrl': reverse('place-detail', args=(place.id,))
        }
        geo_feature = generate_point_feature(longitude, latitude, properties)
        geo_json_points.features.append(geo_feature)

    return render(request, context={'geo_data': geo_json_points.dict(by_alias=True)}, template_name='places/index.html')


def place_view(request, id: int):
    """place detail view"""
    place = get_object_or_404(Place.objects.select_related('coordinates'), pk=id)
    response = {
        'title': place.title,
        'imgs': [photo.image.url for photo in place.photos.all()],
        'description_short': place.description_short,
        'description_long': place.description_long,
        'coordinates': {
            'lat': place.coordinates.latitude,
            'lng': place.coordinates.longitude
        }
    }
    return JsonResponse(data=response, json_dumps_params={'indent': 4, 'ensure_ascii': False})
