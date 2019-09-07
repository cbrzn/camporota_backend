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

FLASK_ENV=development
DATABASE_URL=postgres://vczqpoxvzftnfn:c56ef4f4653753b8132867c4f5330d9bbc0693875952a735e7c0ddca72e3a6c2@ec2-54-228-246-214.eu-west-1.compute.amazonaws.com:5432/d2mktdfobkr16q

## Or you can just use the docker container
```
docker pull cbrzn/camporota_backend
docker run -i -t -p 5000:5000 cbrzn/camporota_backend
```