from django.urls import path

from places.views import place_view

urlpatterns = [
    path('<int:id>/', place_view, name='place-detail'),
    ]
