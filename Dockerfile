FROM python:3.7
COPY . /app
WORKDIR /app
RUN pip install pipenv \ 
    && pipenv install --system --deploy --ignore-pipfile
ENTRYPOINT ["python"]
CMD ["app.py"]