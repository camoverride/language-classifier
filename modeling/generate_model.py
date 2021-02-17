import os
import sys
import joblib

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sqlalchemy import create_engine

sys.path.append("..")
from languages import LANGUAGES


def get_version(model_name):
    """
    Get the model version number. If the model name does not yet exist in the models directory,
    then it's created. If other versions of the model exist, then the highest version number is
    found and incremented by 1 for the new version. This path is also created.
    """
    if model_name not in os.listdir("models"):
        os.makedirs(f"models/{model_name}/1")
        return "1"
    else:
        versions = os.listdir(f"models/{model_name}")
        version = str(max([int(i) for i in versions]) + 1)
        os.makedirs(f"models/{model_name}/{version}")
        print(version)
        return version


def generate_model(model_name, database_path):
    """
    This function reads a sqlite database and implements a Multinomial Naive Bayes classifier
    using sklearn. The classifier is saved to a pkl file for future use. Version numbers are
    generated automatically.
    """
    # Connect to database and read training data into the training_data list.
    db = create_engine(database_path)
    conn = db.connect()
    res = conn.execute("select * from train")

    training_data = []
    for row in res:
        training_data.append(row["text"])

    training_set = np.array(training_data)

    # Read in the target int for each language.
    targets = np.array([i for i in range(len(LANGUAGES))])

    # This  turns a collection of text data into a matrix of frequency counts.
    count_vect = CountVectorizer()
    train_counts = count_vect.fit_transform(training_set)

    # tfidTransformer scales down the impact of very frequent tokens - things like stopwords.
    tfidf_transformer = TfidfTransformer()
    train_tfidf = tfidf_transformer.fit_transform(train_counts)

    # Train a multinomial Naive Bayes classifier.
    classifier = MultinomialNB().fit(train_tfidf, targets)

    # Get the version number.
    version = get_version(model_name)

    # Save the results of the classifier and the vectorizer so that it does not need to be trained at runtime.
    joblib.dump(count_vect, f"models/{model_name}/{version}/count_vect.pkl")
    joblib.dump(tfidf_transformer, f"models/{model_name}/{version}/tfidf_transformer.pkl")
    joblib.dump(classifier, f"models/{model_name}/{version}/classifier.pkl")


if __name__ == "__main__":
    MODEL_NAME = "NB_classif"
    DATABASE_PATH = "sqlite:///../scraper/language_data.db"

    generate_model(MODEL_NAME, DATABASE_PATH)
