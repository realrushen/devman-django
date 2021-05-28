from django.db import models
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from tinymce import models as tinymce_models

from places.utils import slugify


def concrete_place_directory(instance, filename):
    directory_name = instance.for_place.upload_dir
    return f'{directory_name}/{filename}'


class Place(models.Model):
    """Interesting place on map model"""

    title = models.CharField('Название места', max_length=50, db_index=True)
    description_short = models.CharField('Короткое описание', max_length=500)
    description_long = tinymce_models.HTMLField('Подробное описание')
    coordinates = models.ForeignKey('MapPoint', related_name='places', on_delete=models.PROTECT,
                                    verbose_name='координаты места')
    slug = models.CharField(max_length=100, editable=False, null=True, default=None)

    class Meta:
        verbose_name = 'Интересное место'
        verbose_name_plural = 'Интересные места'

    def __str__(self):
        return f'{self.title}'

    @property
    def upload_dir(self):
        if not self.slug:
            dir_name = slugify(self.title)
            self.slug = dir_name
            self.save(update_fields=('slug',))
        return self.slug


class MapPoint(models.Model):
    """Model of place coordinates on map"""
    longitude = models.DecimalField('Долгота', max_digits=16, decimal_places=14)
    latitude = models.DecimalField('Широта', max_digits=16, decimal_places=14)

    class Meta:
        verbose_name = 'Точка на карте'
        verbose_name_plural = 'Точки на карте'
        unique_together = [['longitude', 'latitude']]
        index_together = [['longitude', 'latitude']]

    def __str__(self):
        return f'({self.longitude}, {self.latitude})'


class Photo(models.Model):
    """Photo of interesting place"""
    image = models.ImageField('Загрузка картинки', upload_to=concrete_place_directory)
    ordering_position = models.PositiveSmallIntegerField('Позиция')
    for_place = models.ForeignKey(Place, verbose_name='место', related_name='photos', on_delete=models.CASCADE)

    class Meta:
        ordering = ['ordering_position']
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'

    def __str__(self):
        return f'Фото (ID {self.pk})'

    def preview_image(self):
        """Custom method to display Image in admin panel"""
        return format_html('<img src="{url}" height=150 />',
                           url=mark_safe(self.image.url))

    preview_image.short_description = 'Фото'
