import re
from datetime import datetime

import connexion
from flask import jsonify
from swagger_server import mongo  # Import the PyMongo instance
from swagger_server.models.air_quality_value import AirQualityValue  # noqa: E501
from swagger_server.models.co2_value import CO2Value  # noqa: E501
from swagger_server.models.humidity_value import HumidityValue  # noqa: E501
from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server.models.inline_response2001 import InlineResponse2001  # noqa: E501
from swagger_server.models.inline_response20010 import InlineResponse20010  # noqa: E501
from swagger_server.models.inline_response2002 import InlineResponse2002  # noqa: E501
from swagger_server.models.inline_response2003 import InlineResponse2003  # noqa: E501
from swagger_server.models.inline_response2004 import InlineResponse2004  # noqa: E501
from swagger_server.models.inline_response2005 import InlineResponse2005  # noqa: E501
from swagger_server.models.inline_response2006 import InlineResponse2006  # noqa: E501
from swagger_server.models.inline_response2007 import InlineResponse2007  # noqa: E501
from swagger_server.models.inline_response2008 import InlineResponse2008  # noqa: E501
from swagger_server.models.inline_response2009 import InlineResponse2009  # noqa: E501
from swagger_server.models.inline_response201 import InlineResponse201  # noqa: E501
from swagger_server.models.light_intensity_value import LightIntensityValue  # noqa: E501
from swagger_server.models.room_facilities import RoomFacilities  # noqa: E501
from swagger_server.models.sound_value import SoundValue  # noqa: E501
from swagger_server.models.temperature_value import TemperatureValue  # noqa: E501
from swagger_server.models.voc_value import VOCValue  # noqa: E501
from swagger_server import util


def check_format(date_string):
    # Regular expression for the format Y-m-dTh:m:s.s
    regex = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+$"

    # Check if the string matches the regex pattern
    if not re.match(regex, date_string):
        return False

    try:
        # Extract the main date-time part before fractional seconds
        main_part = date_string.split(".")[0]
        # Validate date-time format
        datetime.strptime(main_part, "%Y-%m-%dT%H:%M:%S")
        # If all checks pass
        return True
    except ValueError:
        return False


def air_quality_room_name_get(room_name):
    """Retrieve air quality of a room

    Returns a list of all air quality values for a specific room. # noqa: E501

    :param room_name: Name of the room to retrieve air quality data for
    :type room_name: str

    :rtype: InlineResponse2002
    """

    # Query the database for the specific room
    room_data = mongo.db.air_quality.find_one({"rooms.name": room_name})

    if not room_data:
        return jsonify({"error": "Room not found"}), 404

    for room in room_data["rooms"]:
        if room["name"] == room_name:
            air_quality_data = room.get("air_quality_values", [])
            break
    else:
        return jsonify({"error": "Room not found"}), 404

    return jsonify({"room_name": room_name, "air_quality_data": air_quality_data})


def air_quality_room_name_post(body, room_name):  # noqa: E501
    """Add a new air quality value to a room

    Adds a new air quality value for the specified room. # noqa: E501

    :param body:
    :type body: dict | bytes
    :param room_name: Name of the room to add air quality data to
    :type room_name: str

    :rtype: None
    """
    # Parse the input body
    if not connexion.request.is_json:
        return jsonify({"error": "Invalid input: JSON payload required"}), 400

    body = connexion.request.get_json()

    # Validate the required fields
    required_fields = ["timestamp", "PM2.5", "PM10"]
    missing_fields = [field for field in required_fields if field not in body]

    if missing_fields:
        return jsonify(
            {
                "error": "Invalid input: Missing required fields",
                "missing_fields": missing_fields,
            }
        ), 400

    # Validate the timestamp format using check_format
    timestamp = body["timestamp"]
    if not check_format(timestamp):
        return jsonify(
            {
                "error": "Invalid input: 'timestamp' must be in format YYYY-MM-DDTHH:MM:SS.ssssss",
                "example": "2024-10-29T06:48:42.987448",
            }
        ), 400

    # Validate PM2.5 and PM10 are floats
    float_fields = ["PM2.5", "PM10"]
    invalid_fields = [
        field for field in float_fields if not isinstance(body[field], (float, int))
    ]

    if invalid_fields:
        return jsonify(
            {
                "error": "Invalid input: Fields must be of type float",
                "invalid_fields": invalid_fields,
            }
        ), 400

    # Query the database for the specific room
    room_data = mongo.db.air_quality.find_one({"rooms.name": room_name})

    if not room_data:
        return jsonify({"error": "Room not found"}), 404

    # Iterate through the rooms to find the specific one
    for room in room_data["rooms"]:
        if room["name"] == room_name:
            # Append the new air quality value to the room's air_quality_values list
            if "air_quality_values" not in room:
                room[
                    "air_quality_values"
                ] = []  # Initialize the list if it doesn't exist
            room["air_quality_values"].append(body)
            break
    else:
        return jsonify({"error": "Room not found"}), 404

    # Update the database with the modified document
    mongo.db.air_quality.update_one(
        {"_id": room_data["_id"]},  # Match the specific document
        {"$set": {"rooms": room_data["rooms"]}},  # Update the rooms array
    )

    # Return a success response
    return jsonify({"message": "Air quality value successfully added to the room"}), 201


def c_o2_room_name_get(room_name):  # noqa: E501
    """Retrieve CO2 levels of a room

    Returns a list of all CO2 level values for a specific room. # noqa: E501

    :param room_name: Name of the room to retrieve CO2 level data for
    :type room_name: str

    :rtype: InlineResponse2003
    """
    # Query the database for the specific room
    room_data = mongo.db.co2.find_one({"rooms.name": room_name})

    if not room_data:
        return jsonify({"error": "Room not found"}), 404

    for room in room_data["rooms"]:
        if room["name"] == room_name:
            co2_data = room.get("co2_values", [])
            break
    else:
        return jsonify({"error": "Room not found"}), 404

    return jsonify({"room_name": room_name, "co2_data": co2_data})


def c_o2_room_name_post(body, room_name):  # noqa: E501
    """Add a new CO2 level value to a room

    Adds a new CO2 level value for the specified room. # noqa: E501

    :param body:
    :type body: dict | bytes
    :param room_name: Name of the room to add CO2 level data to
    :type room_name: str

    :rtype: None
    """
    # Parse the input body
    if not connexion.request.is_json:
        return jsonify({"error": "Invalid input: JSON payload required"}), 400

    body = connexion.request.get_json()

    # Validate the required fields
    required_fields = ["timestamp", "co2_level"]
    missing_fields = [field for field in required_fields if field not in body]

    if missing_fields:
        return jsonify(
            {
                "error": "Invalid input: Missing required fields",
                "missing_fields": missing_fields,
            }
        ), 400

    # Validate the timestamp format using check_format
    timestamp = body["timestamp"]
    if not check_format(timestamp):
        return jsonify(
            {
                "error": "Invalid input: 'timestamp' must be in format YYYY-MM-DDTHH:MM:SS.ssssss",
                "example": "2024-10-29T06:48:42.987448",
            }
        ), 400

    # Validate co2_level is float
    float_fields = ["co2_level"]
    invalid_fields = [
        field for field in float_fields if not isinstance(body[field], (float, int))
    ]

    if invalid_fields:
        return jsonify(
            {
                "error": "Invalid input: Fields must be of type float",
                "invalid_fields": invalid_fields,
            }
        ), 400

    # Query the database for the specific room
    room_data = mongo.db.co2.find_one({"rooms.name": room_name})

    if not room_data:
        return jsonify({"error": "Room not found"}), 404

    # Iterate through the rooms to find the specific one
    for room in room_data["rooms"]:
        if room["name"] == room_name:
            # Append the new CO2 value to the room's co2_values list
            if "co2_values" not in room:
                room["co2_values"] = []  # Initialize the list if it doesn't exist
            room["co2_values"].append(body)
            break
    else:
        return jsonify({"error": "Room not found"}), 404

    # Update the database with the modified document
    mongo.db.co2.update_one(
        {"_id": room_data["_id"]},  # Match the specific document
        {"$set": {"rooms": room_data["rooms"]}},  # Update the rooms array
    )

    # Return a success response
    return jsonify({"message": "CO2 value successfully added to the room"}), 201


def humidity_room_name_get(room_name):  # noqa: E501
    """Retrieve humidity levels of a room

    Returns a list of all humidity level values for a specific room. # noqa: E501

    :param room_name: Name of the room to retrieve humidity level data for
    :type room_name: str

    :rtype: InlineResponse2004
    """
    # Query the database for the specific room
    room_data = mongo.db.humidity.find_one({"rooms.name": room_name})

    if not room_data:
        return jsonify({"error": "Room not found"}), 404

    for room in room_data["rooms"]:
        if room["name"] == room_name:
            humidity_data = room.get("humidity_values", [])
            break
    else:
        return jsonify({"error": "Room not found"}), 404

    return jsonify({"room_name": room_name, "humidity_data": humidity_data})


def humidity_room_name_post(body, room_name):  # noqa: E501
    """Add a new humidity level value to a room

    Adds a new humidity level value for the specified room. # noqa: E501

    :param body:
    :type body: dict | bytes
    :param room_name: Name of the room to add humidity level data to
    :type room_name: str

    :rtype: None
    """
    # Parse the input body
    if not connexion.request.is_json:
        return jsonify({"error": "Invalid input: JSON payload required"}), 400

    body = connexion.request.get_json()

    # Validate the required fields
    required_fields = ["timestamp", "humidity"]
    missing_fields = [field for field in required_fields if field not in body]

    if missing_fields:
        return jsonify(
            {
                "error": "Invalid input: Missing required fields",
                "missing_fields": missing_fields,
            }
        ), 400

    # Validate the timestamp format using check_format
    timestamp = body["timestamp"]
    if not check_format(timestamp):
        return jsonify(
            {
                "error": "Invalid input: 'timestamp' must be in format YYYY-MM-DDTHH:MM:SS.ssssss",
                "example": "2024-10-29T06:48:42.987448",
            }
        ), 400

    # Validate humidity is float
    float_fields = ["humidity"]
    invalid_fields = [
        field for field in float_fields if not isinstance(body[field], (float, int))
    ]

    if invalid_fields:
        return jsonify(
            {
                "error": "Invalid input: Fields must be of type float",
                "invalid_fields": invalid_fields,
            }
        ), 400

    # Query the database for the specific room
    room_data = mongo.db.humidity.find_one({"rooms.name": room_name})

    if not room_data:
        return jsonify({"error": "Room not found"}), 404

    # Iterate through the rooms to find the specific one
    for room in room_data["rooms"]:
        if room["name"] == room_name:
            # Append the new Humidity value to the room's humidity_values list
            if "humidity_values" not in room:
                room["humidity_values"] = []  # Initialize the list if it doesn't exist
            room["humidity_values"].append(body)
            break
    else:
        return jsonify({"error": "Room not found"}), 404

    # Update the database with the modified document
    mongo.db.humidity.update_one(
        {"_id": room_data["_id"]},  # Match the specific document
        {"$set": {"rooms": room_data["rooms"]}},  # Update the rooms array
    )

    # Return a success response
    return jsonify({"message": "Humidity value successfully added to the room"}), 201


def light_intensity_room_name_get(room_name):  # noqa: E501
    """Retrieve light intensity levels of a room

    Returns a list of all light intensity values for a specific room. # noqa: E501

    :param room_name: Name of the room to retrieve light intensity data for
    :type room_name: str

    :rtype: InlineResponse2005
    """
    # Query the database for the specific room
    room_data = mongo.db.light_intensity.find_one({"rooms.name": room_name})

    if not room_data:
        return jsonify({"error": "Room not found"}), 404

    for room in room_data["rooms"]:
        if room["name"] == room_name:
            light_intensity_data = room.get("light_intensity_values", [])
            break
    else:
        return jsonify({"error": "Room not found"}), 404

    return jsonify(
        {"room_name": room_name, "light_intensity_data": light_intensity_data}
    )


def light_intensity_room_name_post(body, room_name):  # noqa: E501
    """Add a new light intensity value to a room

    Adds a new light intensity value for the specified room. # noqa: E501

    :param body:
    :type body: dict | bytes
    :param room_name: Name of the room to add light intensity data to
    :type room_name: str

    :rtype: None
    """
    # Parse the input body
    if not connexion.request.is_json:
        return jsonify({"error": "Invalid input: JSON payload required"}), 400

    body = connexion.request.get_json()

    # Validate the required fields
    required_fields = ["timestamp", "light_intensity"]
    missing_fields = [field for field in required_fields if field not in body]

    if missing_fields:
        return jsonify(
            {
                "error": "Invalid input: Missing required fields",
                "missing_fields": missing_fields,
            }
        ), 400

    # Validate the timestamp format using check_format
    timestamp = body["timestamp"]
    if not check_format(timestamp):
        return jsonify(
            {
                "error": "Invalid input: 'timestamp' must be in format YYYY-MM-DDTHH:MM:SS.ssssss",
                "example": "2024-10-29T06:48:42.987448",
            }
        ), 400

    # Validate light_intensity is float
    float_fields = ["light_intensity"]
    invalid_fields = [
        field for field in float_fields if not isinstance(body[field], (float, int))
    ]

    if invalid_fields:
        return jsonify(
            {
                "error": "Invalid input: Fields must be of type float",
                "invalid_fields": invalid_fields,
            }
        ), 400

    # Query the database for the specific room
    room_data = mongo.db.light_intensity.find_one({"rooms.name": room_name})

    if not room_data:
        return jsonify({"error": "Room not found"}), 404

    # Iterate through the rooms to find the specific one
    for room in room_data["rooms"]:
        if room["name"] == room_name:
            # Append the new Light Intensity value to the room's light_intensity_values list
            if "light_intensity_values" not in room:
                room[
                    "light_intensity_values"
                ] = []  # Initialize the list if it doesn't exist
            room["light_intensity_values"].append(body)
            break
    else:
        return jsonify({"error": "Room not found"}), 404

    # Update the database with the modified document
    mongo.db.light_intensity.update_one(
        {"_id": room_data["_id"]},  # Match the specific document
        {"$set": {"rooms": room_data["rooms"]}},  # Update the rooms array
    )

    # Return a success response
    return jsonify(
        {"message": "Light Intensity value successfully added to the room"}
    ), 201


def room_facilities_room_name_get(room_name):  # noqa: E501
    """Retrieve room facilities of a room

    Returns a list of all room facilities for a specific room. # noqa: E501

    :param room_name: Name of the room to retrieve facilities data for
    :type room_name: str

    :rtype: InlineResponse2009
    """
    # Query the database for the specific room
    room_data = mongo.db.room_facilities.find_one({"rooms.name": room_name})

    if not room_data:
        return jsonify({"error": "Room not found"}), 404

    for room in room_data["rooms"]:
        if room["name"] == room_name:
            facilities = room.get("facilities", [])
            break
    else:
        return jsonify({"error": "Room not found"}), 404

    return jsonify({"room_name": room_name, "facilities": facilities})


def room_facilities_room_name_post(body, room_name):  # noqa: E501
    """Add or update room facilities for a room

    Adds or updates room facilities for a specified room. # noqa: E501

    :param body:
    :type body: dict | bytes
    :param room_name: Name of the room to add/update facilities for
    :type room_name: str

    :rtype: None
    """
    # Parse the input body
    if not connexion.request.is_json:
        return jsonify({"error": "Invalid input: JSON payload required"}), 400

    body = connexion.request.get_json()

    # Define allowed fields and their expected types
    allowed_fields = {
        "videoprojector": bool,
        "seating_capacity": int,
        "computers": int,
        "robots_for_training": int,
    }

    # Check if the input body contains only the allowed fields
    invalid_fields = [field for field in body if field not in allowed_fields]
    if invalid_fields:
        return jsonify(
            {
                "error": "Invalid input: Only the following fields are allowed",
                "allowed_fields": list(allowed_fields.keys()),
                "invalid_fields": invalid_fields,
            }
        ), 400

    # Check the types of the fields
    type_mismatch_fields = [
        field
        for field, expected_type in allowed_fields.items()
        if field in body and not isinstance(body[field], expected_type)
    ]

    if type_mismatch_fields:
        return jsonify(
            {
                "error": "Invalid input: Fields must have the correct types",
                "type_mismatch_fields": type_mismatch_fields,
            }
        ), 400

    # Query the database for the specific room
    room_data = mongo.db.facilities.find_one({"rooms.name": room_name})

    if not room_data:
        return jsonify({"error": "Room not found"}), 404

    # Iterate through the rooms to find the specific one
    for room in room_data["rooms"]:
        if room["name"] == room_name:
            # Update or add the facilities for the room
            if "facilities" not in room:
                room["facilities"] = []  # Initialize the list if it doesn't exist
            room["facilities"].append(body)
            break
    else:
        return jsonify({"error": "Room not found"}), 404

    # Update the database with the modified document
    mongo.db.facilities.update_one(
        {"_id": room_data["_id"]},  # Match the specific document
        {"$set": {"rooms": room_data["rooms"]}},  # Update the rooms array
    )

    # Return a success response
    return jsonify({"message": "Facilities successfully added to the room"}), 201

def room_facilities_room_name_put(body, room_name):
    if not connexion.request.is_json:
        return jsonify({"error": "Invalid input: JSON payload required"}), 400

    body = connexion.request.get_json()

    allowed_fields = {
        "videoprojector": bool,
        "seating_capacity": int,
        "computers": int,
        "robots_for_training": int,
    }

    invalid_fields = [field for field in body if field not in allowed_fields]
    if invalid_fields:
        return jsonify(
            {
                "error": "Invalid input: Only the following fields are allowed",
                "allowed_fields": list(allowed_fields.keys()),
                "invalid_fields": invalid_fields,
            }
        ), 400

    type_mismatch_fields = [
        field
        for field, expected_type in allowed_fields.items()
        if field in body and not isinstance(body[field], expected_type)
    ]

    if type_mismatch_fields:
        return jsonify(
            {
                "error": "Invalid input: Fields must have the correct types",
                "type_mismatch_fields": type_mismatch_fields,
            }
        ), 400

    room_data = mongo.db.room_facilities.find_one({"rooms.name": room_name})

    if not room_data:
        return jsonify({"error": "Room not found"}), 404

    room_updated = False
    for room in room_data["rooms"]:
        if room["name"] == room_name:
            if "facilities" not in room:
                room["facilities"] = {}

            room["facilities"].update(body)
            room_updated = True
            break

    if not room_updated:
        return jsonify({"error": "Room not found"}), 404

    mongo.db.room_facilities.update_one(
        {"rooms.name": room_name}, {"$set": {"rooms.$.facilities": room["facilities"]}}
    )

    return jsonify(
        {
            "message": "Room facilities updated successfully",
            "room_name": room_name,
            "updated_facilities": body,
        }
    ), 200


def room_list_get():  # noqa: E501
    """Retrieve a list of all rooms, including their associated sensor data and facilities.

    Returns a list of all rooms, each including their associated details (e.g., sensor data, facilities). # noqa: E501

    :rtype: List[InlineResponse200]
    """

    # Sensor types we need to query
    sensor_types = [
        "air_quality",
        "co2",
        "humidity",
        "light_intensity",
        "sound",
        "temperature",
        "voc",
    ]

    # Initialize an empty list to hold room data
    rooms_data = {}

    # Loop through each sensor type to fetch data
    for sensor_type in sensor_types:
        sensor_data = mongo.db[
            sensor_type
        ].find()  # Get all data for the current sensor type

        # Loop through the data and group by room name
        for data in sensor_data:
            for room in data.get("rooms", []):
                room_name = room["name"]
                # Initialize the room data if not already done
                if room_name not in rooms_data:
                    rooms_data[room_name] = {
                        "room_name": room_name,
                        "sensor_data": {},
                        "facilities": {},
                    }

                # If sensor data for this room is not yet present, initialize it
                if sensor_type not in rooms_data[room_name]["sensor_data"]:
                    rooms_data[room_name]["sensor_data"][sensor_type] = []

                # Add the sensor data for this room and sensor type
                rooms_data[room_name]["sensor_data"][sensor_type].extend(
                    room.get(f"{sensor_type}_values", [])
                )

    # Now handle the room_facilities collection separately
    room_facilities_data = (
        mongo.db.room_facilities.find()
    )  # Get all room facilities data

    for data in room_facilities_data:
        for room in data.get("rooms", []):
            room_name = room["name"]
            if (
                room_name in rooms_data
            ):  # Ensure we only update rooms that already have sensor data
                rooms_data[room_name]["facilities"] = room.get("facilities", {})

    # Convert the rooms_data dictionary to a list
    rooms_list = list(rooms_data.values())

    # Return the response with the list of rooms and their sensor data and facilities
    return jsonify(rooms_list), 200


def room_list_post(body):  # noqa: E501
    """Add a new AirQualityRoom to all sensor collections"""

    if not connexion.request.is_json:
        return jsonify({"error": "Invalid input: JSON payload required"}), 400

    body = connexion.request.get_json()

    if not isinstance(body, str) or not body.strip():
        return jsonify({"error": "Invalid room name"}), 400

    # Sensor collections in the database
    sensor_types = [
        "air_quality",
        "co2",
        "humidity",
        "light_intensity",
        "sound",
        "temperature",
        "voc",
        "room_facilities",
    ]

    # Check if the room already exists in any collection
    room_already_exists = False
    for sensor_type in sensor_types:
        existing_room = mongo.db[sensor_type].find_one({"rooms.name": body})
        if existing_room:
            room_already_exists = True
            bad_sensor = sensor_type
            break  # Stop checking once found

    if room_already_exists:
        return jsonify(
            {"error": f"Room '{body}' already exists in {bad_sensor}"}
        ), 409  # 409 Conflict

    # Loop through each sensor collection and add the new room
    for sensor_type in sensor_types:
        sensor_collection = mongo.db[sensor_type]

        if sensor_type == "room_facilities":
            # Room facilities should have a proper 'facilities' structure
            new_room = {"name": body, "facilities": {}}
        else:
            # Other sensor collections get an empty array for values
            new_room = {"name": body, f"{sensor_type}_values": []}

        sensor_collection.update_one(
            {},  # Match any document (assuming there's only one)
            {"$push": {"rooms": new_room}},
            upsert=True,  # Create a document if it doesn't exist
        )

    return jsonify(
        {"message": f"Room '{body}' successfully added to all collections."}
    ), 201

from flask import jsonify

def rooms_last_room_name_get(room_name):  # noqa: E501
    """Retrieve the last sensor values of a room

    Returns the most recent sensor values for a specific room.

    :param room_name: Name of the room to retrieve data for
    :type room_name: str

    :rtype: InlineResponse2002
    """
    sensor_types = {
        "Air_Quality": "air_quality",
        "CO2": "co2",
        "Humidity": "humidity",
        "Light_Intensity": "light_intensity",
        "Sound": "sound",
        "Temperature": "temperature",
        "VOC": "voc"
    }

    room_data = {"name": room_name}

    # Loop through each sensor type to get the most recent reading
    for sensor, collection in sensor_types.items():
        # Fetch the sensor data for the room
        sensor_document = mongo.db[collection].find_one({"rooms.name": room_name})

        if sensor_document:
            for room in sensor_document.get("rooms", []):
                if room["name"] == room_name:
                    # If values are available, get the last (most recent) value in the list
                    sensor_values = room.get(f"{sensor.lower()}_values", [])
                    if sensor_values:
                        room_data[sensor] = sensor_values[-1]  # Last item is the most recent
                    else:
                        room_data[sensor] = None
                    break
        else:
            room_data[sensor] = None

    # Fetch room facilities, if available
    facilities_document = mongo.db.room_facilities.find_one({"rooms.name": room_name})
    if facilities_document:
        for room in facilities_document.get("rooms", []):
            if room["name"] == room_name:
                room_data["Room_facilities"] = room.get("facilities", {})
                break
    else:
        room_data["Room_facilities"] = None

    # If no data was found for any sensor or facility, return a 404 error
    if not any(value is not None for value in room_data.values()):
        return jsonify({"error": "Room not found"}), 404

    # Return the data for the specified room
    return jsonify(room_data), 200




def room_list_names_get():  # noqa: E501
    """Retrieve a list of all room names

    Returns a list of all existing room names from the sensor collections. # noqa: E501


    :rtype: List[str]
    """
    # Query the room_facilities collection for all room names
    facilities_document = mongo.db.room_facilities.find({}, {"rooms.name": 1})

    room_names = set()  # Use a set to avoid duplicates

    # Iterate through the documents in the room_facilities collection
    for doc in facilities_document:
        if "rooms" in doc:
            for room in doc["rooms"]:
                room_names.add(room["name"])  # Add room name to the set

    # Convert the set to a sorted list for consistency
    room_list = sorted(room_names)

    return jsonify(room_list), 200



def rooms_room_name_delete(room_name):  # noqa: E501
    """Delete a Room

    Removes a Room from the room’s record. # noqa: E501

    :param room_name: name of the room that needs to be deleted
    :type room_name: str

    :rtype: None
    """
    # List of all sensor types and collections
    sensor_types = [
        "air_quality",
        "co2",
        "humidity",
        "light_intensity",
        "sound",
        "temperature",
        "voc",
    ]
    facilities_collection = "room_facilities"

    # Flag to check if the room was found in any collection
    room_found = False

    # Delete the room from the `room_facilities` collection
    facilities_collection_ref = mongo.db[facilities_collection]

    delete_result = facilities_collection_ref.update_one(
        {"rooms.name": room_name},  # Find the document with the room
        {
            "$pull": {"rooms": {"name": room_name}}
        },  # Remove the room from the "rooms" array
    )
    if delete_result.modified_count > 0:
        room_found = True

    # Delete the room from all sensor collections
    for sensor_type in sensor_types:
        sensor_collection = mongo.db[sensor_type]

        delete_result = sensor_collection.update_one(
            {"rooms.name": room_name},  # Find the document with the room
            {
                "$pull": {"rooms": {"name": room_name}}
            },  # Remove the room from the "rooms" array
        )
        if delete_result.modified_count > 0:
            room_found = True

    # If no room was found in any collection, return 404
    if not room_found:
        return jsonify({"error": f"Room '{room_name}' not found"}), 404

    # Return a success response
    return jsonify(
        {"message": f"Room '{room_name}' successfully deleted from all collections."}
    ), 204


def rooms_room_name_get(room_name):  # noqa: E501
    """Retrive a list of room

    Returns a list of all rooms, each including their associated details. # noqa: E501

    :param room_name: name of the room that needs to be fetched
    :type room_name: str

    :rtype: List[InlineResponse200]
    """
    # Sensor types to query
    sensor_types = [
        "air_quality",
        "co2",
        "humidity",
        "light_intensity",
        "sound",
        "temperature",
        "voc",
    ]

    # Initialize a dictionary to hold the room data
    room_data = {"room_name": room_name, "sensor_data": {}, "facilities": {}}

    # Loop through each sensor type to fetch data for the room
    for sensor_type in sensor_types:
        sensor_collection = mongo.db[sensor_type]
        sensor_document = sensor_collection.find_one(
            {"rooms.name": room_name}
        )  # Fetch data for this room

        if sensor_document:  # If data exists for this sensor type
            for room in sensor_document.get("rooms", []):
                if room["name"] == room_name:
                    room_data["sensor_data"][sensor_type] = room.get(
                        f"{sensor_type}_values", []
                    )
                    break
    # Fetch room facilities data
    facilities_document = mongo.db.room_facilities.find_one({"rooms.name": room_name})

    if facilities_document:
        for room in facilities_document.get("rooms", []):
            if room["name"] == room_name:
                room_data["facilities"] = room.get("facilities", {})
                break

    # If no data was found, return a 404 error
    if not room_data["sensor_data"] and not room_data["facilities"]:
        return jsonify({"error": "Room not found"}), 404

    # Return the data for the specified room
    return jsonify(room_data), 200


def rooms_room_name_put(body, room_name):  # noqa: E501
    """Update room name

    Updates the name of an existing room. # noqa: E501

    :param body: New name of the room
    :type body: dict | bytes
    :param room_name: Current name of the room that needs to be updated
    :type room_name: str

    :rtype: InlineResponse2001
    """
    # Validate the body (new room name)
    if not isinstance(body, str) or not body.strip():
        return jsonify(
            {"error": "Invalid input: New room name must be a non-empty string"}
        ), 400

    new_room_name = body.strip()

    # Ensure the new room name is not already taken
    sensor_types = [
        "air_quality",
        "co2",
        "humidity",
        "light_intensity",
        "sound",
        "temperature",
        "voc",
    ]
    facilities_collection = "room_facilities"

    # Check if the new room name exists in the facilities collection
    facilities_collection_ref = mongo.db[facilities_collection]
    if facilities_collection_ref.find_one({"rooms.name": new_room_name}):
        return jsonify({"error": f"Room name '{new_room_name}' is already taken"}), 400

    # Check if the new room name exists in any sensor collection
    for sensor_type in sensor_types:
        sensor_collection = mongo.db[sensor_type]
        if sensor_collection.find_one({"rooms.name": new_room_name}):
            return jsonify(
                {"error": f"Room name '{new_room_name}' is already taken"}
            ), 400

    # Flag to track if the room name was updated in any collection
    room_found = False

    # Update the room name in the `room_facilities` collection
    update_result = facilities_collection_ref.update_one(
        {"rooms.name": room_name},  # Find the document with the old room name
        {"$set": {"rooms.$.name": new_room_name}},  # Update the room name
    )
    if update_result.modified_count > 0:
        room_found = True

    # Update the room name in all sensor collections
    for sensor_type in sensor_types:
        sensor_collection = mongo.db[sensor_type]

        update_result = sensor_collection.update_one(
            {"rooms.name": room_name},  # Find the document with the old room name
            {"$set": {"rooms.$.name": new_room_name}},  # Update the room name
        )
        if update_result.modified_count > 0:
            room_found = True

    # If the room name was not found in any collection, return 404
    if not room_found:
        return jsonify({"error": f"Room '{room_name}' not found"}), 404

    # Return success response
    return jsonify(
        {
            "message": "Room name updated successfully",
            "old_name": room_name,
            "updated_name": new_room_name,
        }
    ), 200


def sound_room_name_get(room_name):  # noqa: E501
    """Retrieve sound levels of a room

    Returns a list of all sound level values for a specific room. # noqa: E501

    :param room_name: Name of the room to retrieve sound level data for
    :type room_name: str

    :rtype: InlineResponse2006
    """
    # Query the database for the specific room
    room_data = mongo.db.sound.find_one({"rooms.name": room_name})

    if not room_data:
        return jsonify({"error": "Room not found"}), 404

    for room in room_data["rooms"]:
        if room["name"] == room_name:
            sound_data = room.get("sound_values", [])
            break
    else:
        return jsonify({"error": "Room not found"}), 404

    return jsonify({"room_name": room_name, "sound_data": sound_data})


def sound_room_name_post(body, room_name):  # noqa: E501
    """Add a new sound level value to a room

    Adds a new sound level value for the specified room. # noqa: E501

    :param body:
    :type body: dict | bytes
    :param room_name: Name of the room to add sound level data to
    :type room_name: str

    :rtype: None
    """
    # Parse the input body
    if not connexion.request.is_json:
        return jsonify({"error": "Invalid input: JSON payload required"}), 400

    body = connexion.request.get_json()

    # Validate the required fields
    required_fields = ["timestamp", "sound_level"]
    missing_fields = [field for field in required_fields if field not in body]

    if missing_fields:
        return jsonify(
            {
                "error": "Invalid input: Missing required fields",
                "missing_fields": missing_fields,
            }
        ), 400

    # Validate the timestamp format using check_format
    timestamp = body["timestamp"]
    if not check_format(timestamp):
        return jsonify(
            {
                "error": "Invalid input: 'timestamp' must be in format YYYY-MM-DDTHH:MM:SS.ssssss",
                "example": "2024-10-29T06:48:42.987448",
            }
        ), 400

    # Validate sound_level is float
    float_fields = ["sound_level"]
    invalid_fields = [
        field for field in float_fields if not isinstance(body[field], (float, int))
    ]

    if invalid_fields:
        return jsonify(
            {
                "error": "Invalid input: Fields must be of type float",
                "invalid_fields": invalid_fields,
            }
        ), 400

    # Query the database for the specific room
    room_data = mongo.db.sound.find_one({"rooms.name": room_name})

    if not room_data:
        return jsonify({"error": "Room not found"}), 404

    # Iterate through the rooms to find the specific one
    for room in room_data["rooms"]:
        if room["name"] == room_name:
            # Append the new Sound Level value to the room's sound_values list
            if "sound_values" not in room:
                room["sound_values"] = []  # Initialize the list if it doesn't exist
            room["sound_values"].append(body)
            break
    else:
        return jsonify({"error": "Room not found"}), 404

    # Update the database with the modified document
    mongo.db.sound.update_one(
        {"_id": room_data["_id"]},  # Match the specific document
        {"$set": {"rooms": room_data["rooms"]}},  # Update the rooms array
    )

    # Return a success response
    return jsonify({"message": "Sound Level value successfully added to the room"}), 201


def temperature_room_name_get(room_name):  # noqa: E501
    """Retrieve temperature of a room

    Returns a list of all temperature values for a specific room. # noqa: E501

    :param room_name: Name of the room to retrieve temperature data for
    :type room_name: str

    :rtype: InlineResponse2007
    """
    # Query the database for the specific room
    room_data = mongo.db.temperature.find_one({"rooms.name": room_name})

    if not room_data:
        return jsonify({"error": "Room not found"}), 404

    for room in room_data["rooms"]:
        if room["name"] == room_name:
            temperature_data = room.get("temperature_values", [])
            break
    else:
        return jsonify({"error": "Room not found"}), 404

    return jsonify({"room_name": room_name, "temperature_data": temperature_data})


def temperature_room_name_post(body, room_name):  # noqa: E501
    """Add a new temperature value to a room

    Adds a new temperature value for the specified room. # noqa: E501

    :param body:
    :type body: dict | bytes
    :param room_name: Name of the room to add temperature data to
    :type room_name: str

    :rtype: None
    """
    # Parse the input body
    if not connexion.request.is_json:
        return jsonify({"error": "Invalid input: JSON payload required"}), 400

    body = connexion.request.get_json()

    # Validate the required fields
    required_fields = ["timestamp", "temperature"]
    missing_fields = [field for field in required_fields if field not in body]

    if missing_fields:
        return jsonify(
            {
                "error": "Invalid input: Missing required fields",
                "missing_fields": missing_fields,
            }
        ), 400

    # Validate the timestamp format using check_format
    timestamp = body["timestamp"]
    if not check_format(timestamp):
        return jsonify(
            {
                "error": "Invalid input: 'timestamp' must be in format YYYY-MM-DDTHH:MM:SS.ssssss",
                "example": "2024-10-29T06:48:42.987448",
            }
        ), 400

    # Validate temperature is float
    float_fields = ["temperature"]
    invalid_fields = [
        field for field in float_fields if not isinstance(body[field], (float, int))
    ]

    if invalid_fields:
        return jsonify(
            {
                "error": "Invalid input: Fields must be of type float",
                "invalid_fields": invalid_fields,
            }
        ), 400

    # Query the database for the specific room
    room_data = mongo.db.temperature.find_one({"rooms.name": room_name})

    if not room_data:
        return jsonify({"error": "Room not found"}), 404

    # Iterate through the rooms to find the specific one
    for room in room_data["rooms"]:
        if room["name"] == room_name:
            # Append the new Temperature value to the room's temperature_values list
            if "temperature_values" not in room:
                room[
                    "temperature_values"
                ] = []  # Initialize the list if it doesn't exist
            room["temperature_values"].append(body)
            break
    else:
        return jsonify({"error": "Room not found"}), 404

    # Update the database with the modified document
    mongo.db.temperature.update_one(
        {"_id": room_data["_id"]},  # Match the specific document
        {"$set": {"rooms": room_data["rooms"]}},  # Update the rooms array
    )

    # Return a success response
    return jsonify({"message": "Temperature value successfully added to the room"}), 201


def v_oc_room_name_get(room_name):  # noqa: E501
    """Retrieve VOC levels of a room

    Returns a list of all VOC levels for a specific room. # noqa: E501

    :param room_name: Name of the room to retrieve VOC data for
    :type room_name: str

    :rtype: InlineResponse2008
    """
    # Query the database for the specific room
    room_data = mongo.db.voc.find_one({"rooms.name": room_name})

    if not room_data:
        return jsonify({"error": "Room not found"}), 404

    for room in room_data["rooms"]:
        if room["name"] == room_name:
            voc_data = room.get("voc_values", [])
            break
    else:
        return jsonify({"error": "Room not found"}), 404

    return jsonify({"room_name": room_name, "voc_data": voc_data})


def v_oc_room_name_post(body, room_name):  # noqa: E501
    """Add a new VOC value to a room

    Adds a new VOC value for the specified room. # noqa: E501

    :param body:
    :type body: dict | bytes
    :param room_name: Name of the room to add VOC data to
    :type room_name: str

    :rtype: None
    """
    # Parse the input body
    if not connexion.request.is_json:
        return jsonify({"error": "Invalid input: JSON payload required"}), 400

    body = connexion.request.get_json()

    # Validate the required fields
    required_fields = ["timestamp", "VOC_level"]
    missing_fields = [field for field in required_fields if field not in body]

    if missing_fields:
        return jsonify(
            {
                "error": "Invalid input: Missing required fields",
                "missing_fields": missing_fields,
            }
        ), 400

    # Validate the timestamp format using check_format
    timestamp = body["timestamp"]
    if not check_format(timestamp):
        return jsonify(
            {
                "error": "Invalid input: 'timestamp' must be in format YYYY-MM-DDTHH:MM:SS.ssssss",
                "example": "2024-10-29T06:48:42.987448",
            }
        ), 400

    # Validate VOC_level is float
    float_fields = ["VOC_level"]
    invalid_fields = [
        field for field in float_fields if not isinstance(body[field], (float, int))
    ]

    if invalid_fields:
        return jsonify(
            {
                "error": "Invalid input: Fields must be of type float",
                "invalid_fields": invalid_fields,
            }
        ), 400

    # Query the database for the specific room
    room_data = mongo.db.voc.find_one({"rooms.name": room_name})

    if not room_data:
        return jsonify({"error": "Room not found"}), 404

    # Iterate through the rooms to find the specific one
    for room in room_data["rooms"]:
        if room["name"] == room_name:
            # Append the new VOC value to the room's voc_values list
            if "voc_values" not in room:
                room["voc_values"] = []  # Initialize the list if it doesn't exist
            room["voc_values"].append(body)
            break
    else:
        return jsonify({"error": "Room not found"}), 404

    # Update the database with the modified document
    mongo.db.voc.update_one(
        {"_id": room_data["_id"]},  # Match the specific document
        {"$set": {"rooms": room_data["rooms"]}},  # Update the rooms array
    )

    # Return a success response
    return jsonify({"message": "VOC value successfully added to the room"}), 201
