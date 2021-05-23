from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from django.contrib import admin

from places.models import Place, MapPoint, Photo


class PlaceInline(admin.StackedInline):
    model = Place
    extra = 1


class PhotoInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Photo
    extra = 2
    fields = ['ordering_position', 'image', 'preview_image', ]
    readonly_fields = ['preview_image']


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ['title', 'coordinates']
    inlines = [
        PhotoInline
    ]


@admin.register(MapPoint)
class MapPointAdmin(admin.ModelAdmin):
    list_display = ['longitude', 'latitude', 'places_display']
    inlines = [
        PlaceInline
    ]

    def places_display(self, obj):
        return ", ".join([
            place.title for place in obj.places.all()
        ])

    places_display.short_description = "Места"

