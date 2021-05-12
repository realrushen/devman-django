from django.contrib import admin

from places.models import Place, MapPoint, Photo


class PlaceInline(admin.StackedInline):
    model = Place
    extra = 1


class PhotoInline(admin.StackedInline):
    model = Photo
    extra = 2


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    inlines = [
        PhotoInline
    ]


@admin.register(MapPoint)
class MapPointAdmin(admin.ModelAdmin):
    inlines = [
        PlaceInline
    ]


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass
