import json
import os
from waitress import serve
from flask import Flask, jsonify, request, session, render_template
from chess.gui.main_menu import MainMenu
import state


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

    @app.route('/get_index', methods=['GET'])
    def get_index():
        current_index = session.get('question_index', 1)
        return jsonify({'currentIndex': current_index})

    @app.route('/set_index', methods=['POST'])
    def set_index():
        data = request.json
        new_index = data.get('index')
        if new_index:
            session['question_index'] = new_index
        return jsonify({'status': 'ok', 'newIndex': session.get('question_index', 1)})

    @app.route('/end', methods=['POST'])
    def end_script():
        chess = MainMenu()
        chess.init_game(1)
        chess.mainloop()
        return jsonify({'status': 'ok'})

    @app.route('/get_fide_elo', methods=['GET'])
    def get_fide_elo():
        return jsonify({"fide_elo": state.FIDE_ELO})


app = Flask(__name__)
app.secret_key = "endives_au_jambon"
configure_routes(app)
