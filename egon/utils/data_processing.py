import os

from django.contrib.gis.utils import LayerMapping

from config.settings.base import DATA_DIR
from egon.map import models

REGIONS = [
    models.Country,
    models.State,
    models.District,
    models.Municipality,
]

MODELS = [
    # models.CentralHeatPumps100RE,  # empty
    models.CH4Voronoi100RE,
    models.EHVHVSubstation100RE,
    models.EHVLine100RE,
    models.FlexPotElDynamicLineRating100RE,
    models.GasCH4Industry100RE,
    models.GasH2Industry100RE,
    models.GasPotentialBiogasProduction100RE,
    models.H2Voronoi100RE,
    # models.HeatGeothermal100RE, # empty
    models.HeatingHouseholdsCts100RE,
    # models.HeatSolarthermal100RE, # empty
    models.HVLine100RE,
    models.HVMVSubstation100RE,
    models.LoadArea100RE,
    models.MethaneGridLine100RE,
    models.MVGridDistrictData100RE,
    models.PotentialCH4Stores100RE,
    models.PotentialH2UndergroundStorage100RE,
    models.PVGroundMountedPotentialAreaAgriculture100RE,
    models.PVGroundMountedPotentialAreaHighways_Railroads100RE,
    models.PVGroundMountedPVPlant100RE,
    models.PVRoofTopPVPlant100RE,
    models.TransportHeavyDuty100RE,
    models.WindOffshoreWindPark100RE,
    models.WindOnshorePotentialArea100RE,
    models.WindOnshoreWindPark100RE,
    # egon2035 scenario
    models.CentralHeatPumps,
    models.CH4Voronoi,
    models.EHVHVSubstation,
    models.EHVLine,
    models.FlexPotElDynamicLineRating,
    models.GasCH4Industry,
    models.GasH2Industry,
    models.GasPotentialBiogasProduction,
    models.GasPotentialNaturalGasProduction,
    models.H2Voronoi,
    models.HeatGeothermal,
    models.HeatingHouseholdsCts,
    models.HeatSolarthermal,
    models.HVLine,
    models.HVMVSubstation,
    models.LoadArea,
    models.MethaneGridLine,
    models.MVGridDistrictData,
    models.PotentialCH4Stores,
    models.PotentialH2UndergroundStorage,
    models.PVGroundMountedPotentialAreaAgriculture,
    models.PVGroundMountedPotentialAreaHighways_Railroads,
    models.PVGroundMountedPVPlant,
    models.PVRoofTopPVPlant,
    models.TransportHeavyDuty,
    models.WindOffshoreWindPark,
    models.WindOnshorePotentialArea,
    models.WindOnshoreWindPark,
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
        instance = LayerMapping(
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
        instance = LayerMapping(
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
