import sqlite3

def verify_preload_data(db_path="db/preload_test_data.db"):
    # connection to the test database
    db = sqlite3.connect(db_path)
    cur = db.cursor()

    # Query and print all data from the habit table
    print("Contents of habits table:")
    cur.execute("SELECT * FROM habits")
    habits = cur.fetchall()
    for habit in habits :
        print(habit)

    # Query and print all data from completions table
    print("\nContents of completions table:")
    cur.execute("SELECT * FROM completions")
    completions = cur.fetchall()
    for completion in completions:
        print(completion)

    # Close the database connection
    db.close()

if __name__ == "__main__":
    verify_preload_data()