from waitress import serve
from flask import Flask
from web.routes import configure_routes

app = Flask(__name__)
configure_routes(app)


def start_web_server():
    serve(app, host="0.0.0.0", port=5000)
