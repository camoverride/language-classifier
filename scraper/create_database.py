"""
This module takes Wikipedia texts and writes them to a SQL database. The database is organized
by language and by whether an article is in the training or the test set. Inspect the database like:


"""
import glob
import numpy as np

from sqlalchemy import Table, Column, Text, String, MetaData, create_engine


class Database(object):
    """
    This creates a SQLite database with two tables, "train" and "test." Each table
    has data from each language. This object has the public method write_data,
    which takes as its arguments a language, a training text, and a test text. It
    writes this information to the proper table.
    """

    def __init__(self, database_name):
        # This can easily be exchanged for a different database, like postgres.
        self.engine = create_engine(f"sqlite:///{database_name}.db")
        self.metadata = MetaData()

        # Table that contains the training data.
        self.wiki_data = Table("wiki_data", self.metadata,
                           Column("language", String, primary_key=True),
                           Column("title", String),
                           Column("category", String), # train or test sets
                           Column("text", Text)
                          )

        self.metadata.create_all(self.engine)


    def write_data(self, language, text, title, category):
        """
        This method writes the data to the database.
        """
        conn = self.engine.connect()

        # TODO: clean this up
        del1 = self.wiki_data.delete().where(self.wiki_data.columns.language == language)

        conn.execute(del1)

        ins = self.train.insert().values(
            language=language,
            title=title,
            category=category,
            text=text,
        )

        # Insert date into the database!
        conn.execute(ins)


if __name__ == "__main__":
    DATABASE_NAME = "language_data.db"
    DATA_LOCATION = "data"
    TRAIN_FRAC = 0.9

    db = Database(DATABASE_NAME)

    file_paths = glob.glob(".data/**/*.txt", recursive=True)

    for f in file_paths:
        # Get the language id from the path.
        language = f.split("/")[-2]

        # Get the text of the document.
        with open(f) as t:
            text = t.read()

        # Get the title from the path.
        title = f.split(".")[-2]

        # Randomly assign to the training or test set.
        np.random.binomial(1, TRAIN_FRAC)

        db.write_data(language, text, title, category)



# class DataBaseWriter(object):
#     """
#     This is an object with the public method dbwrite. This object takes as its argument
#     data_location, which specifies a directory where the language data should be downloaded.
#     """
#     def __init__(self, data_location, sql_database_name):
#         self.data_location = data_location
#         self.sql_database = Database(sql_database_name)


#     def dbwrite(self, language, train_frac):
#         """
#         This function writes to the SQLite database.
#         """
#         language_data_path = f"{self.data_location}/{language}"

#         # Join the words by white-space and add to the SQL database.
#         self.sql_database.write_data(language, title, category, text)



# if __name__ == "__main__":
#     DB_VERSION = "1"
#     DB_PATH = f"language_data_{DB_VERSION}.db"
#     DATA_PATH = "data"
#     TRAIN_FRAC = 0.9

#     writer = DataBaseWriter(data_location=DATA_PATH, sql_database_name=DB_PATH)

#     for lang in LANGUAGES:
#         writer.dbwrite(lang, TRAIN_FRAC)
