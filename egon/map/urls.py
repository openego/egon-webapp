from django.urls import path

from . import views

app_name = "map"

urlpatterns = [
    path("", views.MapGLView.as_view(), name="map"),
]
