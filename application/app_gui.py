from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QStyleFactory

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, this_window="login"):
        # Initialize parent class
        super().__init__()

        self.setWindowTitle("GUI Design")

        # Create the login widgets
        self.li_label = QtWidgets.QLabel("Login")
        self.li_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)

        self.username_label = QtWidgets.QLabel("Username:")
        self.username_field = QtWidgets.QLineEdit()
        self.username_field.setPlaceholderText("Enter username...")

        self.password_label = QtWidgets.QLabel("Password:")
        self.password_field = QtWidgets.QLineEdit(echoMode=QtWidgets.QLineEdit.EchoMode.Password)
        self.password_field.setPlaceholderText("Enter password...")

        self.signup_button = QtWidgets.QPushButton("Create Account")
        self.login_button = QtWidgets.QPushButton("Log In")

        # Create the macros widgets
        self.mealtype_slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.mealtype_slider.setMinimum(0)
        self.mealtype_slider.setMaximum(2)
        self.mealtype_slider.setValue(0)
        self.mealtype_slider.valueChanged.connect(self.slider_update)

        self.mealtype_label = QtWidgets.QLabel("Breakfast")

        self.food_search_bar = QtWidgets.QLineEdit()
        self.food_search_bar.setPlaceholderText("Search for food to add...")
        self.food_search_button = QtWidgets.QPushButton("Search")

        self.calories_label = QtWidgets.QLabel("Calories")
        self.calories_value = QtWidgets.QLabel("{}".format(1500))
        self.calories_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.calories_value.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignTop)

        self.protein_label = QtWidgets.QLabel("Protein")
        self.protein_value = QtWidgets.QLabel("{}".format(90.0))
        self.protein_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.protein_value.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignTop)

        self.carbs_label = QtWidgets.QLabel("Carbs")
        self.carbs_value = QtWidgets.QLabel("{}".format(82.5))
        self.carbs_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.carbs_value.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignTop)

        self.fat_label = QtWidgets.QLabel("Fat")
        self.fat_value = QtWidgets.QLabel("{}".format(51.0))
        self.fat_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.fat_value.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignTop)

        self.added_foods_list = QtWidgets.QListWidget()
        self.added_foods_list.addItems(["Sample Food 1", "Sample Food 2"])
        self.added_foods_label = QtWidgets.QLabel("Added Foods")

        #Create the exercise plan widgets
        self.plan_droplist = QtWidgets.QComboBox()
        self.plan_droplist.addItems(["Plan 1", "Plan 2"])
        self.exercise_list = QtWidgets.QListWidget()
        self.exercise_list.addItems(["Pushups", "Squats", "Treadmill"])

        self.plan_info = QtWidgets.QGroupBox(f"Selected Exercise: {'Pushups'}")
        self.exercise_label = QtWidgets.QLabel("Pushups", self.plan_info)
        self.sets_label = QtWidgets.QLabel(f"Sets: {3}", self.plan_info)
        self.reps_label = QtWidgets.QLabel(f"Reps: {8}", self.plan_info)
        self.musclegroup_label = QtWidgets.QLabel(f"Muscle Group: Chest", self.plan_info)

        plan_info_grid = QtWidgets.QGridLayout()
        plan_info_grid.addWidget(self.exercise_label, 0, 0)
        plan_info_grid.addWidget(self.sets_label, 1, 0)
        plan_info_grid.addWidget(self.reps_label, 2, 0)
        plan_info_grid.addWidget(self.musclegroup_label, 3, 0)
        self.plan_info.setLayout(plan_info_grid)

        # Create the grid
        self.meta_grid = QtWidgets.QGridLayout()
        self.grid_layout = QtWidgets.QGridLayout()


        # Add widgets to the grid (currently dependent on the input of this_window)
        if this_window == "login":
            # Set the grid_layout
            self.build_login_screen()
            self.setWindowTitle("Login Screen")

            # Set the grid to the window
            empty_widget = QtWidgets.QWidget()
            self.meta_grid.addWidget(empty_widget, 2, 2)

            placeholder_inner = QtWidgets.QWidget()
            placeholder_inner.setLayout(self.grid_layout)

            placeholder_outer = QtWidgets.QWidget()
            placeholder_outer.setLayout(self.meta_grid)

            self.meta_grid.addWidget(placeholder_inner, 1, 1)
            self.setCentralWidget(placeholder_outer)

        elif this_window == "counting":
            self.build_counting_screen()
            self.setWindowTitle("Counting Screen")

            placeholder_outer = QtWidgets.QWidget()
            placeholder_outer.setLayout(self.grid_layout)
            self.setCentralWidget(placeholder_outer)

        elif this_window == "plan":
            self.build_plan_screen()
            self.setWindowTitle("Exercise Plan Screen")

            placeholder_outer = QtWidgets.QWidget()
            placeholder_outer.setLayout(self.grid_layout)
            self.setCentralWidget(placeholder_outer)

    def build_login_screen(self):
        self.grid_layout.addWidget(self.li_label, 0, 0, 1, 2)
        self.grid_layout.addWidget(self.username_label, 1, 0)
        self.grid_layout.addWidget(self.username_field, 1, 1)
        self.grid_layout.addWidget(self.password_label, 2, 0)
        self.grid_layout.addWidget(self.password_field, 2, 1)
        self.grid_layout.addWidget(self.signup_button, 3, 0)
        self.grid_layout.addWidget(self.login_button, 3, 1)

    def build_counting_screen(self):
        self.grid_layout.addWidget(self.mealtype_slider, 0, 1, 1, 4)
        self.grid_layout.addWidget(self.mealtype_label, 0, 0)

        self.grid_layout.addWidget(self.food_search_bar, 1, 0, 1, 3)
        self.grid_layout.addWidget(self.food_search_button, 1, 3)

        self.grid_layout.addWidget(self.calories_label, 2, 0)
        self.grid_layout.addWidget(self.calories_value, 3, 0)

        self.grid_layout.addWidget(self.protein_label, 2, 1)
        self.grid_layout.addWidget(self.protein_value, 3, 1)

        self.grid_layout.addWidget(self.carbs_label, 2, 2)
        self.grid_layout.addWidget(self.carbs_value, 3, 2)

        self.grid_layout.addWidget(self.fat_label, 2, 3)
        self.grid_layout.addWidget(self.fat_value, 3, 3)

        self.grid_layout.addWidget(self.added_foods_label, 0, 5, 1, 1)
        self.grid_layout.addWidget(self.added_foods_list, 1, 5, 3, 3)

    def build_plan_screen(self):
        self.grid_layout.addWidget(self.plan_droplist, 0, 0, 1, 2)
        self.grid_layout.addWidget(self.exercise_list, 1, 0, 2, 2)
        self.grid_layout.addWidget(self.plan_info, 0, 2, 3, 2)

    def slider_update(self):
        if self.mealtype_slider.value() == 0:
            self.mealtype_label.setText("Breakfast")
        elif self.mealtype_slider.value() == 1:
           self.mealtype_label.setText("Lunch")
        else:
            self.mealtype_label.setText("Dinner")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow("plan")

    print(QStyleFactory.keys())

    app.setStyle("Fusion")

    window.show()
    app.exec()
