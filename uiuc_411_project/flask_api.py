from flask import Flask

from uiuc_411_project.db.mongodb import get_us_college_map_info

flask_app = Flask(__name__)


def register_routes(app: Flask) -> None:
    @app.get("/ping")
    def ping():
        return "pong"

    @app.get("/college_and_faculty_map")
    def get_college_faculty_map():
        df = get_us_college_map_info()
        return df.to_dict(orient="split")
