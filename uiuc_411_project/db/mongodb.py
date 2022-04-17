from pymongo import MongoClient, errors

DB_NAME = "academicworld"


def _init_mongodb_client() -> MongoClient:
    try:
        # Connect to local mongo db
        return MongoClient()
    except errors.ConnectionFailure as e:
        print(f"Failed to connect to mongodb due to: {e}")
        exit(0)


client = _init_mongodb_client()


def get_table_items() -> None:
    db = client[DB_NAME]



def connect_to_mongodb() -> None:
    pass
