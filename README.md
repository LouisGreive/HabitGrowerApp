# Habit Grower App
Habit Grower App is a Python based habit tracking application that allows user to create,
manage and analyze personal habits. 
The application is displayed with an intuitive Tkinter-based GUI where user can track habits,
get insights of his progress and analyze the evolution of their habits.

The app uses SQLite3 for local data storage and retrieval. 

### REQUIREMENTS
- Python 3.x 
- SQLite 3 (included in the python standard library)
- TKINTER (included in the python standard library)
- pytest 7.2.0

### INSTALLATION
1. Install required packages:
    ```bash
    pip install -r requirements.txt
    ```
2. ensure Python's standard library includes "SQLite3" and "Tkinter"

### RUNNING THE APPLICATION 

Start the application by running "main.py":
```bash

python main.py
```
### RUNNING THE APPLICATION WITH PRELOADED TEST DATA
For testing purposes, you can also use the main_preload_data.py file to run the app with a set
of preloaded sample habits. to do this, execute:
```bash
python main_preload_data.py
```
## HOW TO USE THE HABIT GROWER APP 
1. **Create a Habit**: Click create habit to add a new habit that you want to track. Enter the habit's 
name, description,periodicity (daily or weekly)
2. **Edit a Habit**: Click edit habit to modify the description or periodicity of an existing habit.
Note: For avoid problems with the database, edit the name of the habit is not possible, you can delete
the habit and recreate it.
3. **Delete Habit**: select delete habit and enter the name of the habit you want to remove.
4. **Show Habit Info**:click show habit info to see details about a specific habit.
5. **Marking Habit Completed**: Use mark habit completed to log each time you complete a habit.
Note: Habit will be mark as completed for the current day.

6. **Analytical Functions**:
- **Show All Tracked Habits**: View a list of all habits being tracked.
- **Show Habits By Periodicity**: List habits by daily or weekly periodicity
- **Longest Streak Across All Habits**: display the habit with the historical longest completion streak
- **Longest Streak For Each Habit**: View the historical longest streak for each individual habit.

## CREDITS 
this project was developed by Louis Greive for the **Object-Oriented and Functional
programming with Python** course at IU University. Special thanks to **Prof. Dr. Max Pumperla**
whose tutorials were instrumental in the project's development.

