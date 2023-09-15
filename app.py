from flask import Flask, jsonify
from flask_cors import CORS
import threading
from api import API

app = Flask(__name__)
CORS(app)

team_stats_cache = []


@app.route('/api/team_statistics', methods=['GET'])
def team_statistics():
    global team_stats_cache
    return jsonify(team_stats_cache), 200


def communication_thread_function():
    api_call = API()
    global team_stats_cache
    team_stats_cache = [team_stat.add_to_tuple() for team_stat in api_call.get_team_statistics()]
    print("Data fetched:", team_stats_cache)


def presentation_thread_function():
    while not team_stats_cache:
        print("Presentation thread: Waiting for data from the communication thread...")
        threading.Event().wait(timeout=1)
    print("Presentation thread: Data ready for presentation!")


if __name__ == "__main__":
    # Start the threads
    threading.Thread(target=communication_thread_function).start()
    threading.Thread(target=presentation_thread_function).start()

    # Start the Flask app
    app.run(debug=True)
