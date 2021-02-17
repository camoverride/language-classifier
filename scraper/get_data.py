"""
This module exposes the class GetWikiArticles which is used to download and sanitize Wikipedia
articles, downloading them as .txt files to a specified directory. I recommend downloading less
than 100 articles per language at a time, as Wikipedia's servers might decide to block or limit
your IP address.

The number of articles that are downloaded are set as a fraction of the total number of Wikipedia
articles for the given language. The default fraction is 0.00001. For instance, there are 6 million
articles in English, so: 6000000 * 0.00001 = 60 articles will be downloaded. However, keep in mind
that some languages like Cebuano are over-represented, so depending on how you intend this app to
be used, you may want to modify the data distribution by language.

https://www.quora.com/Why-are-there-so-many-articles-in-the-Cebuano-language-on-Wikipedia
"""
import os
import re

import requests

import sys
sys.path.append("..")
from languages import LANGUAGE_STATS


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
        try:
            data = requests.get(query).json()

        except requests.exceptions.ConnectionError:
            print("\nYou are requesting too much data! Wikipedia is blocking you. Wait a bit and try again.")
            sys.exit()

        # Collects the ids from the json.
        ids = [article["id"] for article in data["query"]["random"]]

        return ids


    def _get_article_text(self, language_id, article_id_list):
        """
        This function takes a list of articles and yields a tuple (article_title, article_text).
        """
        for idx in article_id_list:
            idx = str(idx)
            query = f"https://{language_id}.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&pageids={idx}&redirects=true"

            data = requests.get(query).json()

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

    # Location the actual articles will be downloaded
    DATA_PATH = "data"

    # What proportion of all the wiki articles are downloaded.
    # There are 6 million English articles, so 6000000 * 0.00001 = 60 articles.
    DATA_FRAC = 0.00001

    article_downloader = GetWikiArticles(DATA_PATH)
    
    for language, language_id, num_articles, _ in LANGUAGE_STATS:
        num_articles_to_download = int(num_articles * DATA_FRAC)

        # Debug
        print(f"\nDownloading {num_articles_to_download} articles in {language} ", end="")

        # Download articles for the given language.
        article_downloader.write_articles(language_id, num_articles_to_download)
