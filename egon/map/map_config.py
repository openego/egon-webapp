"""Actual map setup is done here."""

from django.utils.translation import gettext_lazy as _
from django_mapengine import legend

LEGEND = {
    "demand": [
        legend.LegendLayer(
            _("Electricity Households"), "Descriptions", layer_id="egon_demand_electricity_household_2035"
        ),
        legend.LegendLayer(_("Number of electric vehicles"), "", layer_id="transport_mit_number_of_evs_2035_ev_count"),
    ],
    "generation": [
        legend.LegendLayer(_("Biomasse"), "", layer_id="supply_biomass"),
        legend.LegendLayer(_("Hydro"), "", layer_id="supply_run_of_river"),
        legend.LegendLayer(_("Wind Onshore"), "", layer_id="supply_wind"),
        legend.LegendLayer(_("Solar"), "", layer_id="supply_solar"),
        legend.LegendLayer(_("Potential Wind"), "", layer_id="potential_wind"),
        legend.LegendLayer(_("Potential PV"), "", layer_id="potential_pv"),
    ],
    "grid": [
        legend.LegendLayer(_("EHV Line"), "", layer_id="ehv_line"),
        legend.LegendLayer(_("HV Line"), "", layer_id="hv_line"),
        legend.LegendLayer(_("EHV/HV Stations"), "", layer_id="ehv_hv_station"),
        legend.LegendLayer(_("HV/MV Stations"), "", layer_id="hv_mv_station"),
    ],
    "model": [
        legend.LegendLayer(_("MV Grid Districts"), "", layer_id="mv_grid_districts"),
        legend.LegendLayer(_("MV Grid District Data"), "", layer_id="mv_grid_district_data"),
        legend.LegendLayer(_("Municipalities"), "", layer_id="municipality"),
        legend.LegendLayer(_("Districts"), "", layer_id="district"),
        legend.LegendLayer(_("States"), "", layer_id="state"),
    ],
}
