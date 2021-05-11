from django.db import models

class Place(models.Model):
    """
    Модель интересного места на карте
    """
    title = models.CharField('Название места', max_length=50, db_index=True)
    description_short = models.CharField('Короткое описание', max_length=255)
    description_long = models.TextField('Подробное описание')
    coordinates = models.ForeignKey('MapPoint', related_name='places', on_delete=models.PROTECT,
                                    verbose_name='координаты места')

    class Meta:
        verbose_name = 'Интересное место'
        verbose_name_plural = 'Интересные места'

    def __str__(self):
        return f'{self.title} {self.coordinates}'


class MapPoint(models.Model):
    """Модель координат точки на карте"""
    longitude = models.DecimalField('Долгота', max_digits=16, decimal_places=14)
    latitude = models.DecimalField('Широта', max_digits=16, decimal_places=14)

    class Meta:
        verbose_name = 'Точка на карте'
        verbose_name_plural = 'Точки на карте'
        unique_together = [['longitude', 'latitude']]
        index_together = [['longitude', 'latitude']]

    def __str__(self):
        return f'({self.longitude}, {self.latitude})'


