CREATE DATABASE USERS;

CREATE TABLE user_id (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    current_weight DECIMAL(5,2) NOT NULL,
    goal_weight DECIMAL(5,2) NOT NULL,
    height DECIMAL(5,2) NOT NULL,
);

CREATE TABLE DIET (
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
