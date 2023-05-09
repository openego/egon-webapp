import os

import pandas

from config.settings.base import DATA_DIR
from egon.map import models
from egon.map.models import MVGridDistricts
from egon.utils.ogr_layer_mapping import RelatedModelLayerMapping

REGIONS = [
    models.Country,
    models.State,
    models.District,
    models.Municipality,
]

MODELS = [
    models.MVGridDistrictData,
    models.MVGridDistricts,
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

CSV_MODELS = [models.TransportMitDemand, models.DemandHousehold]


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


def load_csv():
    data_models = CSV_MODELS
    for model in data_models:
        if model.objects.exists():
            print(f"Skipping data for model '{model.__name__}' - Please empty model first if you want to update data.")
            continue
        print(f"Upload data for model '{model.__name__}'")
        if hasattr(model, "data_folder"):
            data_path = os.path.join(DATA_DIR, model.data_folder, f"{model.data_file}.csv")
        else:
            data_path = os.path.join(DATA_DIR, f"{model.data_file}.csv")

        # Read the CSV file into a pandas DataFrame
        dataframe = pandas.read_csv(data_path, sep=",")
        if model == models.TransportMitDemand:
            for index, row in dataframe.iterrows():
                model.objects.create(
                    mv_grid_district=MVGridDistricts.objects.get(id=row["bus_id"]),
                    annual_demand=row["annual_demand"],
                    min=row["min"],
                    max=row["max"],
                )
        if model == models.DemandHousehold:
            for index, row in dataframe.iterrows():
                model.objects.create(
                    mv_grid_district=MVGridDistricts.objects.get(id=row["mv_grid_district_id"]),
                    sum=row["sum"],
                    min=row["min"],
                    max=row["max"],
                )


def empty_data(data_models=None):
    data_models = data_models or MODELS
    for model in data_models:
        model.objects.all().delete()
