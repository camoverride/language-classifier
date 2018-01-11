"""
This module creates an object that can be used to grab data from Wikipedia. This scraper
also performs basic document sanitizing, such as removing punctuation, HTML tags, and
citation brackets. I recommend scraping less than 100 articles per API call.
"""
import re
import json
import requests
from sqlalchemy import Table, Column, Text, String, MetaData, create_engine, exc


class GetArticles(object):
    """
    This is an object with the public method write_articles(language_id, number_of_articles,
    db_location). This writes sanitized articles to text files in a specified location.
    """
    def __init__(self):
        pass


    def _get_random_article_ids(self, language_id, number_of_articles):
        """
        Makes a request for random article ids. "rnnamespace=0" means that only articles are chosen,
        as opposed to user-talk pages or category pages. These ids are used by the _get_article_text
        function to request articles.
        """
        query = \
                        'https://' + language_id \
                        + '.wikipedia.org/w/api.php?format=json&action=query&list=random&rnlimit=' \
                        + str(number_of_articles) + '&rnnamespace=0'

        # reads the response into a json object that can be iterated over
        data = json.loads(requests.get(query).text)

        # collects the ids from the json
        ids = []
        for article in data['query']['random']:
            ids.append(article['id'])

        return ids


    def _get_article_text(self, language_id, article_id_list):
        """
        This function takes a list of articles and yields a tuple (article_title, article_text).
        """
        for idx in article_id_list:
            idx = str(idx)
            query = \
                            'https://' + language_id \
                            + '.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&pageids=' \
                            + idx + '&redirects=true'

            data = json.loads(requests.get(query).text)

            try:
                title = data['query']['pages'][idx]['title']
                text_body = data['query']['pages'][idx]['extract']
            except KeyError as error:
                # if nothing is returned for the request, skip to the next item
                # if it is important to download a precise number of files
                # then this can be repeated for every error to get a new file
                # but getting a precise number of files shouldn't matter
                print(error)
                continue

            def clean(text):
                """
                Sanitizes the document by removing HTML tags, citations, and punctuation. This
                function can also be expanded to remove headers, footers, side-bar elements, etc.
                """
                match_tag = re.compile(r'(<[^>]+>|\[\d+\]|[,.\'\"()])')
                return match_tag.sub('', text)

            yield title, clean(text_body)


    def write_articles(self, language_id, number_of_articles, db_location):
        """
        This writes articles to the location specified.
        """
        articles = self._get_random_article_ids(language_id, number_of_articles)
        text_list = self._get_article_text(language_id, articles)

        for title, text in text_list:
            # slugify the title (make a valid UNIX filename)
            title = "".join(x for x in title if x.isalnum())
            with open(db_location + '/' + title + '.txt', 'w+') as wikipedia_file:
                wikipedia_file.write(text)



class Database(object):
    """
    This creates a SQLite database with two tables, "train" and "test." Each table
    has data from each language. This object has the public method write_categories,
    which takes as its arguments a language, a training text, and a test text. It
    writes this information to the proper table.
    """

    def __init__(self, database_name):
        # This can easily be exchanged for a different database, like postgres.
        self.engine = create_engine('sqlite:///' + database_name + '.db')
        self.metadata = MetaData()

        # Table that contains the training data.
        self.train = Table('train', self.metadata,
                           Column('language', String, primary_key=True),
                           Column('text', Text)
                          )

        # Table that contains the test data.
        self.test = Table('test', self.metadata,
                          Column('language', String, primary_key=True),
                          Column('text', Text)
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
