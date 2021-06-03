# Generated by Django 3.2.3 on 2021-05-17 20:23

from django.db import migrations, models
import django.db.models.deletion
import places.models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0002_auto_20210512_1843'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='photo',
            options={'ordering': ['ordering_position'], 'verbose_name': 'Фото', 'verbose_name_plural': 'Фото'},
        ),
        migrations.AlterField(
            model_name='photo',
            name='for_place',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='places.place', verbose_name='место'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.ImageField(upload_to=places.models.generate_place_directory, verbose_name='Загрузка картинки'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='ordering_position',
            field=models.PositiveSmallIntegerField(verbose_name='Позиция'),
        ),
        migrations.AlterUniqueTogether(
            name='photo',
            unique_together=set(),
        ),
    ]
