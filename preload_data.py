import sqlite3
from datetime import datetime, timedelta
from database import add_habit, add_completion_date, create_table


def preload_data(db_path="db/preload_test_data.db"):

    """
    Create a database with sample data for testing purposes.
    """
    #connect to the test data database
    db = sqlite3.connect(db_path)
    create_table(db) # Create the tables

    # Clear existing data to avoid duplicates
    cur = db.cursor()
    cur.execute("DELETE FROM habits")
    cur.execute("DELETE FROM completions")
    db.commit()

    # set creation date to four weeks ago
    creation_date = (datetime.now() - timedelta(weeks=4)).isoformat()

    # define  sample habit
    habits = [
        ("Exercise", "Daily workout 30 minutes", "daily", creation_date),
        ("Read", "Read for 20 minutes", "weekly", creation_date),
        ("Meditate", "Daily meditation practice", "daily", creation_date),
        ("Guitar Practice", "Weekly guitar practice", "weekly", creation_date),
        ("Code", "Daily coding practice", "daily", creation_date)
    ]

    # add each habit to the database
    for name,description,periodicity,date in habits:
        add_habit(db,name,description,periodicity,date)

    # Define completions
    today = datetime.now()
    completion_patterns = {
        # exercise daily for the last 20 days
        "Exercise":[(today - timedelta(days=i)).isoformat() for i in range(20)],
        # read weekly for the past 4 weeks
        "Read":[(today - timedelta(weeks=i)).isoformat() for i in range(4)],
        # Meditate only 4 days for the last 4 weeks
        "Meditate":[
            (today-timedelta(days=1)).isoformat(),
            (today-timedelta(days=3)).isoformat(),
            (today-timedelta(days=7)).isoformat(),
            (today-timedelta(days=10)).isoformat(),
        ],
        # Guitar practice only 2 weeks of the last 4 weeks
        "Guitar Practice": [
            (today-timedelta(weeks=1)).isoformat(),
            (today-timedelta(weeks=3)).isoformat()
        ],
        # Code 10 days on a row until today, break daily streak before that
        # 5 days without code and create another 5 days streak before that
        "Code": [
            (today - timedelta(days=i)).isoformat() for i in range(10)
        ] + [
            (today - timedelta(days=i)).isoformat() for i in range(15,20)
        ]

    }

    # add completions dates for each habit based on the defined patterns
    for habit_name, dates in completion_patterns.items():
        for date in dates:
            add_completion_date(db,habit_name,date)

    # Commit and close connection after create the data
    db.commit()
    db.close()

if __name__ == "__main__":
    preload_data()

