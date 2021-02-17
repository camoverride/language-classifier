"""
This module exposes the function identify, which is used to classify the language of a span
of text. The global variables MODEL_NAME and MODEL_VERSION determine which model the API
will serve.
"""
import joblib
from languages import LANGUAGES


MODEL_NAME = "NB_classif"
MODEL_VERSION = "1"


def identify(phrase, model_name=MODEL_NAME, model_version=MODEL_VERSION):
    """
    This function accepts a model (along with its version) and a phrase and then predicts
    the language category.
    """
    # Add an extra "undetermined" index.
    language_mapping = {14: "undetermined"}

    # Add languages to their numerical mapping.
    for index, language in enumerate(LANGUAGES):
        language_mapping[index] = language

    # Generate the path to the model.
    model_path = f"modeling/models/{model_name}/{model_version}/"

    # Load the model components.
    classifier = joblib.load(f"{model_path}/classifier.pkl")
    tfidf_transformer = joblib.load(f"{model_path}/tfidf_transformer.pkl")
    count_vect = joblib.load(f"{model_path}/count_vect.pkl")

    # Apply the model.
    counts = count_vect.transform([phrase])
    tfidf = tfidf_transformer.transform(counts)
    predicted = classifier.predict(tfidf)

    return language_mapping[predicted[0]]
