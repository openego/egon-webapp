import fiona
from osgeo import gdal, ogr
import geopandas as gpd
import os


def check_geopackage(gpkg_path):
    try:
        # Öffne das GeoPackage mit GDAL
        gpkg_dataset = gdal.OpenEx(gpkg_path, gdal.OF_VECTOR)

        # Überprüfe, ob das GeoPackage erfolgreich geöffnet wurde
        if gpkg_dataset is None:
            print("Das GeoPackage konnte nicht geöffnet werden.")
            return

        # Lese die Anzahl der Layer im GeoPackage
        num_layers = gpkg_dataset.GetLayerCount()
        print(f"Anzahl der Layer im GeoPackage: {num_layers}")

        # Lese die Informationen für jeden Layer
        for i in range(num_layers):
            layer = gpkg_dataset.GetLayerByIndex(i)
            layer_name = layer.GetName()
            feature_count = layer.GetFeatureCount()
            spatial_ref = layer.GetSpatialRef()

            print(f"Layer {i+1}:")
            print(f"Name: {layer_name}")
            print(f"Anzahl der Features: {feature_count}")
            print(f"Raumbezugssystem: {spatial_ref.ExportToWkt()}")

            # Zusätzliche Informationen
            extent = layer.GetExtent()
            min_x, max_x, min_y, max_y = extent
            print(f"Minimale X-Koordinate: {min_x}")
            print(f"Maximale X-Koordinate: {max_x}")
            print(f"Minimale Y-Koordinate: {min_y}")
            print(f"Maximale Y-Koordinate: {max_y}")

            # Überprüfe, ob der Layer geometrische Informationen enthält
            if layer.GetGeomType() != ogr.wkbNone:
                print("Der Layer enthält geometrische Informationen.")
                # Lese den Geometrietyp des Layers
                geom_type = ogr.GeometryTypeToName(layer.GetGeomType())
                print(f"Geometrietyp: {geom_type}")

            # Überprüfe, ob der Layer Attributtabelle enthält
            if layer.GetLayerDefn().GetFieldCount() > 0:
                print("Der Layer enthält eine Attributtabelle.")
                # Lese die Anzahl der Attribute in der Tabelle
                num_fields = layer.GetLayerDefn().GetFieldCount()
                print(f"Anzahl der Attribute: {num_fields}")

                # Lese die Namen der Attribute
                field_names = [
                    layer.GetLayerDefn().GetFieldDefn(i).GetName()
                    for i in range(num_fields)
                ]
                print(f"Attributnamen: {field_names}")

            print("-----------------------------------")

        # Schließe das GeoPackage
        gpkg_dataset = None
        print("GeoPackage wurde erfolgreich überprüft.\n")

    except Exception as e:
        print(f"Fehler beim Überprüfen des GeoPackages: {str(e)}\n")


def check_geopackage_geopandas(gpkg_path, output_path):
    try:
        # Open the GeoPackage with GDAL
        gpkg_dataset = gdal.OpenEx(gpkg_path, gdal.OF_VECTOR)

        # Check if the GeoPackage was successfully opened
        if gpkg_dataset is None:
            print("The GeoPackage could not be opened.")
            return

        # Read the GeoPackage using GeoPandas
        gdf = gpd.read_file(gpkg_path)

        # Print the GeoDataFrame information
        print("GeoDataFrame information:")
        print(gdf.info())
        print(gdf.crs)

        # Export the GeoDataFrame as a GeoPackage
        output_csv_path = "check_gdf/" + output_path
        gdf.to_csv(f"{output_csv_path}")
        print(f"GeoDataFrame exported to {output_csv_path}.")

        # Close the GeoPackage
        gpkg_dataset = None
        print("GeoPackage was successfully checked.\n")

    except Exception as e:
        print(f"Error while checking the GeoPackage: {str(e)}\n")


# # Lese das GeoPackage mit geopandas ein
# geodf = gpd.read_file(
#     gpkg_path, layer=0
# )  # Annahme: Der Layer, den du bearbeiten möchtest, hat den Index 0

# # Iteriere über alle Features im geopandas DataFrame
# for index, row in geodf.iterrows():
#     # Hol dir den aktuell zugewiesenen Geometrietyp
#     geom_type = row.geometry.geom_type

#     # Wenn der Geometrietyp "Unknown" ist, ändere ihn zu "MultiPolygon"
#     if geom_type == "GEOMETRY":
#         geodf.at[index, "geometry"] = row.geometry.buffer(
#             0
#         )  # Ändere den Geometrietyp auf "MultiPolygon"

# # Schreibe das aktualisierte DataFrame zurück in das GeoPackage
# geodf.to_file(gpkg_path, driver="GPKG", layer=0)

# # Öffne das GeoPackage im Update-Modus
# geopackage = ogr.Open(geopackage_path, 1)

# # Hol dir den Layer des GeoPackages
# layer = geopackage.GetLayer()

# # Iteriere über alle Features im Layer
# for feature in layer:
#     # Hol dir den aktuell zugewiesenen Geometrietyp
#     geom_type = feature.GetGeometryRef().GetGeometryType()

#     # Wenn der Geometrietyp "Unknown" ist, ändere ihn zu "MultiPolygon"
#     if geom_type == ogr.wkbUnknown:
#         new_geom = ogr.Geometry(ogr.wkbMultiPolygon)
#         new_geom.AddGeometry(feature.GetGeometryRef())
#         feature.SetGeometry(new_geom)
#         layer.SetFeature(feature)

# # Schließe das GeoPackage
# geopackage = None


# Open the GeoPackage
driver = ogr.GetDriverByName("GPKG")
geopackage = driver.Open(
    "gpkgs/1_Demand/egon100re.demand.gas_methane_for_industry.gpkg", 1
)

# Get the original layer by name
layer_name = "egon100re.demand.gas_methane_for_industry"
original_layer = geopackage.GetLayerByName(layer_name)

# Create a new layer with the desired geometry type
new_layer_name = "egon100re.demand.gas_methane_for_industry"
new_layer = geopackage.CreateLayer(
    new_layer_name, geom_type=ogr.wkbMultiPolygon, options=["OVERWRITE=YES"]
)

# Copy the fields from the original layer to the new layer
original_layer_defn = original_layer.GetLayerDefn()
for i in range(original_layer_defn.GetFieldCount()):
    field_defn = original_layer_defn.GetFieldDefn(i)
    if new_layer.CreateField(field_defn) != 0:
        print("Error creating field: {}".format(field_defn.GetName()))

# Copy the features from the original layer to the new layer
for feature in original_layer:
    new_feature = ogr.Feature(new_layer.GetLayerDefn())
    new_feature.SetGeometry(feature.GetGeometryRef().Clone())
    for i in range(feature.GetFieldCount()):
        new_feature.SetField(i, feature.GetField(i))
    if new_layer.CreateFeature(new_feature) != 0:
        print("Error creating feature")
    new_feature = None

# Close the GeoPackage
geopackage = None
