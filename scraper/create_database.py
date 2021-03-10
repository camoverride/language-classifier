"""
This module takes Wikipedia texts and writes them to a SQL database. The database is organized
by language and by whether an article is in the training or the test set. Inspect the database like:

$ sqlite3 language_data.db
> SELECT language, title FROM wiki_data WHERE language = "en";

This does NOT append to an existing database: it creates a new one from scratch.
"""
import glob
import numpy as np
import sqlite3


class Database(object):
    """
    This creates a SQLite database with the columns title, language, and text_data, which
    are all the values we'll need to train some ML algorithms!
    """

    def __init__(self, database_name):
        self.database_name = database_name

        # Connect to the database.
        self.conn = sqlite3.connect(f"{self.database_name}.db")
        self.c = self.conn.cursor()

        # Create a table.
        self.c.execute("""CREATE TABLE wiki_data
                     (title text primary key, language text, text_data text)""")

        # Commit the changes and clean up.
        self.conn.commit()
        self.conn.close()


    def write_data(self, language, text_data, title):
        """
        This method writes the data to the database.
        """
        # Connect to the database.
        self.conn = sqlite3.connect(f"{self.database_name}.db")
        self.c = self.conn.cursor()

        self.c.execute(f"""INSERT INTO wiki_data VALUES ('{title}', '{language}', '{text_data}')""")

        # Commit the changes and clean up.
        self.conn.commit()
        self.conn.close()


if __name__ == "__main__":

    DATABASE_NAME = "language_data"
    DATA_LOCATION = "data"

    # Get all the file paths from the data directory
    file_paths = glob.glob(f"./{DATA_LOCATION}/**/*.txt", recursive=True)

    # Initialize the database
    db = Database(DATABASE_NAME)

    for f in file_paths:
        # Get the language id from the path.
        language = f.split("/")[-2]

        # Get the text of the document.
        with open(f) as t:
            text = t.read()

        # Get the title from the path.
        title = f.split(".")[-2].split("/")[-1]

        # Write to the database.
        db.write_data(language, text, title)
