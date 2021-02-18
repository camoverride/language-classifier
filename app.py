"""
This is a flask server. This renders a web page and handles user requests. When a user
enters a phrase, this server sends a request to the identify api server, which returns
the identity of the language. This is then rendered on the webpage.

This server is set to run on port 5000, whereas the API server is set to run on port 5001.
"""

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
# Remove this line if running independent model and HTML servers
from classify_language import model


app = Flask(__name__)
app.config["SECRET_KEY"] = "SECRET_KEY"

# Pretty CSS and HTML for website.
bootstrap = Bootstrap(app)

# This is the address of the model API. It may be different on your machine.
API_ROUTE = "http://127.0.0.1:5001/"

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
        # Replace this line with the below line if running independent model and HTML servers
        response = model.classify([phrase])[0]
        # response = requests.get(f"{API_ROUTE}/identify", data = {"data": phrase}).json()["language"]
        form.language.data = ""
    return render_template("index.html", form=form, phrase=phrase, language=response)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port="5000", debug=True)
