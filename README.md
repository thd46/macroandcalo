# 🏋️‍♂️ Health and Fitness Tracker

## 📋 Project Summary

The **Health and Fitness Tracker** is a comprehensive database system designed to help users monitor their daily food intake and exercise routines. This system allows individuals to log and manage personal health data, including current and goal weight, dietary habits, and structured workout plans.

Built to support web-based data integration—such as nutritional data from the USDA Food Data Central—the system combines reliable external sources with user-provided information to enable a personalized fitness tracking experience. Users can log meals, track macronutrients, and follow customized workout routines tailored to their fitness goals.

### 🔍 Key Features:
- **User Profiles**: Store login credentials and essential metrics like weight, height, and fitness goals.
- **Diet Tracking**: Daily food diaries linked to comprehensive nutrition data, including calories, protein, fats, and carbs.
- **Exercise Plans**: Structured workout programs composed of exercises grouped by sets, reps, muscle group, and type (e.g., lifting or cardio).
- **Progress Monitoring**: Track weight changes over time and adjust plans accordingly.
- **Relational Database Design**: A normalized schema linking users, diet logs, food items, exercises, and workout plans efficiently.

This system forms the backend foundation for a potential web or mobile application to empower users to take control of their health journey through consistent and informed tracking.

- Connects Flask to a MySQL database
- Parses and cleans USDA food CSVs
- Imports over 1.8 million food items
- Has a working /users route that pulls user data from MySQL

1. Clone the repo and open it in VS Code

2. Run:
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt

3. Set up MySQL and run the schema to create all tables

      mysql -u root -p < CREATE_DATABASE.sql

4. Edit db_config.py with your MySQL password

5. Run the scraper:
   python FoodItems/USDA-scraper.py

6. Import the cleaned CSVs (Exercises and Foods):
   python import_to_db.py

7. Start the app:
   python app.py

**NOTE THE FOLLOWING** 
- You only need to run the import once (it’s slow)
- cleanFoodItems.csv is already prepared after running the scraper
- Don’t forget to activate your venv every time


BTW MAKE SURE YOU RUN THE QUERIES IN TEST.SQL, THIS WILL EXPAND THE VALUES.