"""
This module implements a Multinomial Naive Bayes classifier using sklearn.
The classifier is saved to a pkl file for future use.
Tests are performed at the end to make sure the model is valid.
"""
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib
from sqlalchemy import create_engine

# Because our data set is small, we can save it to RAM. However, if we have a massive
# dataset, we should save the data to disk or read it from a generator.

LANGUAGES = ['en', 'sv', 'de', 'fr', 'nl', 'ru', 'it', 'es', 'pl', 'vi', 'pt', 'uk', 'fa', 'sco'
            ]

TRAINING_DATA = []

# Connect to database and read information into the TRAININ_DATA list.
db = create_engine('sqlite:///scraper/language_data.db')
conn = db.connect()
res = conn.execute('select * from train')
for row in res:
    TRAINING_DATA.append(row['text'])


TRAINING_SET = np.array(TRAINING_DATA) #np.concatenate([language for language in TRAINING_DATA])

# Read in the target int for each language.
TARGETS = np.array([i for i in range(len(LANGUAGES))])

# This  turns a collection of text data into a matrix of frequency counts.
COUNT_VECT = CountVectorizer()
TRAIN_COUNTS = COUNT_VECT.fit_transform(TRAINING_SET)

# tfidTransformer scales down the impact of very frequent tokens -- things like stopwords.
# http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfTransformer.html
TDIDF_TRANSFORMER = TfidfTransformer()
TRAIN_TFIDF = TDIDF_TRANSFORMER.fit_transform(TRAIN_COUNTS)

# Train a multinomial Naive Bayes classifier.
CLASSIFIER = MultinomialNB().fit(TRAIN_TFIDF, TARGETS)

# Save the results of the classifier and the vectorizer so that it does not need to be trained at runtime.
joblib.dump(COUNT_VECT, 'model/count_vect.pkl')
joblib.dump(TDIDF_TRANSFORMER, 'model/tdidf_transformer.pkl')
joblib.dump(CLASSIFIER, 'model/classifier.pkl')
