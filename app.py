"""
This is a flask server. This renders a web page and handles user requests. When a user
enters a phrase, this server sends a request to the identify api server, which returns
the identity of the language. This is then rendered on the webpage.

Test the API:
    curl http://127.0.0.1:5000//identify -d "data=Le commerce n'est pas un monstre et la publicité" -X GET
"""
from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_restful import Resource, Api
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

from classify_language import model


app = Flask(__name__)
api = Api(app)
app.config["SECRET_KEY"] = "SECRET_KEY"

# Pretty CSS and HTML for website.
bootstrap = Bootstrap(app)

# This is our API class. This accepts text data and returns the language abbreviation.
class LanguageIdentifier(Resource):
    def get(self):
        # The final [0] prevents the user from sending a large list of requests.
        response = model.classify([request.form["data"]])[0]
        return {"language": response}

api.add_resource(LanguageIdentifier, "/identify")


# This is a form where users will type/paste snippets of the language they want to identify.
class LanguageForm(FlaskForm):
    language = StringField("Enter a phrase:", validators=[DataRequired()])
    submit = SubmitField("Submit")


# This is the website's main route. Only one route needs to be defined for this application.
@app.route("/", methods=["GET", "POST"])
def index():
    phrase, response = None, None
    form = LanguageForm()
    if form.validate_on_submit():
        phrase = form.language.data
        response = model.classify([phrase])[0]
        form.language.data = ""
    return render_template("index.html", form=form, phrase=phrase, language=response)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port="5000", debug=True)
