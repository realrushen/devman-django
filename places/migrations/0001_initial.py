# Generated by Django 3.2.2 on 2021-05-11 18:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MapPoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('longitude', models.DecimalField(decimal_places=15, max_digits=17, verbose_name='Долгота')),
                ('latitude', models.DecimalField(decimal_places=15, max_digits=18, verbose_name='Широта')),
            ],
            options={
                'verbose_name': 'Точка на карте',
                'verbose_name_plural': 'Точки на карте',
                'unique_together': {('longitude', 'latitude')},
                'index_together': {('longitude', 'latitude')},
            },
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=50, verbose_name='Название места')),
                ('description_short', models.CharField(max_length=255, verbose_name='Короткое описание')),
                ('description_long', models.TextField(verbose_name='Подробное описание')),
                ('coordinates', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='places', to='places.mappoint', verbose_name='координаты места')),
            ],
            options={
                'verbose_name': 'Интересное место',
                'verbose_name_plural': 'Интересные места',
            },
        ),
    ]
