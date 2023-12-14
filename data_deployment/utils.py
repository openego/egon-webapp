import geopandas as gpd
import pandas as pd
import psycopg2
import os
import sqlite3


def create_gpkgs(
    df_ods: pd.DataFrame,
    conn: psycopg2.connect,
    egon_scenario: str,
    path: str,
    ignore_query_category_list: list = [],
):
    """
    Creates GeoPackages from SQL queries stored in a Pandas DataFrame.

    Args:
        df_ods (pandas.DataFrame): DataFrame containing the SQL queries and metadata from 'WebApp_scenario_data.ods'.
        conn (psycopg2.connect): database connection to execute the SQL queries.
        egon_scenario (str): eGon scenario name ('2035' or '100RE').
        path (str): directory path where the GeoPackages will be saved.
        ignore_query_category_list (list): (OPTIONAL) list of category names where queries will be skipped.
    
    Returns:
        None

    Raises:
        Exception: If an error occurs while executing a SQL query or creating a GeoPackage.
    """
    if egon_scenario == "2035":
        column = 5
    else:
        column = 6
    print("Querying data and creating geopackages...")

    category_name, subcategory_name = "", ""

    for i, value in enumerate(df_ods.iloc[:, column]):
        if not pd.isna(df_ods.iloc[i, 0]) and df_ods.iloc[i, 0] != category_name:
            category_name = df_ods.iloc[i, 0]
        if (
            isinstance(value, str)
            and (value.lower().startswith("select") or value.lower().startswith("with"))
            and category_name not in ignore_query_category_list
        ):
            subcategory_name = df_ods.iloc[i, 1]
            layer_name = df_ods.iloc[i, 2]
            try:
                query = value
                gpkg_filename = (
                    f"egon{egon_scenario}.{category_name}.{subcategory_name}_{layer_name}".replace(
                        "/", "_"
                    )
                    .replace(" ", "_")
                    .replace("-_", "")
                    .replace("(", "")
                    .replace(")", "")
                    .lower()
                )
                gpkg_file_path = f"{path}/{category_name}/{gpkg_filename}.gpkg"
                # Create directory if it does not exist
                os.makedirs(os.path.dirname(gpkg_file_path), exist_ok=True)
                if "OWN" in df_ods.iloc[i, 8]:
                    gdf = gpd.read_postgis(query, conn, geom_col="geom")
                    has_null_values = gdf["geom"].isnull().any()
                    if has_null_values:
                        gdf = gdf.dropna(subset=["geom"])
                    gdf.to_file(gpkg_file_path, layer=gpkg_filename, driver="GPKG")
                    update_geometry_type_name(gpkg_file_path)
                    print(f"'{gpkg_filename}.gpkg' was created successfully.")
                else:
                    continue
            except Exception as e:
                print(
                    f"Error with query for {gpkg_filename}. Now trying to generate geodataframe with 'geom_polygon'..."
                )
                try:
                    gdf = gpd.read_postgis(query, conn, geom_col="geom_polygon")
                    gdf.to_file(gpkg_file_path, layer=gpkg_filename, driver="GPKG")
                    update_geometry_type_name(gpkg_file_path)
                    print(f"'{gpkg_filename}.gpkg' was now created successfully.")
                except:
                    print(
                        f"Error with query for {gpkg_filename} could not be resolved."
                    )
                    print(str(e))


def create_mv_grid_district_gpkg(
    df_ods: pd.DataFrame,
    conn: psycopg2.connect,
    egon_scenario: str,
    path: str,
    ignore_query_category_list: list = [],
):
    """
    Creates a single GeoPackage by combining data from multiple DataFrames.

    Args:
        df_ods (pandas.DataFrame): DataFrame containing the SQL queries and metadata from 'WebApp_scenario_data.ods'.
        conn (psycopg2.connect): database connection to execute the SQL queries.
        egon_scenario (str): eGon scenario name ('2035' or '100re').
        path (str): directory path where the GeoPackages will be saved.
        ignore_query_category_list (list): (OPTIONAL) list of category names where queries will be skipped.
    
    Returns:
        None

    Raises:
        Exception: If an error occurs while executing a SQL query or creating a GeoPackage.
    """
    if egon_scenario == "2035":
        column = 5
    else:
        column = 6
    category_name, subcategory_name = "", ""

    print("Querying data and creating merged geopackage...")

    # Read the base GeoDataFrame to build the final GeoPackage
    gdf_query = "SELECT bus_id, geom, area FROM grid.egon_mv_grid_district"
    gdf_base = gpd.read_postgis(gdf_query, conn, geom_col="geom")

    # Create an empty DataFrame to store the merged data
    df_merged = gdf_base[["bus_id", "geom", "area"]].copy()

    for i, value in enumerate(df_ods.iloc[:, column]):
        if not pd.isna(df_ods.iloc[i, 0]) and df_ods.iloc[i, 0] != category_name:
            category_name = df_ods.iloc[i, 0]
        if (
            isinstance(value, str)
            and (value.lower().startswith("select") or value.lower().startswith("with"))
            and category_name not in ignore_query_category_list
        ):
            subcategory_name = df_ods.iloc[i, 1]
            layer_name = df_ods.iloc[i, 2]
            try:
                if "OWN" not in df_ods.iloc[i, 8]:
                    query = value
                    gpkg_filename = (
                        f"{category_name}_{subcategory_name}_{layer_name}".replace(
                            "/", "_"
                        )
                        .replace(" ", "_")
                        .replace("-_", "")
                        .replace("(", "")
                        .replace(")", "")
                        .lower()
                    )

                    df = pd.read_sql_query(query, conn)

                    # Rename columns to 'bus_id' if necessary
                    if "mv_grid_district_id" in df.columns:
                        df.rename(
                            columns={"mv_grid_district_id": "bus_id"}, inplace=True
                        )
                    if "mv_grid_id" in df.columns:
                        df.rename(columns={"mv_grid_id": "bus_id"}, inplace=True)

                    # Add the prefix to column names
                    columns_to_rename = [col for col in df.columns if col != "bus_id"]
                    df.rename(
                        columns={
                            col: f"{gpkg_filename}_{col}" for col in columns_to_rename
                        },
                        inplace=True,
                    )

                    # Merge the DataFrame based on 'bus_id'
                    df_merged = pd.merge(df_merged, df, on="bus_id", how="left")

                    print(f"'{gpkg_filename}' added to the merged dataframe...")

            except Exception as e:
                print(f"Error with query for {gpkg_filename} could not be resolved.")
                print(str(e))

    # Convert the merged DataFrame to a GeoDataFrame
    gdf_merged = gpd.GeoDataFrame(df_merged, geometry="geom")
    gdf_merged.fillna(0, inplace=True)
    # Save the merged GeoDataFrame as a GeoPackage
    merged_gpkg_path = f"{path}/egon{egon_scenario}.grid.egon_mv_grid_district.gpkg"
    # Create directory if it does not exist
    os.makedirs(os.path.dirname(merged_gpkg_path), exist_ok=True)
    gdf_merged.to_file(merged_gpkg_path, driver="GPKG")
    print(f"'{merged_gpkg_path}' was created successfully.")


def create_mapping_table(conn):
    """
    Creates a necessary mapping table 'boundaries.egon_map_grid_districts_bus_ids' in the database
    to associate grid district IDs with bus IDs and scenario names.

    Args:
        conn (psycopg2.connect): A PostgreSQL database connection.

    Returns:
        None

    Raises:
        psycopg2.Error: If there's an error with the PostgreSQL database operations.
    """
    cur = conn.cursor()

    # Check if the table already exists
    check_table_query = """
    SELECT EXISTS 
    (SELECT FROM information_schema.tables WHERE table_name = 'egon_map_grid_districts_bus_ids')
    """
    cur.execute(check_table_query)
    table_exists = cur.fetchone()[0]

    if not table_exists:
        print(
            "Create necessary mapping table 'boundaries.egon_map_grid_districts_bus_ids' in 'egon-data'"
        )
        # Create the mapping table
        query_create_table_ = """
        CREATE TABLE boundaries.egon_map_grid_districts_bus_ids
        AS
        SELECT b.bus_id AS mv_grid_district_id, a.bus_id, a.scn_name
        FROM grid.egon_etrago_bus a
        JOIN grid.egon_mv_grid_district b
        ON ST_Contains(ST_Transform(b.geom, 4326), a.geom)
        WHERE a.carrier = 'AC' AND a.scn_name in ('eGon2035', 'eGon100RE') AND a.country = 'DE'
        ORDER BY (b.bus_id, a.bus_id)
        """
        cur.execute(query_create_table_)
        conn.commit()

        # Add nodes manually
        query_insert_node = """
        INSERT INTO boundaries.egon_map_grid_districts_bus_ids(mv_grid_district_id, bus_id, scn_name)
        VALUES
        (33935, 15662, 'eGon2035'),
        (33935, 15662, 'eGon100RE'),
        (33935, 33250, 'eGon2035'),
        (33935, 33250, 'eGon100RE'),
        (35828, 34945, 'eGon2035'),
        (35828, 34945, 'eGon100RE')
        """
        cur.execute(query_insert_node)
        conn.commit()
        print("Mapping table successfully created.")
    
    cur.close()



def update_geometry_type_name(gpkg_file_path):
    # Connect to the GeoPackage using sqlite3
    conn = sqlite3.connect(gpkg_file_path)

    # Create a cursor to execute SQL commands
    cursor = conn.cursor()

    # Update the value in the "geometry_type_name" column if it is "GEOMETRY"
    query = "UPDATE gpkg_geometry_columns SET geometry_type_name = ? WHERE geometry_type_name = ?;"
    cursor.execute(query, ("MULTIPOLYGON", "GEOMETRY"))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
