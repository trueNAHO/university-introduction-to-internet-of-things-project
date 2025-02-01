#!/bin/bash

mongo_import() {
  mongoimport --db Temp_DB --collection "$1" --file "$2"
}

until
  mongosh --host localhost --eval "print('MongoDB is ready!')" &>/dev/null
do
  printf '[%s] %s\n' "$(date --iso-8601=second)" "Waiting for MongoDB to start"
  sleep 0.1
done

mongo_import air_quality /data/Project_sensor_data/air_quality_sensor_data.json
mongo_import co2 /data/Project_sensor_data/co2_sensor_data.json
mongo_import humidity /data/Project_sensor_data/humidity_sensor_data.json

mongo_import \
  light_intensity \
  /data/Project_sensor_data/LightIntensity_sensor_data.json

mongo_import room_facilities /data/Project_sensor_data/room_facilities_data.json
mongo_import sound /data/Project_sensor_data/sound_sensor_data.json
mongo_import temperature /data/Project_sensor_data/temperature_sensor_data.json
mongo_import voc /data/Project_sensor_data/voc_sensor_data.json
