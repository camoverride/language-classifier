# language-classifier

[See a demo in production!](https://language-identifier-app.herokuapp.com/)

Test out the API:

~~~shell
curl https://language-identifier-app.herokuapp.com/identify -d "data=Le commerce n'est pas un monstre et la publicité" -X GET
~~~

See [the website](https://camtsmith.com/articles/2021-02/how-to-build-ml-app-from-scratch) for a tutorial.

This repo is an example of how to build a machine learning application from scratch! This is a simple web application that uses the [Naive Bayes](https://en.wikipedia.org/wiki/Naive_Bayes_classifier#Multinomial_na%C3%AFve_Bayes) algorithm to classify a string of text as belonging to one of several languages.

This application has a front-end built in Flask, a model server created with flask_restful, and a database in SQLite. Data is downloaded from Wikipedia.


## Install

Install dependencies with conda:

~~~shell
conda create --name language_classifier python=3.8
conda activate language_classifier
pip install -r requirements.txt
~~~


## Run the app locally

Run the web application:

~~~shell
export FLASK_APP=app.py
flask run
~~~

Or:

~~~shell
python app.py
~~~

View the application:

~~~shell
http://127.0.0.1:5000
~~~

Run the model API:

~~~shell
python api.py
~~~

Test out the API:

~~~shell
curl http://127.0.0.1:5001//identify -d "data=Le commerce n'est pas un monstre et la publicité" -X GET
~~~


## The data pipeline

Download some data from Wikipedia:

~~~shell
cd scraper && python get_data.py
~~~

Generate a SQLite database:

~~~shell
create_database.py
~~~

Explore the data:

~~~shell
$ sqlite3 language_data.db
> SELECT language, title FROM wiki_data LIMIT 25;
~~~

Make and test model (run all cells in this notebook):

~~~shell
cd ../modeling
jupyter lab create_model.ipynb
~~~

Deploy the model by editing the following lines in `classify_language.py`:

~~~shell
MODEL_NAME = "NB_classif"
MODEL_VERSION = "1"
~~~


## How to put this into production

You should deploy the web application `app.py` to _Heroku_ or something. Then you should deploy `api.py` to GCP or AWS. You'll need to fiddle with the requirements for each of these apps as well as the DNS so the servers can talk to each other.

## Caveats
- This application was designed with teaching in mind, so there are some simplifications.
- This application has three distinct severs: a web app, a model API, and a SQL database. When run locally, these distinctions don't matter, but when you deploy an app like this, these pieces will all be distinct servers.
- All the dependencies here are global - if this was deployed, not all dependencies would need to be shared between servers.
