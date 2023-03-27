"""Actual map setup is done here."""

from django_mapengine import legend


LEGEND = {
    "generation": [
        legend.LegendLayer("Biomasse", "", layer_id="supply_biomass"),
        legend.LegendLayer("Hydro", "", layer_id="supply_run_of_river"),
        legend.LegendLayer("Wind Onshore", "", layer_id="supply_wind"),
        legend.LegendLayer("Solar", "", layer_id="supply_solar"),
        legend.LegendLayer("Potential Wind", "", layer_id="potential_wind"),
        legend.LegendLayer("Potential PV", "", layer_id="potential_pv"),
    ],
    "grid": [
        legend.LegendLayer("EHV Line", "", layer_id="ehv_line"),
        legend.LegendLayer("HV Line", "", layer_id="hv_line"),
        legend.LegendLayer("EHV/HV Stations", "", layer_id="ehv_hv_station"),
        legend.LegendLayer("HV/MV Stations", "", layer_id="hv_mv_station"),
    ],
}
