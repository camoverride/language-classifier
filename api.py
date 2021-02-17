"""
This is a simple restful API that exposes a single route, "identify", which returns the identity
of a language given a sample of its text. To test this API manually, use the following shell command:

curl http://127.0.0.1:5001//identify -d "data=Le commerce n'est pas un monstre et la publicité" -X GET
"""

from flask import Flask, request
from flask_restful import Resource, Api
from classify_language import identify


app = Flask(__name__)
api = Api(app)


# This is our API class. This accepts text data and returns the language abbreviation.
class LanguageIdentifier(Resource):
    def get(self):
        return {"language": identify(request.form["data"])}

api.add_resource(LanguageIdentifier, "/identify")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)
