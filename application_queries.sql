-- NOTE THAT ALL '%s' IN THIS SCRIPT REPRESENT SPECIFIC VALUES DETERMINED BY USER INPUT

-- Render users onto the user page
SELECT username, current_weight, goal_weight FROM User;

-- Search the food database for foods matching the substring '%s' (user input)
SELECT food_id, name, calories, protein, fat, carbs
FROM FoodItem
WHERE name LIKE %s
LIMIT 25;

-- Add selected food into diet table for the specific user
INSERT INTO Diet (user_id, date, meal_type, food_id, calories)
VALUES (%s, %s, %s, %s, %s);

-- Fetch all added foods to a user's diet for display in the My Foods tab
SELECT d.date, d.meal_type, f.name, d.calories
FROM Diet d
JOIN FoodItem f ON d.food_id = f.food_id
WHERE d.user_id = %s
ORDER BY d.date DESC;

-- Fetch all added foods and the sum of calories/macros for display on the Dashboard tab
SELECT d.date, SUM(f.calories), SUM(f.protein), SUM(f.fat), SUM(f.carbs)
FROM Diet d
JOIN FoodItem f ON d.food_id = f.food_id
WHERE d.user_id = %s
GROUP BY d.date
ORDER BY d.date DESC;

-- For displaying the meals by date
SELECT d.diet_id, d.meal_type, f.name, d.calories
FROM Diet d
JOIN FoodItem f ON d.food_id = f.food_id
WHERE d.user_id = %s AND d.date = %s
ORDER BY FIELD(d.meal_type, 'breakfast', 'lunch', 'dinner', 'snack');

-- For deleting a specified food from the user's diet
DELETE FROM Diet 
WHERE diet_id = %s AND user_id = %s;

-- For updating a specified food in the user's diet
UPDATE Diet
SET meal_type = %s, calories = %s
WHERE diet_id = %s AND user_id = %s;

-- To update the display values of the meal after it was edited
SELECT meal_type, calories FROM Diet
WHERE diet_id = %s AND user_id = %s;

-- Check if the username has already been registered (the unique check is done on the application side)
SELECT * 
FROM User 
WHERE username = %s;

-- Register a new user into the User table
INSERT INTO User (username, password, current_weight, goal_weight, height)
VALUES (%s, %s, 0, 0, 0);

-- Log in a user (note password is hashed on application side, stored in the database as hashed text)
SELECT user_id, password FROM User WHERE username = %s;

-- Update the user's weight/height info in the user table
UPDATE User
SET current_weight = %s, goal_weight = %s, height = %s
WHERE user_id = %s;

-- To update the display of the user's weight/height info after updating that information in the table
SELECT current_weight, goal_weight, height 
FROM User 
WHERE user_id = %s;