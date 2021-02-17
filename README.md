# language-classifier

See [the website](https://camtsmith.com/articles/2017-10/naive-bayes-text-classification) for a tutorial.

## Install

Install dependencies with conda:
`conda create --name language_classifier python=3.8`
`conda activate language_classifier`
`conda install --file requirements.txt`


## Run the app locally

Run the web application:
`python3 app.py`

View the application:
`http://127.0.0.1:5000`

Run the model API:
`python3 api.py`

Test out the API:
`curl http://127.0.0.1:5001//identify -d "data=Le commerce n'est pas un monstre et la publicité" -X GET`


## The data pipeline

Download some data from Wikipedia:
`cd scraper && python3 get_data.py`

Generate a SQLite database:
`create_database.py`

Explore the data:
`sqlite3 language_data_1.db`
`> SELECT * FROM train WHERE language = "en" LIMIT 100;`

Make a model:
`cd ../modeling && python3 generate_model.py`

Test the model:
`python3 test_model.py`


## How to put this into production

You should deploy the web application `app.py` to _Heroku_ or something. Then you should deploy `api.py` to GCP or AWS. You'll need to fiddle with the requirements for each of these apps as well as the DNS so the servers can talk to each other.

## Caveats
- This application was designed with teaching in mind, so there are some simplifications.
- This application has three distinct severs: a web app, a model API, and a SQL database. When run locally, these distinctions don't matter, but when you deploy an app like this, these pieces will all be distinct servers.
- All the dependencies here are global - if this was deployed, not all dependencies would need to be shared between servers.
