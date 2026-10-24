
from flask import Flask
from rute.web import web
from rute.api import api


def create_app():
    app = Flask(__name__)
    app.register_blueprint(web)
    app.register_blueprint(api)
    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
