import pandas as pd

food_df = pd.read_csv("FoodItems/USDA Food Data/food.csv")
nutrient_df = pd.read_csv("FoodItems/USDA Food Data/food_nutrient.csv", low_memory=False)
portion_df = pd.read_csv("FoodItems/USDA Food Data/food_portion.csv")

nutrient_ids = {
    1008: 'calories',
    1003: 'protein',
    1004: 'fat',
    1005: 'carbs'
}

nutrient_filtered = nutrient_df[nutrient_df['nutrient_id'].isin(nutrient_ids.keys())].copy()
nutrient_filtered['nutrient_name'] = nutrient_filtered['nutrient_id'].map(nutrient_ids)
nutrient_pivot = nutrient_filtered.pivot_table(
    index='fdc_id',
    columns='nutrient_name',
    values='amount',
    aggfunc='first'
).reset_index()

portion_simplified = portion_df[['fdc_id', 'gram_weight']].dropna().drop_duplicates('fdc_id')

merged_df = food_df[['fdc_id', 'description']].merge(nutrient_pivot, on='fdc_id', how='inner')
merged_df = merged_df.merge(portion_simplified, on='fdc_id', how='left')

final_df = merged_df.rename(columns={
    'description': 'name',
    'gram_weight': 'servings'
})
final_df = final_df[['name', 'calories', 'protein', 'fat', 'carbs', 'servings']]
final_df = final_df.dropna(subset=['calories']).head(500)

final_df.to_csv("FoodItems/scrapedFoodItems.csv", index=False)
