[![Build Status](https://travis-ci.com/cbrzn/camporota_backend.svg?token=M9Rvxc6FJxunVdovxho3&branch=master)](https://travis-ci.com/cbrzn/camporota_backend)
# Camporota back end
## Installation
Make sure the following dependencies are satisfied
```
python 3.7 and pip
```
Install the pipenv
```
pip install pipenv
pipenv install
pipenv shell
python app.py
```
#### Setup environment variables

Add a `.env` file in the root of the project and paste this:
```
FLASK_ENV=development
DATABASE_URL=
```
## Or you can just use the docker container
```
docker pull cbrzn/camporota_backend
docker run -i -t -p 5000:5000 cbrzn/camporota_backend
```
