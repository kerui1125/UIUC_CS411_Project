from flask import Flask

flask_app = Flask(__name__)


def register_routes(app: Flask) -> None:
    @app.get("/ping")
    def hello_world():
        return "pong"
