from django.urls import path

from . import views

app_name = "map"

urlpatterns = [
    path("", views.MapGLView.as_view(), name="map"),
    path("choropleth/<str:lookup>/<str:scenario>", views.get_choropleth, name="choropleth"),
]
