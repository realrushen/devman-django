# Generated by Django 3.2.3 on 2021-05-24 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0005_auto_20210517_2116'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='upload_dir',
            field=models.CharField(blank=True, default=None, editable=False, max_length=50, null=True, verbose_name='Директория для загрузок'),
        ),
    ]