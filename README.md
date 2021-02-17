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

Run the model API:
`python3 api.py`


## Get new data for the model


## Create new model


## Run tests


## The data pipeline

get_data.py -> create_database.py -> generate_model.py -> test_model.py -> api.py -> app.py

## How to put this into production

