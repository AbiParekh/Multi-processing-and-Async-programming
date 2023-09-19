from flask import Flask, jsonify
from flask_cors import CORS
import threading
from api import API
from flask_sqlalchemy import SQLAlchemy

# from app import db

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///teams.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(80), nullable=False)
    team_number = db.Column(db.String(80), nullable=False)
    team_code = db.Column(db.String(80), nullable=False)
    score = db.Column(db.String(80), nullable=False)


with app.app_context():
    db.create_all()

team_stats_cache = []


@app.route('/api/team_statistics', methods=['GET'])
def team_statistics():
    teams = Team.query.all()
    team_stats = [
        {
            "team_name": team.team_name,
            "team_number": team.team_number,
            "team_code": team.team_code,
            "score": team.score
        }
        for team in teams
    ]
    return jsonify(team_stats), 200


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()


def communication_thread_function():
    api_call = API()
    team_stats = api_call.get_team_statistics()

    try:
        # Save to the database
        for stat in team_stats:
            team = Team(team_name=stat.team_name, team_number=stat.team_number, team_code=stat.team_code, score=stat.score)
            db.session.add(team)
        db.session.commit()
    except Exception as e:
        print(f"Error saving to database: {e}")
        db.session.rollback()
    finally:
        db.session.close()

    global team_stats_cache
    team_stats_cache = [team_stat.add_to_tuple() for team_stat in team_stats]
    print("Data fetched:", team_stats_cache)


def presentation_thread_function():
    while not team_stats_cache:
        print("Presentation thread: Waiting for data from the communication thread...")
        threading.Event().wait(timeout=1)
    print("Presentation thread: Data ready for presentation!")


@app.errorhandler(500)
def handle_internal_error(error):
    return jsonify({"error": "An internal error occurred."}), 500


@app.errorhandler(404)
def handle_not_found(error):
    return jsonify({"error": "Resource not found."}), 404


if __name__ == "__main__":
    # Start the threads
    threading.Thread(target=communication_thread_function).start()
    threading.Thread(target=presentation_thread_function).start()

    # Start the Flask app
    app.run(debug=True)
