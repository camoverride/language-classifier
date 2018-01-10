"""
When run as a script, this module iterates through a list of languages, downloading a specified
number of words from each language. Determine the languages and number of words to download by
altering the LANGUAGES and WORDS variables. Tokenization is done by whitespace, so languages like
Chinese and Japanese will not yield accurate results: use languages that have spaces between words.
Language prefixes from here: https://en.wikipedia.org/wiki/List_of_Wikipedias
Trivia: https://www.quora.com/Why-are-there-so-many-articles-in-the-Cebuano-language-on-Wikipedia
"""
import subprocess
from os import listdir
from os.path import join
from get_data import GetArticles
import sys
sys.path.append('..')
from languages import LANGUAGES


WORDS = 40000
DATABASE_LOCATION = 'data'


class DataBaseWriter(object):
    """
    This is an object with the public method dbwrite. This object takes as its argument
    db_root_location, which specifies a directory where the language data should be downloaded.
    """
    def __init__(self, db_root_location):
        self.getdata = GetArticles()
        self.db_root_location = db_root_location


    def dbwrite(self, language, words, exact_words=False):
        """
        Given a language, this function downloads 25 Wikipedia articles. It then reads those
        articles and adds words to an "all_articles.dat" file until the number of words is
        reached. It also leaves behind the articles downloaded as .txt files.
        """
        # debug output
        print('checking ' + language + ' articles')

        language_data_folder = join(self.db_root_location, language)
        language_data_db = join(self.db_root_location, language, 'all_articles.dat')

        # Checks if the folder for the specific language exists. Creates it if it doesn't.
        if language not in listdir(self.db_root_location):
            subprocess.run(["mkdir", language_data_folder])

        # Checks if the database file exists. Creates it if it doesn't.
        if 'all_articles.dat' not in language_data_folder:
            subprocess.run(["touch", language_data_db])

        # Counts lines in all_articles.db, the database file.
        words_in_db = 0
        with open(language_data_db) as articles:
            for line in articles:
                for word in line.split():
                    words_in_db += 1
        articles.close()

        # debug
        print('   > Target words:', words)
        print('   > Current words:', words_in_db)

        # Checks whether enough words are in the database.
        if words_in_db < words:
            words_in_db = 0

            # While there are not enough words, download more.
            while words_in_db < words:

                # Set to zero, because all words are counted every time.
                words_in_db = 0
                self.getdata.write_articles(language, 25, language_data_folder)

                # Overrides database file.
                with open(language_data_db, 'w') as db:

                    # Gathers up all the Wikipedia files.
                    contents = listdir(language_data_folder)
                    articles = [article for article in contents if article[-3:] == 'txt']

                    # Iterates through the Wiki files, adding their words to the database.
                    for article in articles:
                        with open(join(language_data_folder, article)) as a:
                            for line in a:
                                for word in line.split():
                                    words_in_db += 1
                                    db.write(word)
                                    db.write(' ')

                                    # The loop is terminated if an exact word count is desired.
                                    if exact_words and words_in_db >= words:
                                        break
                                else:
                                    continue
                                break
                            else:
                                continue
                            break

                # debug
                print('   ... adding words. Total:', words_in_db)

        # splits all_data into training and test sets
        train = int(0.9 * words_in_db)
        all_words = []
        with open(language_data_db) as database:
            for line in database:
                for word in line.split():
                    all_words.append(word)

        with open(join(language_data_folder, 'TRAINING_SET.db'), 'w') as training_set:
            for word in all_words[:train]:
                training_set.write(word)
                training_set.write(' ')

        with open(join(language_data_folder, 'TEST_SET.db'), 'w') as test_set:
            for word in all_words[train:]:
                test_set.write(word)
                test_set.write(' ')


if __name__ == "__main__":

    db = DataBaseWriter(DATABASE_LOCATION)

    for lang in LANGUAGES:
        db.dbwrite(lang, WORDS)
