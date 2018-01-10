"""
This module contains a function, identify(), that returns the identity of a phrase's
language. Other models can be tested by importing a different CLASSIFIER.
"""
from sklearn.externals import joblib
from languages import LANGUAGES

CLASSIFIER = joblib.load('model/classifier.pkl')
TDIDF_TRANSFORMER = joblib.load('model/tdidf_transformer.pkl')
COUNT_VECT = joblib.load('model/count_vect.pkl')


# Because Naive Bayes maps its results to integers, it's necessary to map the language codes to ints
# len(languages) + 1 must equal "undetermined"
LANGUAGE_MAPPING = {14: "undetermined"}

for index, language in enumerate(LANGUAGES):
    LANGUAGE_MAPPING[index] = language


def identify(phrase):
    """
    Imports our model and necessary information and then identifies which language
    the phrase belongs to.
    """
    counts = COUNT_VECT.transform([phrase])
    tfidf = TDIDF_TRANSFORMER.transform(counts)
    predicted = CLASSIFIER.predict(tfidf)

    return LANGUAGE_MAPPING[predicted[0]]
