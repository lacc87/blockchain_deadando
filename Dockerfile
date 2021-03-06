# pull official base image
FROM python:3.8.1-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

EXPOSE  5000

# copy project
COPY . /usr/src/app/

#CMD ["python", "manage.py", "db", "upgrade"]
#CMD ["python", "manage.py", "seed"]
#CMD ["gunicorn", "--log-level", "debug", "--bind", "0.0.0.0:5000", "app:app"]

