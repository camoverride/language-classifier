# language-classifier

See [the website](https://camtsmith.com/articles/2017-10/naive-bayes-text-classification) for a tutorial.

~~~shell
$ cd scraper
$ mkdir data
$ python3 create_database.py
...
$ cd ..
$ python3 model/generate_model.py
$ export FLASK_APP=app.py
$ flask run
 * Serving Flask app "app"
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
~~~
