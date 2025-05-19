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

target_nutrients = ["Energy", "Protein", "Total lipid (fat)", "Carbohydrate, by difference"]

nutrient_ids = nutrient_df[nutrient_df["name"].isin(target_nutrients)][["id", "name"]]
print("Target nutrient IDs found:\n", nutrient_ids)

merged = food_nutrient_df.merge(nutrient_ids, left_on="nutrient_id", right_on="id")
merged = merged.merge(food_df[["fdc_id", "description"]], on="fdc_id")

pivot = merged.pivot_table(
    index=["fdc_id", "description"],
    columns="name",
    values="amount"
).reset_index()

pivot = pivot.rename(columns={
    "Energy": "calories",
    "Protein": "protein",
    "Total lipid (fat)": "fat",
    "Carbohydrate, by difference": "carbs"
})

portion_clean = portion_df.groupby("fdc_id").first().reset_index()
pivot = pivot.merge(portion_clean[["fdc_id", "portion_description", "gram_weight"]], on="fdc_id", how="left")

pivot.to_csv("FoodItems/masterScrapedFoodItems.csv", index=False)


