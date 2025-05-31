import pandas as pd
import sqlite3

csv_path = "FoodItems/masterScrapedFoodItems.csv"
df = pd.read_csv(csv_path)
print(f"Loaded {len(df)} rows from CSV")

conn = sqlite3.connect("food_items.db")
cursor = conn.cursor()

df.to_sql("food_items", conn, if_exists="replace", index=False)
print("Data inserted into SQLite table 'food_items'")

sample = pd.read_sql_query("SELECT * FROM food_items LIMIT 5;", conn)
print("Sample from database:")
print(sample)

conn.close()