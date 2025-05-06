CREATE DATABASE FitnessTracker;

CREATE TABLE User (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    current_weight DECIMAL(5,2) NOT NULL,
    goal_weight DECIMAL(5,2) NOT NULL,
    height DECIMAL(5,2) NOT NULL
);

CREATE TABLE Diet (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    date DATE NOT NULL,
    meal_type ENUM('breakfast', 'lunch', 'dinner', 'snack') NOT NULL,
    food_item VARCHAR(100) NOT NULL,
    calories DECIMAL(5,2) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES USER(id)
);

CREATE TABLE Exercise (
	exercise_id	INTEGER NOT NULL, 	-- primary key
	name		VARCHAR(30),		-- name of exercise
	sets		INTEGER,		-- number of sets
	reps		INTEGER,		-- number of reps
	muscle_group	VARCHAR(40),		-- targeted muscle group(s)
	type		VARCHAR(20)		-- ie. cardio, weightlifting, aerobics, etc
	PRIMARY KEY (exercise_id)
);

CREATE TABLE ExercisePlan (
	plan_id		INTEGER NOT NULL,	-- primary key of the plan
	user_id		INTEGER NOT NULL,	-- foreign key
	exercise_id	INTEGER NOT NULL,	-- foreign key
	time_frame	DATE,			-- date of the end of the plan
	PRIMARY KEY (plan_id),
	FOREIGN KEY (user_id) REFERENCES User (user_id),
	FOREIGN KEY (exercise_id) REFERENCES Exercise (exercise_id)
);


CREATE TABLE FoodItem (
    food_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    calories INT,
    protein DECIMAL(5,2),
    fat DECIMAL(5,2),
    carbs DECIMAL(5,2),
    added_sugar DECIMAL(5,2),
    servings INT
);
