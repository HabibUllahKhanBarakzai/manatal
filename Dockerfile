
FROM python:3.8 as build-python

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir /code
WORKDIR /code
COPY Pipfile /code
COPY Pipfile.lock /code

RUN pip install pipenv
RUN pipenv install --system --deploy

RUN apt-get update && apt-get install -y postgresql

COPY . /code
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
