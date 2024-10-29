import sqlite3
from datetime import datetime , timedelta
import database


class Habit:
    """
    Initializes a Habit instance and saves it to the database if it's a new habit

    Attributes:
        name(string): The name of the habit.
        description(string):Provide additional details about the habit.
        periodicity(string): Indicates if the habit has to be completed daily or weekly.
        creation_date(date): Records when the habit was created.
        times_completed (integer): Keep tracking the total number of times the habit has been completed.
        completion_dates(list): a list to track all completion dates of the habit.
    """

    def __init__(self,name,description,periodicity):
        """ Initializes the Habit instance with a name,description and periodicity,
            Initializes times_completed to 0, and completion_dates to a empty list """
        self.name = name
        self.description = description
        self.periodicity = periodicity # Daily or weekly
        self.creation_date = datetime.now()  # Automatically sets the creation date
        self.times_completed = 0 # Track the total number of times the habit has been completed
        self.completion_dates = [] # List for track all completion dates

        # save the habit to the database and initialize completion dates
        self.save_to_db()
        self.get_completion_dates()


    """ Methods """

    def save_to_db(self):
        """
        saves the habit data into the database
        """
        try:
            with database.get_db() as db:
                database.add_habit(db, self.name, self.description, self.periodicity, self.creation_date)
        except sqlite3.IntegrityError:
            print(f"Habit {self.name} already exists in the database")


    def check_off(self):
        '''
        Marks the habit as completed for the day, increments times_completed
        and saves the completion to the database.
        '''

        # Gets the current date and time when the habit is completed
        completion_date = datetime.now().isoformat()

        # Append the completion date and time to the list
        self.completion_dates.append(completion_date)

        # increments the total counter of the times the habit has been completed
        self.times_completed += 1

        # save the completion date to the database
        db = database.get_db()
        try:
            database.add_completion_date(db, self.name, completion_date)
            db.commit() # commit the changes
        finally:
            db.close() # close the database connection


    def check_streak(self):

        """
        Calculate the current streak based on the habit periodicity
        Streak = is the number of consecutive periods (days or weeks) where the habit has been completed
        For daily habits, it counts how many consecutive days the habit has been completed
        For weekly habits, it counts how many consecutive weeks the habit has been completed

        :returns: (int)  The current streak of consecutive completions.
        """

        if not self.completion_dates:
            return 0 # no completions, no streak

        # Sort the completion dates to ensure they are in order
        self.completion_dates.sort()

        # convert completion dates to just the date part (ignore the time)
        completion_dates_only = [datetime.fromisoformat(date).date() for date in self.completion_dates]

        streak = 1 # minimun streak if there's at least one completion
        last_date = completion_dates_only [-1]

        if self.periodicity == 'daily':
            for i in range(len(completion_dates_only)-2,-1,-1):
                expected_date = last_date - timedelta(days=1)
                if completion_dates_only[i] == expected_date:
                    streak += 1
                    last_date = completion_dates_only[i]
                else:
                    break # break the loop if there is a gap in consecutive days

        elif self.periodicity == 'weekly':
            for i in range(len(completion_dates_only)-2,-1,-1):
                expected_date = last_date - timedelta(weeks=1)
                if completion_dates_only[i] <= expected_date <= completion_dates_only[i] + timedelta (days=6):
                    streak += 1
                    last_date = completion_dates_only[i]
                else:
                    break #break the loop if there is a gap in consecutive weeks

        return streak

    def get_completion_dates(self):
        """ get the completion dates for this habit from the database"""
        db = database.get_db()
        completion_data = database.get_completion_data(db,self.name)
        db.close()
        self.completion_dates = [date[0] for date in completion_data]
        return self.completion_dates


    def habit_info(self):
        """
        :Returns a dictionary containing information about the habit.
        """

        return {
            "name": self.name,
            "description": self.description,
            "periodicity": self.periodicity,
            "creation_date": self.creation_date.isoformat(),
            "times_completed": self.times_completed,
            "completion_dates": self.completion_dates
        }

