#!/bin/bash

echo "Waiting for MongoDB to start..."
until mongosh --host localhost --eval "print('MongoDB is ready!')" &>/dev/null; do
  sleep 2
done

echo "Importing sensor data into MongoDB..."

# Define database name
DB_NAME="Temp_DB"

# Import JSON files into respective collections
mongoimport --db "$DB_NAME" --collection air_quality --file /data/Project_sensor_data/air_quality_sensor_data.json
mongoimport --db "$DB_NAME" --collection humidity --file /data/Project_sensor_data/humidity_sensor_data.json
mongoimport --db "$DB_NAME" --collection room_facilities --file /data/Project_sensor_data/room_facilities_data.json 
mongoimport --db "$DB_NAME" --collection temperature --file /data/Project_sensor_data/temperature_sensor_data.json 
mongoimport --db "$DB_NAME" --collection co2 --file /data/Project_sensor_data/co2_sensor_data.json 
mongoimport --db "$DB_NAME" --collection light_intensity --file /data/Project_sensor_data/LightIntensity_sensor_data.json 
mongoimport --db "$DB_NAME" --collection sound --file /data/Project_sensor_data/sound_sensor_data.json 
mongoimport --db "$DB_NAME" --collection voc --file /data/Project_sensor_data/voc_sensor_data.json 

echo "Data import completed successfully!"
