FROM python:3.7
COPY . /app
WORKDIR /app
RUN pip install pipenv
RUN pipenv install
ENTRYPOINT ["python"]
CMD ["main.py"]