-- NOTE THAT ALL IMPORTING IS HANDLED VIA PYTHON GIVEN THE SHEAR SIZE OF THE DATA 
-- WE ARE IMPORTING (OVER 1.8 MILLION FOOD ITEMS), THESE QUERIES ARE SIMPLY WHAT THE PYTHON 
-- PROGRAMS ARE USING TO IMPORT THE DATA INTO OUR DATABASE IN THE GENERIC CASE

-- IN ORDER TO ACTUALLY IMPORT THE DATA INTO THE DATABASE, PLEASE RUN *** import_to_db.py ***

-- Insert a given row from CleanFoodItems.csv into the FoodItem table (note that the all the %s represent
-- the values of the row for name, calories, protein, etc.)
INSERT INTO FoodItem (name, calories, protein, fat, carbs, servings)
VALUES (%s, %s, %s, %s, %s, %s);

-- Insert a given row from exercises_full_variations.csv into the Exercise table (again, note that all the %s
-- represent the values of the row)
INSERT INTO Exercise (name, sets, reps, muscle_group, type)
VALUES (%s, %s, %s, %s, %s);