from django.contrib import admin

from places.models import Place, MapPoint


class PlaceInline(admin.StackedInline):
    model = Place
    extra = 1


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    pass


@admin.register(MapPoint)
class MapPointAdmin(admin.ModelAdmin):
    inlines = [
        PlaceInline
    ]
