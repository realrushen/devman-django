from decimal import Decimal
from typing import List, Tuple

from pydantic import BaseModel


class Point(BaseModel):
    type = 'Point'
    coordinates: Tuple[Decimal, Decimal]


class Properties(BaseModel):
    title: str
    place_id: int
    details_url: str

    class Config:
        fields = {
            'place_id': 'placeId',
            'details_url': 'detailsUrl'
        }
        allow_population_by_field_name = True


class Feature(BaseModel):
    type = 'Feature'
    geometry: Point
    properties: Properties


class FeatureCollection(BaseModel):
    type = 'FeatureCollection'
    features: List[Feature] = []


def generate_point_feature(longitude: Decimal, latitude: Decimal, properties: dict):
    """Returning feature in GeoJSON format"""
    point = Point(coordinates=(longitude, latitude))
    point_properties = Properties(
        title=properties.get('title'),
        place_id=properties.get('placeId'),
        details_url=properties.get('detailsUrl'),
    )
    feature = Feature(geometry=point, properties=point_properties)
    return feature


def get_empty_feature_collection():
    return FeatureCollection()
