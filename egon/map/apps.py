from django.apps import AppConfig


class MapConfig(AppConfig):
    name = "egon.map"

    def ready(self):
        # pylint: disable=C0415
        from django_mapengine import mvt, registry, layers

        # pylint: disable=C0415
        from . import models, map_config

        registry.mvt_registry.register(
            "municipality",
            [
                mvt.MVTLayer("municipality", models.Municipality.vector_tiles),
                mvt.MVTLayer("municipalitylabel", models.Municipality.label_tiles),
            ],
        )
        registry.mvt_registry.register(
            "static",
            [
                mvt.MVTLayer("potential_wind", models.SupplyPotentialWind.vector_tiles),
                mvt.MVTLayer("potential_pv", models.SupplyPotentialPVGround.vector_tiles),
                mvt.MVTLayer("ehv_hv_station", models.EHVHVSubstation.vector_tiles),
                mvt.MVTLayer("hv_mv_station", models.HVMVSubstation.vector_tiles),
            ],
        )
        registry.mvt_registry.register("results", [mvt.MVTLayer("results", models.Municipality.vector_tiles)])

        for name, layer in map_config.STATIC_LAYERS.items():
            if isinstance(layer, layers.ClusterModelLayer):
                registry.cluster_registry.register(name, layer.model)
