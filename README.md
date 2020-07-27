# PyPiIndex
PyPiIndex is application that fetches newest PyPi packages based on https://pypi.org/rss/packages.xml once a day and indexes them on elasticsearch engine(using huey task queue). You can search indexed packages by html search or using REST API for example:
HTML: [http://localhost:8000/?search=python](http://localhost:8000/?search=python)
API: [http://localhost:8000/api/packages/?search=python&offset=0&limit=100](http://localhost:8000/api/packages/?search=python&offset=0&limit=100)

## Local Installation
Make sure you have run local instances of elasticsearch and redis (app uses default settings for them). Make virtual env with python3.7 and run following commands in project directory:
```
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
python manage.py run_huey
```

## Settings

You can set how many records per page can be displayed on html search by changing `ELASTICSEARCH_PAGINATE_BY` constant in `settings.py` file for example:
`ELASTICSEARCH_PAGINATE_BY=25`

## Restore es index
In case if you lose data from elasticsearch, app backups everything in sqlite database, to rebuild elasticsearch index all you need to do is run following command:
`python manage.py search_index –rebuild` and index should be rebuilt.
