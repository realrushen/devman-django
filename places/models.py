from django.db import models, IntegrityError, transaction
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from tinymce import models as tinymce_models

from places.translit import slugify


def generate_place_directory(instance, filename):
    directory_name = instance.for_place.upload_dir
    return f'{directory_name}/{filename}'


class Place(models.Model):
    """Interesting place on map model"""

    title = models.CharField(
        'Название места',
        max_length=50,
        db_index=True
    )
    description_short = models.TextField(
        'Короткое описание',
        blank=True
    )
    description_long = tinymce_models.HTMLField(
        'Подробное описание',
        blank=True
    )
    coordinates = models.ForeignKey(
        'MapPoint',
        related_name='places',
        on_delete=models.PROTECT,
        verbose_name='координаты места',
        db_index=True
    )
    _upload_dir = models.CharField(
        max_length=100,
        editable=False,
        blank=True,
        default='',
        unique=True
    )

    class Meta:
        verbose_name = 'Интересное место'
        verbose_name_plural = 'Интересные места'
        unique_together = [['title', 'coordinates']]

    def __str__(self):
        return f'{self.title}'

    @property
    def upload_dir(self):
        if not self._upload_dir:
            dir_name = slugify(self.title)
            self._upload_dir = dir_name
            try:
                with transaction.atomic():
                    self.save(update_fields=('_upload_dir',))
            # modify name of upload_dir if it already exists
            except IntegrityError:
                self._upload_dir = f'{dir_name}_{self.coordinates}'
                self.save(update_fields=('_upload_dir',))
        return self._upload_dir


class MapPoint(models.Model):
    """Model of place coordinates on map"""
    longitude = models.DecimalField(
        'Долгота',
        max_digits=16,
        decimal_places=14
    )
    latitude = models.DecimalField(
        'Широта',
        max_digits=16,
        decimal_places=14
    )

    class Meta:
        verbose_name = 'Точка на карте'
        verbose_name_plural = 'Точки на карте'
        unique_together = [['longitude', 'latitude']]
        index_together = [['longitude', 'latitude']]

    def __str__(self):
        return f'({self.longitude}, {self.latitude})'


class Photo(models.Model):
    """Photo of interesting place"""
    image = models.ImageField(
        'Загрузка картинки',
        upload_to=generate_place_directory
    )
    ordering_position = models.PositiveSmallIntegerField(
        'Позиция',
        blank=True
    )
    for_place = models.ForeignKey(
        Place,
        verbose_name='место',
        related_name='photos',
        on_delete=models.CASCADE,
        db_index=True
    )

    class Meta:
        ordering = ['ordering_position']
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'

    def __str__(self):
        return f'Фото (ID {self.pk})'

    def preview_image(self):
        """Custom method to display Image in admin panel"""
        return format_html(
            '<img src="{url}" height=150 />',
            url=mark_safe(self.image.url)
        )

    preview_image.short_description = 'Фото'
