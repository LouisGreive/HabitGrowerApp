import pytest
import sqlite3
from habit import Habit
import database
from datetime import datetime , timedelta

@pytest.fixture
def db():
    # use an in-memory database for testing
    db = sqlite3.connect(':memory:')
    database.create_table(db) # create tables before testing
    yield db
    db.close()


# Test fixture to create habit instances for testing
@pytest.fixture
def daily_habit(db):
    """ Fixture to create a Habit instance for testing """
    habit=Habit(name = "Test daily habit",description="A daily habit", periodicity = "daily")
    habit.completion_dates = []
    return habit

@pytest.fixture
def weekly_habit(db):
    return Habit(name="Test weekly habit", description="A weekly habit", periodicity = "weekly")

def test_initialization(daily_habit):
    """ Test if the habit is initialized correctly"""
    assert daily_habit.name == "Test daily habit" # check the name
    assert daily_habit.description == "A daily habit" # check the description
    assert daily_habit.periodicity == "daily" # check the periodicity
    assert daily_habit.times_completed == 0 # times_completed should be 0
    assert daily_habit.completion_dates == [] # list should be empty

def test_check_off(daily_habit):
    """Test the check off method"""
    initial_completions = daily_habit.times_completed
    daily_habit.check_off() # Simulates checking off a daily habit
    assert daily_habit.times_completed == initial_completions + 1

    last_completion_date = datetime.fromisoformat(daily_habit.completion_dates[-1]).date()
    assert last_completion_date == datetime.now().date()


def test_check_streak_daily(daily_habit):
    """ Test check_streak method for a daily habit."""
    today = datetime.now().date()

    # Simulation of completing the habit over 3 consecutive days
    daily_habit.completion_dates = [(today - timedelta(days=i)).isoformat() for i in range (3)]
    assert daily_habit.check_streak() == 3

    # Break the streak with a missed day
    daily_habit.completion_dates = [
        (today - timedelta(days=1)).isoformat(),
        (today - timedelta(days=2)).isoformat(),
        (today - timedelta(days=4)).isoformat(),
    ]
    assert daily_habit.check_streak() == 2


def test_check_streak_weekly(weekly_habit):
    """Test check_streak method for weekly habit."""
    today = datetime.now().date()

    #simulation of completing the habit over 3 consecutive weeks
    weekly_habit.completion_dates = [(today - timedelta(weeks=i)).isoformat() for i in range(3)]
    assert weekly_habit.check_streak() == 3

    # Break the streak with a missed week
    weekly_habit.completion_dates = [
        (today - timedelta(weeks=1)).isoformat(),
        (today - timedelta(weeks=3)).isoformat(),
    ]
    assert weekly_habit.check_streak() == 1


def test_habit_info(daily_habit):
    """Test the habit_info method for a habit"""
    info = daily_habit.habit_info()

    # Expected dictionary structure
    expected_info = {
        "name": "Test daily habit",
        "description": "A daily habit",
        "periodicity": "daily",
        "creation_date": daily_habit.creation_date.isoformat(),
        "times_completed": 0,
        "completion_dates": [],
    }

    # checks if the info returned by the habit_info method matches the expected dictionary
    assert info == expected_info
