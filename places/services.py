from copy import deepcopy

from django.urls import reverse

GEO_JSON_POINT_FEATURE_TEMPLATE = {
    'type': 'Feature',
    'geometry': {
        'type': 'Point',
        'coordinates': []
    },
    'properties': {}
}
GEO_JSON_TEMPLATE = {
    'type': 'FeatureCollection',
    'features': []
}


def generate_point_feature(longitude, latitude, properties: dict):
    feature = deepcopy(GEO_JSON_POINT_FEATURE_TEMPLATE)
    place_id = properties.get('placeId')
    feature['geometry']['coordinates'].append(longitude)
    feature['geometry']['coordinates'].append(latitude)

    feature['properties']['title'] = properties.get('title')
    feature['properties']['placeId'] = place_id
    feature['properties']['detailsUrl'] = reverse('place-detail', args=[place_id])

    return feature


def get_geo_json_template():
    return deepcopy(GEO_JSON_TEMPLATE)


def add_feature_to_geo_json(geo_json, feature):
    geo_json['features'].append(feature)
