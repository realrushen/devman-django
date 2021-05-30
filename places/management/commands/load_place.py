"""
This django-admin command developed only for loading places with data structure listed in .gitbook/data/exaple.json
"""
from io import BytesIO
from typing import List
from urllib import parse

import requests
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.core.validators import URLValidator

from places.models import Place, Photo, MapPoint

class Command(BaseCommand):
    """
    TODO: Documentation
    TODO: Loading data from directory stored on OS
    """

    help = 'Loads place on site. It downloads json files and images from network.'

    def add_arguments(self, parser):
        parser.add_argument('json_url', nargs='+', type=str, help='one or multiple URLs to JSON file with place data')

    def handle(self, *args, **options):
        validator = URLValidator(message='Invalid URL')
        urls = options['json_url']
        self.stdout.write(self.style.SQL_TABLE(f'Starting loading data for {len(urls)} place(s)'))
        self._validate_urls(urls, validator)
        self._load_places(urls)

    def _validate_urls(self, input: List[str], validator: URLValidator):
        """Chaks if input is valid urls"""
        errors = []
        for url in input:
            try:
                validator(url)
            except ValidationError as e:
                errors.append(f'{e.message}: {url}')
        if errors:
            raise CommandError(', '.join(errors))

    def _load_photos(self, place, photos):
        """Loads photos for place"""
        skipped = 0
        for position, photo_url in enumerate(photos, start=1):
            photo_filename = self._extract_filename_from_url(photo_url)
            photo, created = Photo.objects.get_or_create(for_place=place, ordering_position=position)
            if created:
                response = requests.get(photo_url)
                if response.status_code == requests.codes.OK:
                    photo_content = BytesIO(response.content)
                    photo.image.save(photo_filename, photo_content, save=True)
                else:
                    self.stderr.write(f'Failed to load {photo_url} HTTP_RESPONSE_CODE: {response.status_code}')
            else:
                skipped += 1
        else:
            photos_loaded = position - skipped
            self.stdout.write(
                self.style.WARNING(f'{photos_loaded} photo(s) loaded for place {place}, {skipped} skipped'))

    def _load_places(self, urls: str):
        """Loads jsons with places data from network and insert it to database"""
        for url in urls:
            self.stdout.write(self.style.SQL_KEYWORD(f'Starting loading {url}'))
            response = requests.get(url)
            if response.status_code == requests.codes.OK:
                place_data: dict = response.json()
                photos = place_data.pop('imgs')
                coordinates = place_data.pop('coordinates')
                point, created = MapPoint.objects.get_or_create(latitude=coordinates['lat'],
                                                                longitude=coordinates['lng'])
                if not created:
                    self.stdout.write(self.style.MIGRATE_HEADING(f'Point: {point} already exists'))
                place, created = Place.objects.get_or_create(coordinates=point, **place_data)
                if not created:
                    self.stdout.write(self.style.MIGRATE_HEADING(f'Place: {place} already exists'))
                self._load_photos(place, photos)
            else:
                self.stderr.write(f'Failed to load {url} HTTP_RESPONSE_CODE: {response.status_code}')

    @staticmethod
    def _extract_filename_from_url(url):
        return parse.urlparse(url).path.split('/')[-1]
