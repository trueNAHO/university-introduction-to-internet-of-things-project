from flask import Flask, render_template
from flasgger import Swagger
import os

app = Flask(__name__)
swagger = Swagger(app)

# here is the path to folder with data
BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://backend-api:8087")

DATA_FOLDER = "assets"


#  def load_sensor_data():
#      try:
#          with open(os.path.join(DATA_FOLDER, "air_quality_sensor_data.json")) as f:
#              air_quality_data = json.load(f)
#          with open(os.path.join(DATA_FOLDER, "co2_sensor_data.json")) as f:
#              co2_data = json.load(f)
#          with open(os.path.join(DATA_FOLDER, "humidity_sensor_data.json")) as f:
#              humidity_data = json.load(f)
#          with open(os.path.join(DATA_FOLDER, "light_intensity_sensor_data.json")) as f:
#              light_data = json.load(f)
#          with open(os.path.join(DATA_FOLDER, "room_facilities_data.json")) as f:
#              facilities_data = json.load(f)
#          with open(os.path.join(DATA_FOLDER, "temperature_sensor_data.json")) as f:
#              temperature_data = json.load(f)
#          with open(os.path.join(DATA_FOLDER, "voc_sensor_data.json")) as f:
#              voc_data = json.load(f)
#
#          return {
#              "air_quality": air_quality_data,
#              "co2": co2_data,
#              "humidity": humidity_data,
#              "light": light_data,
#              "facilities": facilities_data,
#              "temperature": temperature_data,
#              "voc": voc_data,
#          }
#      except Exception as e:
#          print(f"Error loading sensor data: {e}")
#          return {}
#
# sensor_data = load_sensor_data()

# def load_sensor_data():
#     try:
#         response = requests.get(f"{BACKEND_API_URL}/api/sensor_data")
#         response.raise_for_status()  # Raise error if request fails
#         return response.json()
#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching sensor data: {e}")
#         return {}
#
# sensor_data = load_sensor_data()


@app.route("/")
def index():
    return render_template("frontend.html")


# @app.route('/api/sensor_data', methods=['GET'])
# def get_sensor_data():
#     return jsonify(sensor_data)
#
# @app.route('/api/room_ranking', methods=['POST'])
# def rank_rooms():
#     print("DEBUG: sensor_data =", sensor_data)
#
#     user_preferences = request.json.get("preferences", {})
#     desired_profile = request.json.get("profile", {})
#
#     if "temperature" not in sensor_data:
#         return jsonify({"error": "temperature_sensor_data not found"}), 400
#
#     try:
#         rooms = []
#
#         air_quality_data = sensor_data["air_quality"][0] if isinstance(sensor_data["air_quality"], list) else {}
#         co2_data = sensor_data["co2"][0] if isinstance(sensor_data["co2"], list) else {}
#         humidity_data = sensor_data["humidity"][0] if isinstance(sensor_data["humidity"], list) else {}
#         light_data = sensor_data["light"][0] if isinstance(sensor_data["light"], list) else {}
#         facilities_data = {room["name"]: room["facilities"] for room in sensor_data["facilities"]["rooms"]}
#
#         for temp_entry in sensor_data["temperature"]:
#             room_name = temp_entry.get("room")
#
#             room_data = {
#                 "name": room_name,
#                 "temperature": temp_entry.get("temperature", 22),
#                 "humidity": humidity_data.get(room_name, {}).get("humidity", 50),
#                 "light": light_data.get(room_name, {}).get("lux", 300),
#                 "air_quality": air_quality_data.get(room_name, {}).get("AQI", 50),
#                 "facilities": facilities_data.get(room_name, {}),
#             }
#
#             rooms.append(room_data)
#
#         ranked_rooms = sorted(
#             rooms,
#             key=lambda x: abs(x["temperature"] - desired_profile.get("temperature", 22))
#         )
#
#         return jsonify(ranked_rooms)
#
#     except KeyError as e:
#         return jsonify({"error": f"Missing key: {e}"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
