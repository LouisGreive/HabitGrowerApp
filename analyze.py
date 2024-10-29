from database import get_db, get_habit_data, get_completion_data
from datetime import datetime, timedelta
from habit import Habit


def list_tracked_habits(db):
    """
    Function that return a list of all tracked habits from the database
    :param: db Sqlite database connection object
    :returns: list of habits.
    """
    cur = db.cursor()
    # Query to get all habit names from the Habits table
    cur.execute("SELECT habit_name FROM habits")
    habits = cur.fetchall()
    return [habit[0] for habit in habits]

def list_habit_by_periodicity(db,periodicity):
    """
    Function that returns habits filtered by their periodicity (daily or weekly)

    :param periodicity:"daily" or "weekly"
    :param db: Sqlite database connection object
    :return: List of habit names that match the periodicity
    """

    cur = db.cursor()
    # Query to fetch habits based on periodicity
    cur.execute("SELECT habit_name FROM Habits WHERE periodicity = ?", (periodicity,))
    habits = cur.fetchall()
    # Convert list of tuples to a flat list
    return [habit[0] for habit in habits]

def longest_historical_streak_for_habit(db,habit_name):
    """
    Function that calculates the longest historical streak for a habit.
    :param db: Sqlite database connection object
    :param habit_name : Name of the habit to be calculated the longest streak
    :returns: the longest historical streak of consecutive completions for the habit.
    """
    # Fetch habit details from database
    habit_data = get_habit_data(db,habit_name)
    if not habit_data:
        return 0 # Habit not found

    periodicity = habit_data [2]

    # Retrieve completions dates
    completions = get_completion_data(db,habit_name)
    if not completions:
        return 0 # No completions, no longest streak

    # Sort completion dates and convert to datetime objects
    completion_dates = sorted(datetime.fromisoformat(date[0]) for date in completions)

    # Define the time interval to check consecutive completions
    # if daily we check 1 day, if weekly we will check 1 week
    delta = timedelta(days=1) if periodicity == 'daily' else timedelta(weeks=1)

    # Initialize the variables to track the longest and the current streaks
    longest_streak = current_streak = 1
    # Loop trough completions dates to check if it keeps the interval defined by the periodicity
    for i in range(1,len(completion_dates)):
        if completion_dates[i] - completion_dates[i-1] <= delta:
            current_streak += 1
        else:
            current_streak = 1

        #update longest_streak if the current streak exceed the longest previous streak
        longest_streak = max(longest_streak, current_streak)

    return longest_streak

def longest_historical_streak(db):
    """
    Function that calculates the longest historical streak across all tracked habits
    :param db: Sqlite database connection object
    :returns: the longest historical streak among all habits and the name of that habit
    """
    # Get all tracked habits names
    cur = db.cursor()
    cur.execute("SELECT habit_name FROM habits")
    habits = cur.fetchall()

    if not habits:
        return 0 , None # No habits found

    # initialize the variable to track the longest streak across all habits
    longest_streak = 0
    longest_streak_habit = None

    # calculate the longest streak for each habit and update the max found.
    for habit in habits:
        habit_name = habit[0]
        habit_streak = longest_historical_streak_for_habit(db,habit_name)

        # Update the longest streak if the current habit's streak is higher
        if habit_streak > longest_streak:
            longest_streak = habit_streak
            longest_streak_habit = habit_name

    return longest_streak, longest_streak_habit
