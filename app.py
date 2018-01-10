"""
This is a flask server. This renders a web page and handles user requests. When a user
enters a phrase, this server returns the identify() function with the phrase as its argument.
"""
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_restful import Resource, Api
from checklanguage import identify


app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_KEY'

# Pretty CSS and HTML for website.
bootstrap = Bootstrap(app)


class LanguageForm(FlaskForm):
    """
    This is a form where users will type/paste snippets of the language they want to identify.
    """
    language = StringField('Enter a phrase:', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    This is the website's main route. Only one route needs to be defined for this application.
    """
    phrase = None
    language = None
    form = LanguageForm()
    if form.validate_on_submit():
        phrase = form.language.data
        language = identify(form.language.data)
        form.language.data = ''
    return render_template('index.html', form=form, phrase=phrase, language=language)


# Create an API
api = Api(app)

class TodoSimple(Resource):
    """
    This is our API class. It only exposes one call.
    """
    def get(self):
        return {'language': identify(request.form['data'])}

api.add_resource(TodoSimple, '/identify')


if __name__ == '__main__':
    app.run()
