####### Imports #######
import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import sqlite3
import subprocess
import customtkinter
from tkinter import messagebox
import re

customtkinter.set_appearance_mode("Dark")

####### Functions #######
# Function that chnages details on button press
def change_details():
    email = email_value_entry.get()
    password = password_value_entry.get()
    dob = dob_value_entry.get()
    pr_squat = pr_squat_value_entry.get()
    pr_bench = pr_bench_value_entry.get()
    pr_deadlift = pr_deadlift_value_entry.get()

    # Validation
    # Field check
    if (
        not email
        or not password
        or not dob
        or not pr_squat
        or not pr_bench
        or not pr_deadlift
    ):
        messagebox.showerror(
            "Data Error",
            "Error: Please enter all fields before changing values! Re-enter data if want to keep the same.",
        )
        return

    #Email check pattern taken from external source
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    if not re.match(email_pattern, email):
        messagebox.showerror(
            "Data Error",
            "Error: Invalid email format. Please enter a valid email address.",
        )
        return

    # Validate date of birth format (dd/mm/yyyy) pattern taken from an external source
    dob_pattern = r"^(0[1-9]|[1-2]\d|3[0-1])/(0[1-9]|1[0-2])/((19[6-9]\d|20\d{2}))$"
    if not re.match(dob_pattern, dob):
        messagebox.showerror(
            "Data Error",
            "Error: Invalid date of birth format. Please use the format dd/mm/yyyy. DOB has to be withn 100 years of 2023.",
        )
        return

    pr_squat = float(pr_squat)  # Convert pr_squat to a float
    pr_bench = float(pr_bench)  # Convert pr_bench to a float
    pr_deadlift = float(pr_deadlift)  # Convert pr_deadlift to a float

    # Weight entered validation
    if (
        pr_squat > 300
        or pr_bench > 300
        or pr_deadlift > 300
        or pr_squat < 0
        or pr_bench < 0
        or pr_deadlift < 0
        or pr_squat == 0
        or pr_bench == 0
        or pr_deadlift == 0
    ):
        messagebox.showerror(
            "Data Error",
            "Error: Weight limit exceeded. Please enter weights below 300kg and above 0kg.",
        )
        return

    conn = sqlite3.connect("user_details.db")
    cursor = conn.cursor()

    # Update the row with the extracted name
    cursor.execute(
        "UPDATE users SET email=?, password=?, dob=?, pr_squat=?, pr_bench=?, pr_deadlift=? WHERE name=?",
        (email, password, dob, pr_squat, pr_bench, pr_deadlift, name),
    )

    # Print the rows
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    # Close the connection
    conn.commit()
    conn.close()

    change_weights()


# Get the name from the existing row
# Function that changes the weights in the database when the change_detail function is done
def change_weights():
    pr_squat = int(pr_squat_value_entry.get())
    pr_bench = int(pr_bench_value_entry.get())
    pr_deadlift = int(pr_deadlift_value_entry.get())

    workout_variable_list = [
        ("Calf Raises", 2),
        ("Leg-Press", 1.2),
        ("Squat", 1.4),
        ("Walking Lunges", 3),
        ("Leg Extension", 3),
        ("Hack Squat", 2.5),
        ("Romanian Deadlift", 1.5),
        ("Deadlift", 1.4),
        ("Hamstring Curl", 3),
        ("Split", 150),
        ("Bicep Curl", 8),
        ("Ben-Over Rows", 5),
        ("Hammer Curl", 6.5),
        ("Dips", 1),
        ("Push-Downs", 9),
        ("Tricep Extension", 9),
        ("Shoulder Press", 8),
        ("Lateral Raises", 10),
        ("Incline Bicep Curl", 12),
        ("Pull-Ups", 1),
        ("Split", 150),
        ("Bench-Press", 1.5),
        ("Chest-Fly", 2.5),
        ("Push-Ups", 1),
        ("Cable Crossovers", 4),
        ("Tricep Extension", 4),
        ("Chest Dip", 1),
        ("Overhead Press", 5),
        ("Wide Grip Bench-Press", 1.7),
        ("Decline Push-Ups", 1),
    ]

    conn = sqlite3.connect("workouts.db")
    cursor = conn.cursor()

    workout_variable = 0  # Initialize workout_variable before the loop
    # Update weights for legs depending on the weights in the pr slots (works)
    for row in workout_variable_list:
        if row[-1] < 20:
            workout_variable = row[-1]
            weight_legs = pr_squat / workout_variable
            rounded_legs = round(weight_legs)
            workout_name = row[0]
            cursor.execute(
                "UPDATE workouts SET weight=? WHERE name=?",
                (rounded_legs, workout_name),
            )
        else:
            break

    # Update weights for chest exercises starting from the 21st row
    for index in range(21, len(workout_variable_list)):
        exercise = workout_variable_list[index]
        if exercise[-1] < 20:
            workout_variable = exercise[-1]
            weight_chest = pr_bench / workout_variable
            rounded_chest = round(weight_chest)
            workout_name = exercise[0]
            cursor.execute(
                "UPDATE workouts SET weight=? WHERE name=?",
                (rounded_chest, workout_name),
            )
        else:
            break

    # Update weights for arm exercises starting from the 11th row ending at 20th
    for index in range(10, len(workout_variable_list)):
        work = workout_variable_list[index]
        if work[-1] < 20:
            workout_variable = work[-1]
            weight_arms = pr_deadlift / workout_variable
            rounded_arms = round(weight_arms)
            workout_name = work[0]
            cursor.execute(
                "UPDATE workouts SET weight=? WHERE name=?",
                (rounded_arms, workout_name),
            )
        else:
            break

    # Set values for reps and sets
    reps_legs = 12
    sets_legs = 4

    reps_arms = 15
    sets_arms = 3

    reps_chest = 8
    sets_chest = 4

    # Update the reps value for the "legs" type in the workout table
    cursor.execute("UPDATE workouts SET reps=? WHERE type=?", (reps_legs, "Legs"))
    cursor.execute("UPDATE workouts SET sets=? WHERE type=?", (sets_legs, "Legs"))

    cursor.execute("UPDATE workouts SET reps=? WHERE type=?", (reps_chest, "Chest"))
    cursor.execute("UPDATE workouts SET sets=? WHERE type=?", (sets_chest, "Chest"))

    cursor.execute("UPDATE workouts SET reps=? WHERE type=?", (reps_arms, "Arms"))
    cursor.execute("UPDATE workouts SET sets=? WHERE type=?", (sets_arms, "Arms"))

    conn.commit()
    conn.close()

    # Clear the entry fields
    email_value_entry.delete(0, END)
    password_value_entry.delete(0, END)
    dob_value_entry.delete(0, END)
    pr_squat_value_entry.delete(0, END)
    pr_bench_value_entry.delete(0, END)
    pr_deadlift_value_entry.delete(0, END)


conn = sqlite3.connect("user_details.db")
cursor = conn.cursor()
cursor.execute("SELECT name FROM users")
row = cursor.fetchone()
if row is not None:
    name = row[0]
else:
    name = ""

#Menu functions
def go_to_homepage():
    root.destroy()
    subprocess.Popen(["python", "Program_Home_page.py"])


def go_to_datapage():
    root.destroy()
    subprocess.Popen(["python", "Program_Data_page.py"])


def go_to_informationpage():
    root.destroy()
    subprocess.Popen(["python", "Program_Information_page.py"])


####### GUI code #######
conn = sqlite3.connect("user_details.db")
cursor = conn.cursor()


# Print the rows
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
for row in rows:
    print(row)

# GUI code
root = Tk()
root.geometry("640x960")
root.title("Data page")
root.resizable(width=False, height=False)

# Background
background_image = tk.PhotoImage(file="assets/Project Walpaper.png")
background_label = ttk.Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Title
info_title = ttk.Label(root, text="Edit Info:", font=("Helvetica", 30))
info_title.grid(row=0, column=1, columnspan=3, padx=25, pady=20, sticky="NW")

# Frame for Data entry fields
data_frame = ttk.LabelFrame(root)
data_frame.grid(row=1, column=0, columnspan=3, padx=10)

# Label for each field need to be entered and Entry for each
email_label = ttk.Label(data_frame, text="Email:", font=("Helvetica", 16))
email_label.grid(row=1, column=0, padx=30, pady=10)

password_label = ttk.Label(data_frame, text="Password:", font=("Helvetica", 16))
password_label.grid(row=2, column=0, padx=30, pady=10)

dob_label = ttk.Label(data_frame, text="Date of Birth:", font=("Helvetica", 16))
dob_label.grid(row=3, column=0, padx=30, pady=10)

pr_squat_label = ttk.Label(data_frame, text="PR Squat:", font=("Helvetica", 16))
pr_squat_label.grid(row=4, column=0, padx=30, pady=10)

pr_bench_label = ttk.Label(data_frame, text="PR Bench:", font=("Helvetica", 16))
pr_bench_label.grid(row=5, column=0, padx=30, pady=10)

pr_deadlift_label = ttk.Label(data_frame, text="PR Deadlift:", font=("Helvetica", 16))
pr_deadlift_label.grid(row=6, column=0, padx=30, pady=10)

email_value_entry = ttk.Entry(data_frame)
email_value_entry.grid(row=1, column=1, padx=20)

password_value_entry = ttk.Entry(data_frame)
password_value_entry.grid(row=2, column=1, padx=20)

dob_value_entry = ttk.Entry(data_frame)
dob_value_entry.grid(row=3, column=1, padx=20)

pr_squat_value_entry = ttk.Entry(data_frame)
pr_squat_value_entry.grid(row=4, column=1, padx=20)

pr_bench_value_entry = ttk.Entry(data_frame)
pr_bench_value_entry.grid(row=5, column=1, padx=20)

pr_deadlift_value_entry = ttk.Entry(data_frame)
pr_deadlift_value_entry.grid(row=6, column=1, padx=20)

# Radio button frame
importance_frame = ttk.LabelFrame(root)
importance_frame.grid(row=2, column=0, columnspan=3, pady=10, padx=38)

importance_label = ttk.Label(
    importance_frame, text="Importance:", font=("Helvetica", 16)
)
importance_label.grid(row=0, column=0, columnspan=1, padx=10, pady=10)

# Create a variable to hold choice in
preference_choice = StringVar()

# Create the different choices of the radio button
radio_button_strength = ttk.Radiobutton(
    importance_frame,
    text="Want to improve my overall strength in the gym!",
    variable=preference_choice,
    value="Option 1",
)
radio_button_strength.grid(row=0, column=3, padx=10, pady=10, sticky="NW")

radio_button_recovery = ttk.Radiobutton(
    importance_frame,
    text="Want to recover from a recent injury!",
    variable=preference_choice,
    value="Option 2",
)
radio_button_recovery.grid(row=1, column=3, padx=10, pady=10, sticky="NW")

radio_button_endurance = ttk.Radiobutton(
    importance_frame,
    text="Want to improve my muscular endurance through longer sets!",
    variable=preference_choice,
    value="Option 3",
)
radio_button_endurance.grid(row=2, column=3, padx=10, pady=10, sticky="NW")

# submit button
change_button = customtkinter.CTkButton(
    root, text="Change", command=change_details, fg_color=("black", "black")
)
change_button.grid(row=3, column=1, columnspan=3, pady=20, padx=80, sticky="W")

# menu
menu_frame = ttk.Frame(root)
menu_frame.grid(sticky="S", columnspan=1, column=1, row=5, pady=25)

# Load the images for the menu items
data_image1 = Image.open("assets/Data logo menu.png")
data_image1 = data_image1.resize((40, 40))
data_photo1 = ImageTk.PhotoImage(data_image1)

home_image2 = Image.open("assets/DDT logo homepage.png")
home_image2 = home_image2.resize((40, 40))
home_photo2 = ImageTk.PhotoImage(home_image2)

information_image3 = Image.open("assets/Information logo menu.png")
information_image3 = information_image3.resize((40, 40))
information_photo3 = ImageTk.PhotoImage(information_image3)

# Create menu buttons with images
button1 = ttk.Button(menu_frame, image=data_photo1, command=go_to_datapage)
button1.grid(column=0, row=0)

button2 = ttk.Button(menu_frame, image=home_photo2, command=go_to_homepage)
button2.grid(column=1, row=0)

button3 = ttk.Button(
    menu_frame, image=information_photo3, command=go_to_informationpage
)
button3.grid(column=2, row=0)

root.mainloop()
