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


    def _count_words_in_language(self, language):
        """
        Counts the number of words in all the .txt files for a single language.
        """
        words = 0
        language_data_folder = join(self.db_root_location, language)
        contents = listdir(language_data_folder)
        articles = [article for article in contents if article[-3:] == 'txt']
        for article in articles:
            with open(join(language_data_folder, article), 'r') as text:
                for line in text:
                    for _ in line.split(' '):
                        words += 1

        return words


    def _get_words_in_language(self, language):
        """
        Iterates through all the articles downloaded for a single language, collecting all the words
        by splitting on whitespace and returns the list of words.
        """
        words = []
        language_data_folder = join(self.db_root_location, language)
        contents = listdir(language_data_folder)
        articles = [article for article in contents if article[-3:] == 'txt']
        for article in articles:
            with open(join(language_data_folder, article), 'r') as text:
                for line in text:
                    for word in line.split(' '):
                        words.append(word)

        return words

        
    def dbwrite(self, language, words, exact_words=False):
        """
        Given a language, this function downloads 25 Wikipedia articles. It then reads those
        articles and adds words to an "all_articles.dat" file until the number of words is
        reached. It also leaves behind the articles downloaded as .txt files.
        """
        # Debug output.
        print('checking ' + language + ' articles')

        language_data_folder = join(self.db_root_location, language)
        train_ratio = 0.9

        # Checks if the folder for the specific language exists. Creates it if it doesn't.
        if language not in listdir(self.db_root_location):
            subprocess.run(["mkdir", language_data_folder])

        # If there are not enough words downloaded, download more.
        while self._count_words_in_language(language) < words:
            self.getdata.write_articles(language, 25, language_data_folder)

        # Read all the words into a list, removing any extras. Divide into training and test sets.
        all_words = self._get_words_in_language(language)[:words]
        split = int(train_ratio * words)
        training_set = all_words[split:]
        test_set = all_words[:split]

        # Write these sets to the SQL database.
        


if __name__ == "__main__":

    db = DataBaseWriter(DATABASE_LOCATION)

    for lang in LANGUAGES:
        db.dbwrite(lang, WORDS)
