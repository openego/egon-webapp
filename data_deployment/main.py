import json
import geopandas as gpd
import pandas as pd
import psycopg2
from sshtunnel import SSHTunnelForwarder
import os
from functools import reduce
from utils import *

# Make sure that the ods file is up to date and the structure still matches with the values in 'usecols'!
ods_file = "WebApp_scenario_data.ods"
json_refs_list = [{"eGon2035": {}}, {"eGon100RE": {}}]

# Optional: Add specific geo-reference names to 'ignore_query_geodata' to skip these queries
ignore_query_geodata = ["-"]

# Optional: Add specific category names to 'ignore_query_category_data' to skip these queries
ignore_query_category_data = [
    "Aggregation levels",
]


if __name__ == "__main__":
    with SSHTunnelForwarder(
        ("142.132.250.219", 22),
        ssh_username="egon",
        remote_bind_address=("localhost", 59763),
    ) as server:
        server.start()
        # status
        print("Server connected.")

        params = {
            "database": "egon-data",
            "user": "egon",
            "password": "data",
            "host": "localhost",
            "port": server.local_bind_port,
        }

        conn = psycopg2.connect(**params)

        # status
        print("DB connected.")

        # ---- Create mapping table (if not already existing in db) ----
        create_mapping_table(conn)

        # read ods reference file and build dataframe (pandas)
        df_ods = pd.read_excel(
            ods_file,
            engine="odf",
            header=None,
            usecols=[0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
            skiprows=6,
        )

        # ----- query data and create gpkgs with 'OWN' geom -----
        # scenario == eGon2035
        create_gpkgs(df_ods, conn, "2035", "gpkgs", ignore_query_category_data)

        # # scenario == eGon100RE
        create_gpkgs(df_ods, conn, "100re", "gpkgs", ignore_query_category_data)

        # ----- query data and create merged gpkg with 'geom' from 'grid.mv_grid_districts' -----
        # create_mv_grid_district_gpkg(df_ods, conn, "100re", "gpkgs")
        # create_mv_grid_district_gpkg(df_ods, conn, "2035", "gpkgs")

        print("Finished creating gpkgs.")
        # Close Connection to DB
        conn.close()
