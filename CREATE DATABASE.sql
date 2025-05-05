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