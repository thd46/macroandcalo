import pandas as pd
import MySQLdb
from db_config import db_config

# Load the detailed exercise CSV
df = pd.read_csv("Exercises/exercises_full_variations.csv")

df.fillna('', inplace=True)

# Connect to MySQL
conn = MySQLdb.connect(
    host=db_config['host'],
    user=db_config['user'],
    passwd=db_config['password'],
    db=db_config['database']
)
cursor = conn.cursor()

# Insert each row into the Exercise table
for index, row in df.iterrows():
    try:
        cursor.execute("""
            INSERT INTO Exercise (name, sets, reps, muscle_group, type)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            row['name'],
            int(row['sets']),
            int(row['reps']),
            row['muscle_group'],
            row['type']
        ))

        if index % 20 == 0:
            print(f"Inserted row {index}: {row['name']}")

    except Exception as e:
        print(f"⚠️ Skipped row {index} due to error: {e}")

conn.commit()
cursor.close()
conn.close()

print("Exercise data imported successfully.")
