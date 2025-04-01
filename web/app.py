import json
import os
from waitress import serve
from flask import Flask, jsonify, render_template


def start_web_server():
    serve(app, host="0.0.0.0", port=4236)


def configure_routes(app):
    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route("/mise_en_place_d_une_API_a_l_aide_de_Flask")
    def api():
        # Chemin absolu du fichier quest.json
        json_path = os.path.join(os.path.dirname(__file__), "quest.json")
        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return jsonify(data)


app = Flask(__name__)
configure_routes(app)
