from copy import deepcopy
from itertools import cycle

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
details_url_mock = cycle(('./static/places/moscow_legends.json', './static/places/roofs24.json'))


def generate_point_feature(longitude, latitude, properties: dict):
    feature = deepcopy(GEO_JSON_POINT_FEATURE_TEMPLATE)

    feature['geometry']['coordinates'].append(longitude)
    feature['geometry']['coordinates'].append(latitude)

    feature['properties']['title'] = properties.get('title')
    feature['properties']['placeId'] = properties.get('placeId')
    feature['properties']['detailsUrl'] = next(details_url_mock)

    return feature


def get_geo_json_template():
    return deepcopy(GEO_JSON_TEMPLATE)


def add_feature_to_geo_json(geo_json, feature):
    geo_json['features'].append(feature)
