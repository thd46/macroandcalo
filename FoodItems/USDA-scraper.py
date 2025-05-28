import pandas as pd

try:
    food_df = pd.read_csv("FoodItems/USDA Food Data/food-main.csv", low_memory=False)
    food_nutrient_df = pd.read_csv("FoodItems/USDA Food Data/food_nutrient-main.csv", low_memory=False)
    nutrient_df = pd.read_csv("FoodItems/USDA Food Data/nutrient-main.csv", low_memory=False)
    portion_df = pd.read_csv("FoodItems/USDA Food Data/food_portion-main.csv", low_memory=False)
    print("All CSVs loaded successfully.")
except Exception as e:
    print(f"invalid file: {e}")
    exit()

# Nutrients we want to extract
target_nutrients = ["Energy", "Protein", "Total lipid (fat)", "Carbohydrate, by difference"]

# Get matching nutrient IDs
nutrient_ids = nutrient_df[nutrient_df["name"].isin(target_nutrients)][["id", "name"]]
print("Target nutrient IDs found:\n", nutrient_ids)

# Merge nutrients with food descriptions
merged = food_nutrient_df.merge(nutrient_ids, left_on="nutrient_id", right_on="id")
merged = merged.merge(food_df[["fdc_id", "description"]], on="fdc_id")

# Pivot to get each nutrient as a column
pivot = merged.pivot_table(
    index=["fdc_id", "description"],
    columns="name",
    values="amount"
).reset_index()

# Rename columns to match your DB
pivot = pivot.rename(columns={
    "Energy": "calories",
    "Protein": "protein",
    "Total lipid (fat)": "fat",
    "Carbohydrate, by difference": "carbs"
})

trimmed = pivot[["description", "calories", "protein", "fat", "carbs"]]

trimmed.to_csv("FoodItems/cleanFoodItems.csv", index=False)

print("Finished writing FoodItems/cleanFoodItems.csv")
print("Longest description length:", trimmed['description'].astype(str).str.len().max())