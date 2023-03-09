from egon.map import models
from egon.map.mvt import MVTLayer

REGION_MVT_LAYERS = {
    "country": [
        MVTLayer("country", models.Country.vector_tiles),
        MVTLayer("countrylabel", models.Country.label_tiles),
    ],
    "state": [
        MVTLayer("state", models.State.vector_tiles),
        MVTLayer("statelabel", models.State.label_tiles),
    ],
    "district": [
        MVTLayer("district", models.District.vector_tiles),
        MVTLayer("districtlabel", models.District.label_tiles),
    ],
    "municipality": [
        MVTLayer("municipality", models.Municipality.vector_tiles),
        MVTLayer("municipalitylabel", models.Municipality.label_tiles),
    ],
}

STATIC_MVT_LAYERS = {
    "static": [
        MVTLayer("demand_cts", models.DemandCts.vector_tiles),
        MVTLayer("demand_household", models.DemandHousehold.vector_tiles),
        MVTLayer("supply_biomass", models.SupplyBiomass.vector_tiles),
        MVTLayer("supply_run_of_river", models.SupplyRunOfRiver.vector_tiles),
        MVTLayer("supply_wind", models.SupplyWindOnshore.vector_tiles),
        MVTLayer("supply_solar", models.SupplySolarGround.vector_tiles),
        MVTLayer("potential_wind", models.SupplyPotentialWind.vector_tiles),
        MVTLayer("potential_pv", models.SupplyPotentialPVGround.vector_tiles),
        MVTLayer("ehv_line", models.EHVLine.vector_tiles),
        MVTLayer("hv_line", models.HVLine.vector_tiles),
        MVTLayer("ehv_hv_station", models.EHVHVSubstation.vector_tiles),
        MVTLayer("hv_mv_station", models.HVMVSubstation.vector_tiles),
        MVTLayer("mv_grid_districts", models.MVGridDistricts.vector_tiles),
    ]
}

DYNAMIC_MVT_LAYERS = {}

MVT_LAYERS = dict(**REGION_MVT_LAYERS, **STATIC_MVT_LAYERS, **DYNAMIC_MVT_LAYERS)
DISTILL_MVT_LAYERS = dict(**REGION_MVT_LAYERS, **STATIC_MVT_LAYERS)
