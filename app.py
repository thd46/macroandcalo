from flask import Flask, render_template
from flask_mysqldb import MySQL
from db_config import db_config
from flask import request
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, redirect, url_for



app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

app.config['MYSQL_HOST'] = db_config['host']
app.config['MYSQL_USER'] = db_config['user']
app.config['MYSQL_PASSWORD'] = db_config['password']
app.config['MYSQL_DB'] = db_config['database']

mysql = MySQL(app)

@app.route('/')
def home():
    return '<h1>Welcome to the Fitness Tracker!</h1><p>Visit /users to see users</p>'

@app.route('/users')
def users():
    cur = mysql.connection.cursor()
    cur.execute("SELECT username, current_weight, goal_weight FROM User")
    users = cur.fetchall()
    cur.close()
    return render_template('users.html', users=users)

@app.route('/search-food')
def search_food():
    query = request.args.get('q', '')
    print("🔎 Search query:", query)

    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT food_id, name, calories, protein, fat, carbs
        FROM FoodItem
        WHERE name LIKE %s
        LIMIT 25
    """, (f"%{query}%",))
    results = cur.fetchall()
    cur.close()

    cleaned = []
    for row in results:
        cleaned.append((
            row[0],
            row[1],
            float(row[2]),
            float(row[3]),
            float(row[4]),
            float(row[5])
        ))

    return render_template('search_food.html', results=cleaned, query=query)

@app.route('/log-meal/<int:food_id>', methods=['GET', 'POST'])
def log_meal(food_id):
    if request.method == 'POST':
        meal_type = request.form['meal_type']
        if 'user_id' not in session:
            return redirect(url_for('login'))
        user_id = session.get('user_id')
        date = '2025-05-28'  # or use datetime.date.today()
        calories = float(request.form['calories'])

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO Diet (user_id, date, meal_type, food_id, calories)
            VALUES (%s, CURRENT_DATE, %s, %s, %s)
        """, (user_id, meal_type, food_id, calories))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('search_food'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT name, calories FROM FoodItem WHERE food_id = %s", (food_id,))
    food = cur.fetchone()
    cur.close()

    if food is None:
        return f"Food with ID {food_id} not found", 404

    return render_template('log_meal.html', food=food, food_id=food_id)

@app.route('/my-meals')
def my_meals():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session.get('user_id')
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT d.date, d.meal_type, f.name, d.calories
        FROM Diet d
        JOIN FoodItem f ON d.food_id = f.food_id
        WHERE d.user_id = %s
        ORDER BY d.date DESC
    """, (user_id,))
    meals = cur.fetchall()
    cur.close()
    total_calories = sum([meal[3] for meal in meals])
    return render_template('my_meals.html', meals=meals, total=total_calories)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session.get('user_id')
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT 
            d.date,
            SUM(f.calories),
            SUM(f.protein),
            SUM(f.fat),
            SUM(f.carbs)
        FROM Diet d
        JOIN FoodItem f ON d.food_id = f.food_id
        WHERE d.user_id = %s
        GROUP BY d.date
        ORDER BY d.date DESC
    """, (user_id,))
    totals = cur.fetchall()
    cur.close()

    return render_template('dashboard.html', totals=totals)

@app.route('/meals-by-date/<date>')
def meals_by_date(date):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session.get('user_id')
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT d.diet_id, d.meal_type, f.name, d.calories
        FROM Diet d
        JOIN FoodItem f ON d.food_id = f.food_id
        WHERE d.user_id = %s AND d.date = %s
        ORDER BY FIELD(d.meal_type, 'breakfast', 'lunch', 'dinner', 'snack')
    """, (user_id, date))
    meals = cur.fetchall()
    cur.close()
    return render_template('meals_by_date.html', meals=meals, date=date)

@app.route('/delete-meal/<int:diet_id>', methods=['POST'])
def delete_meal(diet_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session.get('user_id')
    date = request.args.get('date')  # so we can redirect back to that day's page
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Diet WHERE diet_id = %s AND user_id = %s", (diet_id, user_id))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('meals_by_date', date=date))

@app.route('/edit-meal/<int:diet_id>', methods=['GET', 'POST'])
def edit_meal(diet_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session.get('user_id')
    date = request.args.get('date')

    cur = mysql.connection.cursor()

    if request.method == 'POST':
        new_meal_type = request.form['meal_type']
        new_calories = float(request.form['calories'])

        cur.execute("""
            UPDATE Diet
            SET meal_type = %s, calories = %s
            WHERE diet_id = %s AND user_id = %s
        """, (new_meal_type, new_calories, diet_id, user_id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('meals_by_date', date=date))

    cur.execute("""
        SELECT meal_type, calories FROM Diet
        WHERE diet_id = %s AND user_id = %s
    """, (diet_id, user_id))
    meal = cur.fetchone()
    cur.close()

    if not meal:
        return "Meal not found", 404

    return render_template('edit_meal.html', meal=meal, diet_id=diet_id, date=date)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_pw = generate_password_hash(password)

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM User WHERE username = %s", (username,))
        existing = cur.fetchone()

        if existing:
            cur.close()
            return "Username already exists!"

        cur.execute("""
            INSERT INTO User (username, password, current_weight, goal_weight, height)
            VALUES (%s, %s, 0, 0, 0)
        """, (username, hashed_pw))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_input = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT user_id, password FROM User WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user[1], password_input):
            session['user_id'] = user[0]
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return "Invalid username or password."

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        current_weight = request.form['current_weight']
        goal_weight = request.form['goal_weight']
        height = request.form['height']

        cur.execute("""
            UPDATE User
            SET current_weight = %s, goal_weight = %s, height = %s
            WHERE user_id = %s
        """, (current_weight, goal_weight, height, user_id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('profile'))

    cur.execute("SELECT current_weight, goal_weight, height FROM User WHERE user_id = %s", (user_id,))
    profile = cur.fetchone()
    cur.close()

    # BMI Calculation
    current_weight = profile[0]
    height = profile[2]

    if height and height > 0:
        bmi = round((current_weight / (height ** 2)) * 703, 1)
        if bmi < 18.5:
            category = "Underweight"
        elif 18.5 <= bmi < 25:
            category = "Normal weight"
        elif 25 <= bmi < 30:
            category = "Overweight"
        else:
            category = "Obese"
    else:
        bmi = None
        category = None

    return render_template('profile.html', profile=profile, bmi=bmi, category=category)

@app.route('/create-exercise-plan', methods=['GET', 'POST'])
def create_exercise_plan():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()

    if request.method == 'POST':
        plan_name = request.form['plan_name']
        selected_exercises = request.form.getlist('exercises')
        user_id = session['user_id']

        for exercise_id in selected_exercises:
            cur.execute("""
                INSERT INTO ExercisePlan (user_id, exercise_id, plan_name)
                VALUES (%s, %s, %s)     
            """, (user_id, exercise_id, plan_name))

        mysql.connection.commit()
        cur.close()
        return redirect(url_for('exercise_plans'))

    # GET: show all exercises to choose from
    cur.execute("SELECT exercise_id, name FROM Exercise ORDER BY name")
    exercises = cur.fetchall()
    cur.close()

    return render_template('exercise_planner.html', exercises=exercises)

@app.route('/exercise-plans')
def exercise_plans():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    cur = mysql.connection.cursor()

    # Get all exercises grouped by plan name
    cur.execute("""
        SELECT ep.plan_name, e.name, e.sets, e.reps, e.muscle_group, e.type, e.exercise_id
        FROM ExercisePlan ep
        JOIN Exercise e ON ep.exercise_id = e.exercise_id
        WHERE ep.user_id = %s
        ORDER BY ep.plan_name, e.name
    """, (user_id,))


    rows = cur.fetchall()
    cur.close()

    # Group exercises by plan name
    from collections import defaultdict
    plans = defaultdict(list)
    plan_timeframes = {}

    for row in rows:
        plan_name, name, sets, reps, muscle_group, ex_type, exercise_id = row
        plans[plan_name].append((name, sets, reps, muscle_group, ex_type, exercise_id))

    return render_template('exercise_plans.html', plans=plans, plan_timeframes=plan_timeframes)

@app.route('/delete-exercise-from-plan', methods=['POST'])
def delete_exercise_from_plan():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    exercise_id = request.form['exercise_id']
    plan_name = request.form['plan_name']

    cur = mysql.connection.cursor()
    cur.execute("""
        DELETE FROM ExercisePlan
        WHERE user_id = %s AND exercise_id = %s AND plan_name = %s
        LIMIT 1
    """, (user_id, exercise_id, plan_name))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('exercise_plans'))


if __name__ == '__main__':
    app.run(debug=True)
