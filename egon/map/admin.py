# Register your models here.

from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import MapLayer, MVGridDistrictData


class MVGridDistrictDataResource(resources.ModelResource):
    class Meta:
        model = MVGridDistrictData


class MVGridDistrictDataAdmin(ImportExportModelAdmin):
    resource_classes = [MVGridDistrictDataResource]


class MVGridDistrictLayerResource(resources.ModelResource):
    class Meta:
        model = MapLayer


class MVGridDistrictLayerAdmin(ImportExportModelAdmin):
    resource_classes = [MVGridDistrictLayerResource]


admin.site.register(MVGridDistrictData, MVGridDistrictDataAdmin)
admin.site.register(MapLayer, MVGridDistrictLayerAdmin)
