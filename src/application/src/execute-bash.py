import subprocess

# Path to your bash script
bash_script_path = './import-data-windows.sh'

# Run the bash script using subprocess
try:
    result = subprocess.run(['bash', bash_script_path], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("Script executed successfully!")
    print("Output:")
    print(result.stdout.decode())  # Print standard output from the bash script
except subprocess.CalledProcessError as e:
    print(f"Error executing script: {e}")
    print("Error output:")
    print(e.stderr.decode())
