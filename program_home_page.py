"""This homepage is the page the user lands on after the login/sign-up page.
This page is the main page the user can access the other pages from.
This page u can generate random workouts from a set catagory"""

import tkinter as tk
from tkinter import *
from tkinter import ttk
import sqlite3
import subprocess
import random
from tkinter import messagebox
import customtkinter
from PIL import Image, ImageTk

customtkinter.set_appearance_mode("Dark")

# Connect to database
conn = sqlite3.connect("user_details.db")
cursor = conn.cursor()

# Print the rows
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
for row in rows:
    print(row)

# Close the connection
conn.commit()
conn.close()

####### Functions #######
class User:
    """This class and object is only used to display the name ,which the user entered, om the homepage."""
    def __init__(self, name):
        self.name = name


def generate_legs():
    """This function will grab a random workout from the Legs catagory. 
    This workout will then be displayed in the form of an error message."""
    # Connect to the SQLite database
    conn = sqlite3.connect("workouts.db")
    cursor = conn.cursor()

    # Fetch all the workouts of the "Legs" category from the table
    cursor.execute(
        "SELECT name, type, reps, weight, sets FROM workouts WHERE type=?", ("Legs",)
    )
    legs_workouts = cursor.fetchall()

    random_workout_legs = random.choice(legs_workouts)

    workout_name, workout_type, reps, weight, sets = random_workout_legs
    message = f"Name: {workout_name}\nType:\
          {workout_type}\nReps: {reps}\nWeight: {weight}\nSets: {sets}"
    messagebox.showinfo("Generated Workout", message)

    # Close the connection
    conn.close


def generate_arms():
    """This function will grab a random workout from the Arms catagory. 
    This workout will then be displayed in the form of an error message."""
    # Connect to the SQLite database
    conn = sqlite3.connect("workouts.db")
    cursor = conn.cursor()

    # Fetch all the workouts of the "Legs" category from the table
    cursor.execute(
        "SELECT name, type, reps, weight, sets FROM workouts WHERE type=?", ("Arms",)
    )
    arms_workouts = cursor.fetchall()

    random_workout_arms = random.choice(arms_workouts)

    workout_name, workout_type, reps, weight, sets = random_workout_arms
    message = f"Name: {workout_name}\nType: {workout_type}\nReps: {reps}\nWeight: {weight}\nSets: {sets}"
    messagebox.showinfo("Generated Workout", message)
    conn.close


def generate_chest():
    """This function will grab a random workout from the Chest catagory. 
    This workout will then be displayed in the form of an error message."""
    # Connect to the SQLite database
    conn = sqlite3.connect("workouts.db")
    cursor = conn.cursor()

    # Fetch all the workouts of the "Legs" category from the table
    cursor.execute(
        "SELECT name, type, reps, weight, sets FROM workouts WHERE type=?", ("Chest",)
    )
    chest_workouts = cursor.fetchall()

    random_workout_chest = random.choice(chest_workouts)

    workout_name, workout_type, reps, weight, sets = random_workout_chest
    message = f"Name: {workout_name}\nType: {workout_type}\nReps: {reps}\nWeight: {weight}\nSets: {sets}"
    messagebox.showinfo("Generated Workout", message)
    conn.close


# Menu
def go_to_homepage():
    """Function when used closes the current page and opens homepage."""
    root.destroy()
    subprocess.Popen(["python", "Program_Home_page.py"])


def go_to_datapage():
    """Function when used closes the current page and opens datapage."""
    root.destroy()
    subprocess.Popen(["python", "Program_Data_page.py"])


def go_to_informationpage():
    """Function when used closes the current page and opens informationpage."""
    root.destroy()
    subprocess.Popen(["python", "Program_Information_page.py"])


####### GUI Code #######
root = Tk()
root.geometry("640x960")
root.title("Home page")
root.resizable(width=False, height=False)

# Background
background_image = tk.PhotoImage(file="assets/Project Walpaper.png")
background_label = ttk.Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Ttile
title_frame = ttk.LabelFrame(root)
title_frame.grid(row=0, column=1, pady=10, padx=10, sticky="NW")

app_title = ttk.Label(title_frame, text="iGym", font=("Arial", 20))
app_title.grid(row=1, column=2, sticky="NESW", pady=5, padx=20)

# Logo next to title
logo_pic = Image.open("assets/DDT logo homepage.png")
resized = logo_pic.resize((50, 50), Image.ANTIALIAS)
logo_final_pic = ImageTk.PhotoImage(resized)

logo_image_label = Label(title_frame, image=logo_final_pic)
logo_image_label.grid(row=1, column=1, padx=10, pady=7)

# Connect to the user_details database
conn = sqlite3.connect("user_details.db")
cursor = conn.cursor()

# Execute an SQL statement to retrieve the user's name
cursor.execute("SELECT name FROM users")
name = cursor.fetchone()[0]

# Close the database connection
conn.close()

# Create a User instance and set the name attribute
user = User(name)

# Welcome label with username next to it
welcome_label_text = "Let's get started, " + user.name + "!"
welcome_message = ttk.Label(root, text=welcome_label_text, font=("Arial", 18))
welcome_message.grid(row=3, column=1, sticky="NW")

# Frame for legs
legs_frame = ttk.LabelFrame(root)
legs_frame.grid(row=4, column=1)

# Label for legs
legs_label_home = ttk.Label(legs_frame, text="Workout for Legs", wraplength=250)
legs_label_home.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

# Picture for legs
legs_pic = Image.open("assets/Legs Image homepage.jpg")
resized = legs_pic.resize((250, 170), Image.ANTIALIAS)
legs_final_pic = ImageTk.PhotoImage(resized)

legs_image_label = Label(root, image=legs_final_pic)
legs_image_label.grid(row=4, column=0, padx=10, pady=5)

# Generate button for legs
generate_button_legs = customtkinter.CTkButton(
    legs_frame, text="Generate", command=generate_legs, fg_color=("black", "black")
)
generate_button_legs.grid(row=2, column=1, columnspan=1)

# Frame for arms
arms_frame = ttk.LabelFrame(root)
arms_frame.grid(row=6, column=1)

# Label for arms
arms_label_home = ttk.Label(arms_frame, text="Workout for Arms", wraplength=250)
arms_label_home.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

# Picture for arms
arms_pic = Image.open("assets/Arms Image homepage.jpg")
resized = arms_pic.resize((250, 170), Image.ANTIALIAS)
arms_final_pic = ImageTk.PhotoImage(resized)

arms_image_label = Label(root, image=arms_final_pic)
arms_image_label.grid(row=6, column=0, padx=10, pady=5)

# Gnerate button for arms
generate_button_arms = customtkinter.CTkButton(
    arms_frame, text="Generate", command=generate_arms, fg_color=("black", "black")
)
generate_button_arms.grid(row=2, column=1, columnspan=1)

# Frame for chest
chest_frame = ttk.LabelFrame(root)
chest_frame.grid(row=7, column=1)

# Label for chest
chest_label_home = ttk.Label(chest_frame, text="Workout for Chest", wraplength=250)
chest_label_home.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

# Picture for chest
chest_pic = Image.open("assets/Chest Image homepage.jpg")
resized = chest_pic.resize((250, 170), Image.ANTIALIAS)
chest_final_pic = ImageTk.PhotoImage(resized)

chest_image_label = Label(root, image=chest_final_pic)
chest_image_label.grid(row=7, column=0, padx=10, pady=5)

# Generate button for chest
generate_button_chest = customtkinter.CTkButton(
    chest_frame, text="Generate", command=generate_chest, fg_color=("black", "black")
)
generate_button_chest.grid(row=2, column=1, columnspan=1)

# Menu
# Menu picture for each page
menu_frame = customtkinter.CTkFrame(root)
menu_frame.grid(sticky="SW", columnspan=1, column=1, row=8, pady=60)

data_image1 = Image.open("assets/Data logo menu.png")
data_image1 = data_image1.resize((40, 40))
data_photo1 = ImageTk.PhotoImage(data_image1)

home_image2 = Image.open("assets/DDT logo homepage.png")
home_image2 = home_image2.resize((40, 40))
home_photo2 = ImageTk.PhotoImage(home_image2)

information_image3 = Image.open("assets/Information logo menu.png")
information_image3 = information_image3.resize((40, 40))
information_photo3 = ImageTk.PhotoImage(information_image3)

# Button for each page to go to
button1 = ttk.Button(menu_frame, image=data_photo1, command=go_to_datapage)
button1.grid(column=0, row=0)

button2 = ttk.Button(menu_frame, image=home_photo2, command=go_to_homepage)
button2.grid(column=1, row=0)

button3 = ttk.Button(
    menu_frame, image=information_photo3, command=go_to_informationpage
)
button3.grid(column=2, row=0)

root.mainloop()
