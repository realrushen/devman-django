from io import BytesIO
from typing import List
from urllib import parse

import requests
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.core.validators import URLValidator

from places.models import Place, Photo, MapPoint

# This django-admin command developed only for loading places with data structure listed below

PLACE_DATA_EXAMPLE = {
    "title": "Антикафе Bizone",
    "imgs": [
        "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/1f09226ae0edf23d20708b4fcc498ffd.jpg",
        "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/6e1c15fd7723e04e73985486c441e061.jpg",
        "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/be067a44fb19342c562e9ffd815c4215.jpg",
        "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/f6148bf3acf5328347f2762a1a674620.jpg",
        "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/b896253e3b4f092cff47a02885450b5c.jpg",
        "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/605da4a5bc8fd9a748526bef3b02120f.jpg"
    ],
    "description_short": "Настольные и компьютерные игры, виртуальная реальность и насыщенная программа мероприятий — новое антикафе Bizone предлагает два уровня удовольствий для вашего уединённого отдыха или радостных встреч с родными, друзьями, коллегами.",
    "description_long": "<p>Рядом со станцией метро «Войковская» открылось антикафе Bizone, в котором создание качественного отдыха стало делом жизни для всей команды. Создатели разделили пространство на две зоны, одна из которых доступна для всех посетителей, вторая — только для совершеннолетних гостей.</p><p>В Bizone вы платите исключительно за время посещения. В стоимость уже включены напитки, сладкие угощения, библиотека комиксов, большая коллекция популярных настольных и видеоигр. Также вы можете арендовать ВИП-зал для большой компании и погрузиться в мир виртуальной реальности с помощью специальных очков от топового производителя.</p><p>В течение недели организаторы проводят разнообразные встречи для меломанов и киноманов. Также можно присоединиться к английскому разговорному клубу или посетить образовательные лекции и мастер-классы. Летом организаторы запускают марафон настольных игр. Каждый день единомышленники собираются, чтобы порубиться в «Мафию», «Имаджинариум», Codenames, «Манчкин», Ticket to ride, «БЭНГ!» или «Колонизаторов». Точное расписание игр ищите в группе антикафе <a class=\"external-link\" href=\"https://vk.com/anticafebizone\" target=\"_blank\">«ВКонтакте»</a>.</p><p>Узнать больше об антикафе Bizone и забронировать стол вы можете <a class=\"external-link\" href=\"http://vbizone.ru/\" target=\"_blank\">на сайте</a> и <a class=\"external-link\" href=\"https://www.instagram.com/anticafe.bi.zone/\" target=\"_blank\">в Instagram</a>.</p>",
    "coordinates": {
        "lng": "37.50169",
        "lat": "55.816591"
    }
}


class Command(BaseCommand):
    """TODO: Documentation"""

    help = 'Loads place on site'

    def add_arguments(self, parser):
        parser.add_argument('json_url', nargs='+', type=str, help='URL to JSON file with place data')

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

    def _extract_filename_from_url(self, url):
        return parse.urlparse(url).path.split('/')[-1]