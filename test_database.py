import sqlite3
import pytest
import database
from datetime import datetime, timedelta

# File path for the test database
DB_PATH = "test.db"

@ pytest.fixture
def db():
    """
    Fixture to create a file-based SQLite database(test.db) for testing.
    Each test will create or overwrite the test.db file.
    """
    # Create a new connection to test.db
    db = sqlite3.connect(DB_PATH)

    # drop the tables before recreating them to ensure a clean start
    cur = db.cursor()
    cur.execute("DROP TABLE IF EXISTS Habits")
    cur.execute("DROP TABLE IF EXISTS Completions")
    database.create_table(db) # create the tables

    yield db

    # close the database after the test
    db.close()

def test_create_table(db):
    """
    Test that the tables are created successfully
    """
    cur = db.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cur.fetchall()

    assert ("habits" , ) in tables
    assert ("completions" , ) in tables

def test_add_habit(db):
    """
    Test that a habit can be added to the database and retrieved correctly.
    This test simultaneously will check the get_habit_data function.
    """
    habit_name = "Exercise"
    habit_description = "Daily workout"
    periodicity = "daily"
    creation_date = datetime.now()

    # add a habit
    database.add_habit(db, habit_name, habit_description, periodicity, creation_date)

    # retrieve the habit
    habit_data = database.get_habit_data(db, habit_name)

    # verify the habit data is correct
    assert habit_data is not None
    assert habit_data[0] == habit_name # check the name
    assert habit_data[1] == habit_description # check description
    assert habit_data[2] == periodicity # check periodicity
    assert habit_data[3] == creation_date.isoformat() # check the creation date
    assert habit_data[4] == 0 # times completed should be 0 initially



def test_add_completion_date(db):
    """
    Test that completion dates are added and linked to the correct habit
    """
    habit_name = "Exercise"
    database.add_habit(db, habit_name, "Daily workout", "daily", datetime.now())

    #Add a completion date
    completion_date = datetime.now().isoformat()
    database.add_completion_date(db, habit_name, completion_date)

    # Retrieve the completion data
    completions = database.get_completion_data(db, habit_name)

    assert len(completions) == 1 # should be the just added completion
    assert completions[0][0] == completion_date # check if matches

def test_get_completion_data(db):
    """
    Test that the completion data can be retrieved correctly after being added
    """
    habit_name = "Exercise"
    database.add_habit(db, habit_name, "Daily workout", "daily", datetime.now())

    # add multiple completion dates
    completion_dates = [
        (datetime.now()- timedelta(days=i)).isoformat() for i in range (3)
    ]

    for date in completion_dates:
        database.add_completion_date(db, habit_name, date)

    # retrieve the completion data
    completions = database.get_completion_data(db, habit_name)

    assert len(completions) == 3
    for i, completion in enumerate(completions):
        assert completion[0] == completion_dates[i]

def test_delete_habit(db):
    """
    Test that a habit can be deleted with its associated completions
    """
    habit_name = "Exercise"
    database.add_habit(db, habit_name, "Daily workout", "daily", datetime.now())

    # add some completions dates
    for _ in range(3):
        database.add_completion_date(db, habit_name, datetime.now().isoformat())

    # check if the habit exists and has completions
    habit_data = database.get_habit_data(db, habit_name)
    assert habit_data is not None # Habit exist
    completions = database.get_completion_data(db, habit_name)
    assert len(completions) == 3 # should be 3 completion

    # Delete habit
    database.delete_habit(db, habit_name)

    # check if habit and completions are deleted
    habit_data = database.get_habit_data(db, habit_name)
    completions= database.get_completion_data(db, habit_name)
    assert habit_data is None
    assert completions == []