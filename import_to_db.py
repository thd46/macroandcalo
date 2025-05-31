import subprocess

print("Importing food items...")
subprocess.run(["python3", "import_food.py"], check=True)

print("Importing exercise items...")
subprocess.run(["python3", "import_exercises.py"], check=True)

print("All data imported successfully.")
