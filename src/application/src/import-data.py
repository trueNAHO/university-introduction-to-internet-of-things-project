import time
import subprocess

# Function to perform the mongoimport operation
def mongo_import(collection, file):
    command = ['mongoimport', '--db', 'Temp_DB', '--collection', collection, '--file', file]
    subprocess.run(command, check=True)

# Wait for MongoDB to be ready
def wait_for_mongodb():
    while True:
        try:
            # Check if MongoDB is available by running a simple command
            subprocess.run(['mongosh', '--host', 'localhost', '--eval', "print('MongoDB is ready!')"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            break
        except subprocess.CalledProcessError:
            # If MongoDB is not ready, print a waiting message and sleep for a while
            print(f"[{time.strftime('%Y-%m-%dT%H:%M:%S')}] Waiting for MongoDB to start")
            time.sleep(0.1)

# Main logic to wait for MongoDB and run the imports
if __name__ == '__main__':
    wait_for_mongodb()

    # Run mongoimport commands
    mongo_import('air_quality', '/data/Project_sensor_data/air_quality_sensor_data.json')
    mongo_import('co2', '/data/Project_sensor_data/co2_sensor_data.json')
    mongo_import('humidity', '/data/Project_sensor_data/humidity_sensor_data.json')
    mongo_import('light_intensity', '/data/Project_sensor_data/light_intensity_sensor_data.json')
    mongo_import('room_facilities', '/data/Project_sensor_data/room_facilities_data.json')
    mongo_import('sound', '/data/Project_sensor_data/sound_sensor_data.json')
    mongo_import('temperature', '/data/Project_sensor_data/temperature_sensor_data.json')
    mongo_import('voc', '/data/Project_sensor_data/voc_sensor_data.json')

    print("MongoDB imports completed successfully.")
