import os

from config.settings.base import DATA_DIR
from egon.map import models
from egon.utils.ogr_layer_mapping import RelatedModelLayerMapping

REGIONS = [
    models.Country,
    models.State,
    models.District,
    models.Municipality,
]

MODELS = [
    models.MVGridDistrictData,
    models.CH4Voronoi,
    models.H2Voronoi,
    models.SupplyBiomass,
    models.SupplyRunOfRiver,
    models.SupplySolarGround,
    models.SupplyWindOnshore,
    models.SupplyPotentialPVGround,
    models.SupplyPotentialWind,
    models.EHVLine,
    models.EHVHVSubstation,
    models.HVLine,
    models.HVMVSubstation,
]


def load_regions(regions=None, verbose=True):
    regions = regions or REGIONS
    for region in regions:
        if region.objects.exists():
            print(f"Skipping data for model '{region.__name__}' - Please empty model first if you want to update data.")
            continue
        print(f"Upload data for region '{region.__name__}'")
        if hasattr(region, "data_folder"):
            data_path = os.path.join(DATA_DIR, region.data_folder, f"{region.data_file}.gpkg")
        else:
            data_path = os.path.join(DATA_DIR, f"{region.data_file}.gpkg")
        region_model = models.Region(layer_type=region.__name__.lower())
        region_model.save()
        instance = RelatedModelLayerMapping(
            model=region,
            data=data_path,
            mapping=region.mapping,
            layer=region.layer,
            transform=4326,
        )
        instance.region = region_model
        instance.save(strict=True, verbose=verbose)


def load_data(data_models=None, verbose=True):
    data_models = data_models or MODELS
    for model in data_models:
        if model.objects.exists():
            print(f"Skipping data for model '{model.__name__}' - Please empty model first if you want to update data.")
            continue
        print(f"Upload data for model '{model.__name__}'")
        if hasattr(model, "data_folder"):
            data_path = os.path.join(DATA_DIR, model.data_folder, f"{model.data_file}.gpkg")
        else:
            data_path = os.path.join(DATA_DIR, f"{model.data_file}.gpkg")
        instance = RelatedModelLayerMapping(
            model=model,
            data=data_path,
            mapping=model.mapping,
            layer=model.layer,
            transform=4326,
        )
        instance.save(strict=True, verbose=verbose)


def empty_data(data_models=None):
    data_models = data_models or MODELS
    for model in data_models:
        model.objects.all().delete()
