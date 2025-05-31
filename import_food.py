import pandas as pd
import MySQLdb
from db_config import db_config

df = pd.read_csv("FoodItems/cleanFoodItems.csv", quotechar='"', encoding='utf-8')

df.fillna({
    'description': '',
    'calories': 0,
    'protein': 0,
    'fat': 0,
    'carbs': 0
}, inplace=True)

conn = MySQLdb.connect(
    host=db_config['host'],
    user=db_config['user'],
    passwd=db_config['password'],
    db=db_config['database']
)
cursor = conn.cursor()

for index, row in df.iterrows():
    try:
        name = str(row['description']).strip().replace('\n', ' ').replace('\r', '')[:255]
        calories = row['calories'] if pd.notna(row['calories']) else 0
        protein = row['protein'] if pd.notna(row['protein']) else 0
        fat = row['fat'] if pd.notna(row['fat']) else 0
        carbs = row['carbs'] if pd.notna(row['carbs']) else 0
        servings = 1

        cursor.execute("""
            INSERT INTO FoodItem (name, calories, protein, fat, carbs, servings)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (name, calories, protein, fat, carbs, servings))

        if index % 50 == 0:
            print(f"Inserted row {index}: {name[:40]}...")

    except Exception as e:
        print(f"Skipped row {index} due to error: {e}")



conn.commit()
cursor.close() 
conn.close()

print("Food items imported successfully.")
