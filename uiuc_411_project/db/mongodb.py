from collections import defaultdict
import csv
import os
import pandas as pd
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from uiuc_411_project.utils import get_college_geo_coordinates

DB_NAME = "academicworld"
DEFAULT_FILE_PATH = "/Users/liukerui/Documents/CS411 Database Sys/final_project/UIUC_CS411_Project/us_college_map.csv"


def get_us_college_map_info(file_path: str = DEFAULT_FILE_PATH) -> pd.DataFrame:
    """
    Return dataframe from local csv file if the data has been cached,
    otherwise querying mongodb for data and cache it on local host.
    """
    if not os.path.exists(file_path):
        query_mongodb_and_save_to_csv(file_path)
    return pd.read_csv(file_path)


def query_mongodb_and_save_to_csv(file_path: str = DEFAULT_FILE_PATH) -> None:
    """
    Get all distinct college names from mongodb and calculate each of their number of faculty members.
    All geo info is fetched from geopy ArcGIS client.
    Data is then cached in a local csv file.
    """
    try:
        with open(file_path, "w") as f:
            writer = csv.writer(f)
            writer.writerow(["college", "professors", "lat", "lon"])

            # Connect to local mongo db
            client = MongoClient()
            collection = client[DB_NAME]["faculty"]
            names = collection.distinct("affiliation.name")
            us_map_info = defaultdict(dict)
            for name in names:
                try:
                    latitude, longitude = get_college_geo_coordinates(name)
                    professors = len(list(collection.find({"affiliation.name": name})))
                    us_map_info[name]["latitude"] = latitude
                    us_map_info[name]["longitude"] = longitude
                    us_map_info[name]["professors"] = professors
                    writer.writerow([name, professors, latitude, longitude])
                except Exception as e:
                    print(e)
    except ConnectionFailure as e:
        print(f"Failed to connect to mongodb due to: {e}")
        exit(0)
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        exit(0)
