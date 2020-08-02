# Glimpse backend prototype
## basic app for video chat room

### To run:
### 1. create virtual env `python3 python3 -m venv .venv`
### 2. `source .venv/bin/activate`
### 3. `pip install -r requirements.txt`
### 4. If you update DB schema, replace db file using python REPL
```
$ rm main/db.sqlite
$ python
>>> from main import db, create_app
>>> db.create_all(app=create_app())
```
### 5. run `FLASK_DEBUG=1 FLASK_APP=main flask run` from app/
### 6. App will be available at `http://localhost:5000/`, can use request tools like Postman to test new APIs
