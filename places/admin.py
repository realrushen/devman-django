from django.contrib import admin

from places.models import Place, MapPoint, Photo


class PlaceInline(admin.StackedInline):
    model = Place
    extra = 1


class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 2
    fields = ['image', 'preview_image', 'ordering_position']

    readonly_fields = ['preview_image']


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ['title', 'coordinates']
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
    list_display = ['for_place', 'preview_image', 'image']
    readonly_fields = ['preview_image']
