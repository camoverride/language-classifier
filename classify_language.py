"""
This module exposes the function identify, which is used to classify the language of a span
of text. The global variables MODEL_NAME and MODEL_VERSION determine which model the API
will serve.
"""
import joblib


# Global variables for selecting the model.
MODEL_NAME = "NB_classif"
MODEL_VERSION = "1"
MODEL_PATH = f"modeling/models/{MODEL_NAME}/{MODEL_VERSION}"


# Load the model components.
classifier = joblib.load(f"{MODEL_PATH}/classifier.pkl")
tfidf_transformer = joblib.load(f"{MODEL_PATH}/tfidf_transformer.pkl")
count_vect = joblib.load(f"{MODEL_PATH}/count_vect.pkl")
label_encoder = joblib.load(f"{MODEL_PATH}/label_encoder.pkl")

# Define a class that performs all the steps in our model pipeline.
class ModelPipeline(object):
    def __init__(self, classifier, count_vect, tfidf_transformer, inverse_encoder):
        self.classifier = classifier
        self.count_vect = count_vect
        self.tfidf_transformer = tfidf_transformer
        self.inverse_encoder = inverse_encoder
        
    def classify(self, text):
        """
        This method accepts a list of phrases and returns a list of the languages that
        they belong to. In production, only a list of len=1 is allowed.
        """
        counts = self.count_vect.transform(text)
        tfidf = self.tfidf_transformer.transform(counts)
        pred = self.classifier.predict(tfidf)
    
        return self.inverse_encoder.inverse_transform(pred)
    
model = ModelPipeline(classifier, count_vect, tfidf_transformer, label_encoder)
