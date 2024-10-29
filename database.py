import sqlite3
from datetime import datetime


def get_db(name="db/main.db"):
    """
    open the connection to the SQLite database and ensure the creation of the tables
    :returns: sqlite3.connection: connection object to interact with the SQLite database.
    """
    db = sqlite3.connect(name)
    create_table(db) # ensure tables are creates
    return db

def create_table(db):
    """
    Creates the habits and completions tables in the database if they don't exist.
    :arg: db : connection object to interact with the SQLite database.
    :returns: None

    """
    cur = db.cursor()

    # Create habits table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS habits(
            habit_name TEXT PRIMARY KEY,
            habit_description TEXT NOT NULL,
            periodicity TEXT NOT NULL,
            creation_date TEXT NOT NULL,
            times_completed INTEGER DEFAULT 0
       )
 """)

    # Create completions table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS completions(
        habit_name TEXT,
        completion_date TEXT NOT NULL,
        FOREIGN KEY (habit_name) REFERENCES habits(habit_name)
        )
    """)

    db.commit()


def add_habit(db,habit_name,habit_description,periodicity,creation_date):
    """
    Adds a new habit to the habits table.
    :param db: connection object to interact with the SQLite database.
    :param habit_name(str): the name of the habit
    :param habit_description(str): the description of the habit
    :param periodicity(str): the periodicity of the habit ('daily' or 'weekly').
    :param creation_date(datetime): the creation date of the habit
    :returns:None
    """

    times_completed = 0 # default value for each new habit

    cur = db.cursor()
    cur.execute("""
        INSERT INTO habits(habit_name, habit_description, periodicity, creation_date, times_completed)
        VALUES (?,?,?,?,?)
    """, (habit_name,habit_description,periodicity,creation_date.isoformat(),0))

    db.commit()

def add_completion_date(db,habit_name,completion_date=None):
    """
    Adds a new Completion date for Habit to the Completions table.
    :param db: connection object to interact with the SQLite database.
    :param habit_name(str): the name of the habit for the completion
    :param completion_date(datetime): the date when the habit was completed.
    :returns:None
    """
    if completion_date is None:
        completion_date = datetime.now().isoformat()

    cur = db.cursor()
    cur.execute("""
        INSERT INTO completions(habit_name, completion_date)
        VALUES (?,?)
    """, (habit_name,completion_date))

    # Update times completed for the habit
    cur.execute("""
        UPDATE habits 
        SET times_completed = times_completed + 1
        WHERE habit_name = ?
    """,(habit_name,))

    db.commit()

def get_habit_data(db,habit_name):
    """
    Retrieves data for a specific habit in the habits table
    :param db: Connection object to interact with the SQLite database.
    :param habit_name: name of the habit to retrieve
    :returns:(Tuple) the habit's information
    """
    cur = db.cursor()
    cur.execute("SELECT * FROM habits WHERE habit_name = ?", (habit_name,))
    return cur.fetchone()

def get_completion_data(db, habit_name):
    """
    Retrieves data for a specific habit in the Completions table
    :param db: connection object to interact with the SQLite database.
    :param habit_name(str):name of the habit to retrieve
    :param:(list) List of completion dates (str) for the habit.
    """
    cur = db.cursor()
    cur.execute("SELECT completion_date FROM completions WHERE habit_name = ?", (habit_name,))
    return cur.fetchall()

def delete_habit(db,habit_name):
    """
    Deletes a habit and its associated completion record from the database
    :param db: connection object to interact with the SQLite database.
    :param habit_name(str): name of the habit to delete
    :returns: None
    """
    cur = db.cursor()

    # delete the habit from the Habits table
    cur.execute("DELETE FROM habits WHERE habit_name = ?", (habit_name,))

    # delete the associated completion record from the completion table
    cur.execute("DELETE FROM completions WHERE habit_name = ?", (habit_name,))

    db.commit()