"""
This module takes Wikipedia texts and writes them to a SQL database. The database is organized
by language and by whether an article is in the training or the test set. Inspect the database like:

$ sqlite3 language_data.db
> SELECT language, title FROM wiki_data WHERE language = "en";
"""
import glob
import numpy as np

from sqlalchemy import Table, Column, Text, String, MetaData, create_engine


class Database(object):
    """
    This creates a SQLite database with the columns title, language, and text, which
    are all the values we'll need to train some ML algorithms!
    """

    def __init__(self, database_name):
        # This can easily be exchanged for a different database, like postgres.
        self.engine = create_engine(f"sqlite:///{database_name}.db")
        self.metadata = MetaData()

        # Table that contains the training data.
        self.wiki_data = Table("wiki_data", self.metadata,
                           Column("title", String, primary_key=True),
                           Column("language", String),
                           Column("text", Text)
                          )

        self.metadata.create_all(self.engine)


    def write_data(self, language, text, title):
        """
        This method writes the data to the database.
        """
        conn = self.engine.connect()

        ins = self.wiki_data.insert().values(
            language=language,
            title=title,
            text=text,
        )

        # Insert date into the database!
        conn.execute(ins)


if __name__ == "__main__":

    DATABASE_NAME = "language_data"
    DATA_LOCATION = "data"
    TRAIN_FRAC = 0.9

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
