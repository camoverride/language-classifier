"""
This module takes Wikipedia texts and writes them to a SQL database. The database is organized
by language and by whether an article is in the training or the test set. Inspect the database like:

$ sqlite3 language_data.db
> .schema
> SELECT text FROM train WHERE language = "en";
"""
import os
import subprocess
import sys

from sqlalchemy import Table, Column, Text, String, MetaData, create_engine

sys.path.append("..")
from languages import LANGUAGES
from get_data import GetWikiArticles


class Database(object):
    """
    This creates a SQLite database with two tables, "train" and "test." Each table
    has data from each language. This object has the public method write_categories,
    which takes as its arguments a language, a training text, and a test text. It
    writes this information to the proper table.
    """

    def __init__(self, database_name):
        # This can easily be exchanged for a different database, like postgres.
        self.engine = create_engine(f"sqlite:///{database_name}.db")
        self.metadata = MetaData()

        # Table that contains the training data.
        self.train = Table("train", self.metadata,
                           Column("language", String, primary_key=True),
                           Column("text", Text)
                          )

        # Table that contains the test data.
        self.test = Table("test", self.metadata,
                          Column("language", String, primary_key=True),
                          Column("text", Text)
                         )

        self.metadata.create_all(self.engine)


    def write_categories(self, language, training_text, test_text):
        """
        This method writes the data to the database.
        """
        conn = self.engine.connect()

        # Drop rows, data will be overwritten anyway.
        del1 = self.train.delete().where(self.train.columns.language == language)
        del2 = self.test.delete().where(self.test.columns.language == language)

        conn.execute(del1)
        conn.execute(del2)

        ins1 = self.train.insert().values(
            language=language,
            text=training_text
        )

        ins2 = self.test.insert().values(
            language=language,
            text=test_text
        )

        # Execute inserts.
        conn.execute(ins1)
        conn.execute(ins2)







class DataBaseWriter(object):
    """
    This is an object with the public method dbwrite. This object takes as its argument
    data_location, which specifies a directory where the language data should be downloaded.
    """
    def __init__(self, data_location, sql_database_name):
        self.data_location = data_location
        self.sql_database = Database(sql_database_name)


    def _get_words_in_language(self, language):
        """
        Iterates through all the articles downloaded for a single language, collecting all the words
        by splitting on whitespace. Returns the list of words.
        """
        words = []
        language_data_folder = f"{self.data_location}/{language}"
        contents = os.listdir(language_data_folder)

        # Check that only articles are selected, not other stuff.
        articles = [article for article in contents if article[-3:] == "txt"]

        # Iterate over all the words.
        for article in articles:
            with open(f"{language_data_folder}/{article}", "r") as text:
                for line in text:
                    for word in line.split(" "):
                        words.append(word)

        return words


    def dbwrite(self, language, words, train_frac):
        """
        This function writes the specified amount of data (in words) to the SQLite database. If
        there are not enough words present, then more are downloaded.
        """
        language_data_path = f"{self.data_location}/{language}"

        # Checks if the folder for the specific language exists. Creates it if it doesn't.
        if language not in os.listdir(self.data_location):
            os.makedirs(language_data_path, exist_ok=True)

        # If there are not enough words downloaded, download more.
        while len(self._get_words_in_language(language)) < words:
            # Debug output.
            print(f"Downloading more words, not enough: {len(self._count_words_in_language(language))}")
            article_downloader = GetWikiArticles(self.data_location)
            article_downloader.write_articles(language, 25)

        # Read all the words into a list, trimming off any extras. Divide into training and test sets.
        all_words = self._get_words_in_language(language)[:words]
        split = int(train_frac * words)
        training_set = all_words[split:]
        test_set = all_words[:split]

        # Join the words by white-space and add to the SQL database.
        self.sql_database.write_categories(language, " ".join(training_set), " ".join(test_set))



if __name__ == "__main__":
    WORDS_PER_LANGUAGE = 4000
    DB_VERSION = "1"
    DB_PATH = f"language_data_{DB_VERSION}.db"
    DATA_PATH = "data"
    TRAIN_FRAC = 0.9

    writer = DataBaseWriter(data_location=DATA_PATH, sql_database_name=DB_PATH)

    for lang in LANGUAGES:
        writer.dbwrite(lang, WORDS_PER_LANGUAGE, TRAIN_FRAC)
