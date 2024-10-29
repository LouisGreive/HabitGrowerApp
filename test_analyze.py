import sqlite3
import pytest
from analyze import (list_tracked_habits,list_habit_by_periodicity,
                     longest_historical_streak_for_habit,longest_historical_streak)
from preload_data import preload_data

# Set up the database path
DB_PATH = "db/preload_test_data.db"

@pytest.fixture(scope="module")
def db():
    """
    Set up and provide access to the database
    """
    # Run preload_data to load the test data
    preload_data(DB_PATH)
    db = sqlite3.connect(DB_PATH)
    yield db
    db.close()

def test_list_tracked_habits(db):
    "test list_tracked_habit() function to ensure it returns all tracked habits"
    result = list_tracked_habits(db)
    expected_habits = {"Exercise","Read","Meditate","Guitar Practice","Code"}
    assert set(result) == expected_habits

def test_list_habit_by_periodicity_daily(db):
    """ test list_habit_by_periodicity to retrieve only daily habits """
    result = list_habit_by_periodicity(db,"daily")
    expected_daily_habits = {"Exercise","Meditate","Code"}
    assert set(result) == expected_daily_habits

def test_list_habit_by_periodicity_weekly(db):
    """ test list_habit_by_periodicity to retrieve only weekly habits """
    result = list_habit_by_periodicity(db,"weekly")
    expected_weekly_habits = {"Read","Guitar Practice"}
    assert set(result) == expected_weekly_habits

def test_longest_historical_streak_for_exercise(db):
    """ test longest_historical_streak_for_habit for the "Exercise" habit """
    result = longest_historical_streak_for_habit(db,"Exercise")
    assert result == 20 # Exercise has a streak of 20 completions

def test_longest_historical_streak_for_read(db):
    """ test longest_historical_streak_for_habit for the "Read" habit """
    result = longest_historical_streak_for_habit(db,"Read")
    assert result == 4 # Read has a weekly streak of 4 completions

def test_longest_historical_streak_for_meditate(db):
    """ test longest_historical_streak_for_habit for the "Meditate" habit """
    result = longest_historical_streak_for_habit(db,"Meditate")
    assert result == 1 # Meditate has a max streak of 1

def test_longest_historical_streak(db):
    """Test the longest_historical_streak to find the habit
    with the historical longest streak among all tracked habits."""
    result_streak, result_habit = longest_historical_streak(db)
    assert result_streak == 20
    assert result_habit == "Exercise"