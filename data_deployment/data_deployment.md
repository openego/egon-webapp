# Overview

**Note:** In the current version data preparation only works with direct DB
access, the OEP is not supported yet.

This script **queries data** from the **PostgreSQL database 'egon-data'** and *
*generates** **geopackages** from the query results. It uses **sshtunnel** to
connect to the remote server and database, and reads a locally provided
spreadsheet file ('WebApp_scenario_data.ods') to determine which queries to run.
If it doesn't already exist, a necessary mapping table is created in the
database to associate grid district IDs with bus IDs and scenario names.

## Requirements

- 'geopandas'
- 'pandas'
- 'psycopg2'
- 'sshtunnel'
- Spreadsheet file ('WebApp_scenario_data.ods') containing the necessary SQL
  queries and metadata
- SSH access to the server where the database is located

## Installation

If necessary, install the required packages:
```pip install geopandas pandas psycopg2 sshtunnel```

## Usage

1. Make sure you have **SSH access** to the server where the database is
   located.
2. If necessary, modify the values for **'ssh_username'**, **'database'**, **'
   user'**, and **'password'** to match your environment.
3. Make sure that the latest version of **'WebApp_scenario_data.ods'** is placed
   in the same directory as the script.
4. Run the script using ```python main.py```
5. The script will connect to the remote server and database, execute the
   queries specified in the ODS reference file, and create geopackages and put
   them into the 'gpkg' directory.
