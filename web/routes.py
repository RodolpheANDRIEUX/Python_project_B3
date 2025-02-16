from flask import jsonify


def configure_routes(app):
    @app.route("/")
    def home():
        return jsonify({"message": "Bienvenue sur le serveur Flask"})
