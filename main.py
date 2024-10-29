import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

from select import select

from habit import Habit
from analyze import (
    list_tracked_habits,
    list_habit_by_periodicity,
    longest_historical_streak_for_habit,
    longest_historical_streak
)
from database import get_db, delete_habit, add_habit, add_completion_date, get_habit_data, get_completion_data
from datetime import datetime

# initialize the main application window
root = tk.Tk()
root.title("Habit Grower")
root.geometry("600x700")
# Custom colors and styles
bg_color = "#282c34" # gives a dark background color
title_color = "#61dafb" # Light blue color for tittle
button_color = "#007acc" # Button color
button_hover = "#005f99" # Hover color for buttons
text_color = "#ffffff" # white text color

# Set background color for the main window
root.configure(bg=bg_color)
# Function to connect to the main database
def get_database():
    """Function to get a connection to the main database."""
    return get_db("db/main.db") ## Run main_preload_data.py for use the preload_data
                                ## Or also change to "db/preload_test_data.db" to run the app with preload data

# Functionalities of the app
def create_habit_app():
    """Ask te user for habit details and adds it to the database"""
    name = simpledialog.askstring("Name", "Enter habit name")
    description = simpledialog.askstring("Description", "Enter habit description")
    periodicity = simpledialog.askstring("Periodicity", "Enter periodicity: 'daily' or 'weekly'")

    # check if periodicity is correct
    if periodicity not in ["daily", "weekly"]:
        messagebox.showerror("Error", "Invalid periodicity. Choose 'daily' or 'weekly'")
        return

    # Add habit to the database
    if name and description and periodicity:
        try:
            with get_database() as db:# connects to the database, ensuring it close automatically
                creation_date = datetime.now()
                add_habit(db, name, description, periodicity,creation_date)
                messagebox.showinfo("Success", f"Habit '{name}' added successfully")
        except Exception as e:
            messagebox.showerror("Error", f"failed to create habit: {e}")

def edit_habit_app():
    """Allows the user to update and existing habit's description or periodicity"""
    name = simpledialog.askstring("Name", "Enter the name of the habit to edit: ")
    if not name:
        messagebox.showerror("Error", "Please provide a habit name")
        return

    #Retrieve current habit details
    try:
        with get_database() as db:
            habit_data = get_habit_data(db,name)
            if not habit_data:
                messagebox.showerror("Error", f"No habit found with the name '{name}'.")
                return

            # Ask user for the new details
            new_description = simpledialog.askstring("Description", "Enter new habit description: ")
            new_periodicity = simpledialog.askstring("Periodicity","Enter new periodicity: 'daily' or 'weekly'")

            if new_periodicity not in ["daily", "weekly"]:
                messagebox.showerror("Error", "Invalid periodicity. Choose 'daily', 'weekly'")
                return

            #Update the habit in the database
            if new_description and new_periodicity:
                cur = db.cursor()
                cur.execute(
                    "UPDATE habits SET habit_description = ?, periodicity = ? WHERE habit_name = ?",
                    (new_description,new_periodicity,name)

                )
                db.commit()
                messagebox.showinfo("Success", f"Habit '{name}' updated successfully")

                # If the user need to change the name it ask to better delete the habit
                renaming = (
                    f"To change the name of '{name}', please delete and recreate the habit."
                    "Type 'ok' to acknowledge."
                )
                if simpledialog.askstring("Change Name", renaming) != 'ok':
                    messagebox.showinfo("Reminder","Habits names cannot be edited directly.")

    except Exception as e:
        messagebox.showerror("Error", f"failed to update habit: {e}")

def delete_habit_app():
    """Ask the user for a habit name and deletes it from the database.
    Show error if the habit don't exist"""
    name = simpledialog.askstring("Name", "Enter the name of the habit to delete: ")
    if name:
        try:
            with get_database() as db:
                delete_habit(db, name)
                messagebox.showinfo("Success", f"Habit '{name}' deleted successfully")
        except Exception as e:
            messagebox.showerror("Error", f"failed to delete habit: {e}")

def show_habit_info():
    """List all tracked habits, ask the user to select one, and display habit info.
    show error if the habit is not found"""
    try:
        with get_database() as db:
            # Get list of all tracked habits
            tracked_habits = list_tracked_habits(db)
            if not tracked_habits:
                messagebox.showinfo("Error", "No habits are being tracked.")
                return

            # Ask user to select the habit that what to know the info
            selected_habit = simpledialog.askstring("Habits",f"Tracked Habits:\n" + "\n".join(tracked_habits))
            if selected_habit:
                # Get habit data from database
                habit_data = get_habit_data(db,selected_habit)
                if habit_data:
                    # Format the creation date to only show the date part
                    creation_date = datetime.fromisoformat(habit_data[3]).strftime("%Y-%m-%d")
                    # Retrieve completion dates
                    completion_dates = [
                        datetime.fromisoformat(date[0]).strftime("%Y-%m-%d %H:%M") for date in
                        get_completion_data(db, selected_habit)
                    ]

                    # show the user data in clean format
                show_info = (
                    f"Name: {habit_data[0]}\n"
                    f"Description: {habit_data[1]}\n"
                    f"Periodicity: {habit_data[2]}\n"
                    f"Creation date: {creation_date}\n"
                    f"Times Completed: {habit_data[4]}\n"
                    f"Completion Dates: {', '.join(completion_dates) if completion_dates else 'none'}"

                )
                messagebox.showinfo("Habit Info", show_info)

    except Exception as e:
        messagebox.showerror("Error", f"failed to show info of the habit: {e}")

def mark_habit_completed():
    """Marks a habit as completed for the current day"""
    name = simpledialog.askstring("Complete Habit",
                                  "Enter the name of the habit to mark as completed for today")
    if name:
        try:
            with get_database() as db:
                add_completion_date(db,name,datetime.now().isoformat())
                messagebox.showinfo("Success", f"Habit '{name}' marked as completed for today")
        except Exception as e:
            messagebox.showerror("Error", f"failed to mark habit as completed for today: {e}")

# ANALYTICAL FUNCTIONS OF THE APP:
def show_tracked_habits():
    """Show the user all tracked habits"""
    try:
        with get_database() as db:
            habit = list_tracked_habits(db)
            messagebox.showinfo("Tracked Habits", "\n".join(habit) if habit else "No habits are being tracked")

    except Exception as e:
        messagebox.showerror("Error", f"failed to show tracked habits: {e}")

def show_habit_by_periodicity():
    """Show the user habits filtered by daily or weekly periodicity"""
    periodicity = simpledialog.askstring("Periodicity","Enter periodicity: 'daily' or 'weekly'")
    if periodicity not in ["daily", "weekly"]:
        messagebox.showerror("Error", "Invalid periodicity. Choose 'daily', 'weekly'")
        return

    try:
        with get_database() as db:
            habits = list_habit_by_periodicity(db,periodicity)
            messagebox.showinfo(f"{periodicity.capitalize()} Habits",
                                "\n".join(habits) if habits else f"No {periodicity} habits being tracked")
    except Exception as e:
        messagebox.showerror("Error", f"failed to show habits by periodicity: {e}")

def show_longest_streak():
    """Show the user the longest streak among all habits"""
    try:
        with get_database() as db:
            longest_streak, habit_name = longest_historical_streak(db)
            if habit_name:
                messagebox.showinfo("Longest Streak",
                                    f"The longest streak is {longest_streak} days/weeks for the habit '{habit_name}'.")


    except Exception as e:
        messagebox.showerror("Error", f"failed to show longest streak: {e}")

def show_longest_streak_by_habit():
    """Show the user the longest streak for each habit"""
    try:
        with get_database() as db:
            tracked_habits = list_tracked_habits(db)
            streak_info = [f"{habit}: {longest_historical_streak_for_habit(db,habit)} days/weeks" for habit in tracked_habits]
            messagebox.showinfo("Longest streak by habit", "\n".join(streak_info) if streak_info else "No habits are being tracked")
    except Exception as e:
        messagebox.showerror("Error", f"failed to show longest streak by habit: {e}")


# GUI Layout
# Title Frame
title_frame = tk.Frame(root, bg=title_color, pady=10)
title_frame.pack(fill="x")

title_label = tk.Label(title_frame, text="Habit Grower", font=("Arial",24,"bold"), fg=bg_color, bg=title_color)
title_label.pack()

quote_label = tk.Label(title_frame, text="“Excellence, then, is not an act, but a habit.” – Aristotle",
                       font=("Arial", 10, "italic"), fg=bg_color, bg=title_color)
quote_label.pack()

# Button frame
button_frame = tk.Frame(root, bg=bg_color, pady=20)
button_frame.pack(fill="x",padx=10)

def add_button(frame, text, command):
    button = tk.Button(frame, text=text, command=command,
                       font=("Arial",12),fg=text_color, bg=button_color,
                       activebackground=button_hover, activeforeground=text_color)
    button.pack(pady=5,padx=10, fill="x")

add_button(button_frame, "Create Habit", create_habit_app)
add_button(button_frame, "Edit Habit", edit_habit_app)
add_button(button_frame, "Delete Habit", delete_habit_app)
add_button(button_frame, "Show Habit Info", show_habit_info)
add_button(button_frame, "Mark Habit Completed", mark_habit_completed)

#Analysis Frame
analyze_frame = tk.LabelFrame(root, text="Analytical Functions",font=("Arial",14),
                              fg=text_color, bg=button_color, padx=10, pady=10)
analyze_frame.pack(fill="x",padx=10,pady=10)

add_button(analyze_frame,"Show all tracked Habits",show_tracked_habits)
add_button(analyze_frame,"Show Habits by periodicity",show_habit_by_periodicity)
add_button(analyze_frame, "Longest Streak Across All Habits",show_longest_streak)
add_button(analyze_frame,"Longest Streak For Each Habit",show_longest_streak_by_habit)

#Run the main loop for the app
root.mainloop()
