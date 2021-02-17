"""
This module exposes two objects. The first is GetArticles which can be used to grab data
from Wikipedia. This scraper also performs basic document sanitizing, such as removing
punctuation, HTML tags, and citation brackets. I recommend scraping less than 100 articles
per API call. The second object, Database, creates a SQLite database.

Language prefixes from here: https://en.wikipedia.org/wiki/List_of_Wikipedias
Trivia: https://www.quora.com/Why-are-there-so-many-articles-in-the-Cebuano-language-on-Wikipedia
"""
import os
import re
import json

import requests

import sys
sys.path.append("..")
from languages import LANGUAGES


class GetWikiArticles(object):
    """
    This is an object with the public method write_articles(language_id, number_of_articles,
    db_location). This writes sanitized articles to text files in a specified location.
    """
    def __init__(self, data_path):
        self.data_path = data_path


    def _get_random_article_ids(self, language_id, number_of_articles):
        """
        Makes a request for random article ids. "rnnamespace=0" means that only articles are chosen,
        as opposed to user-talk pages or category pages. These ids are used by the _get_article_text
        function to request articles.
        """
        query = f"https://{language_id}.wikipedia.org/w/api.php?format=json&action=query&list=random&rnlimit={str(number_of_articles)}&rnnamespace=0"

        # Reads the response into a json object that can be iterated over.
        data = json.loads(requests.get(query).text)

        # collects the ids from the json
        ids = [article["id"] for article in data["query"]["random"]]

        return ids


    def _get_article_text(self, language_id, article_id_list):
        """
        This function takes a list of articles and yields a tuple (article_title, article_text).
        """
        for idx in article_id_list:
            idx = str(idx)
            query = f"https://{language_id}.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&pageids={idx}&redirects=true"

            data = json.loads(requests.get(query).text)

            try:
                title = data["query"]["pages"][idx]["title"]
                text_body = data["query"]["pages"][idx]["extract"]
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
                return match_tag.sub("", text)

            yield title, clean(text_body)


    def write_articles(self, language_id, number_of_articles):
        """
        This writes articles to the location specified.
        """
        articles = self._get_random_article_ids(language_id, number_of_articles)
        text_list = self._get_article_text(language_id, articles)

        for title, text in text_list:
            # Slugify the title (make a valid UNIX filename)
            title = "".join(char for char in title if char.isalnum())

            # Write the data.
            os.makedirs(f"{self.data_path}/{language_id}", exist_ok=True)
            with open(f"{self.data_path}/{language_id}/{title}.txt", "w+") as wiki_file:
                wiki_file.write(text)


if __name__ == "__main__":

    NUM_ARTICLES = 50
    DATA_PATH = "data"
    article_downloader = GetWikiArticles(DATA_PATH)

    for lang_id in LANGUAGES:
        article_downloader.write_articles(lang_id, NUM_ARTICLES)
