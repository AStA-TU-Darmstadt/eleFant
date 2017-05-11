FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code

# install dependencies
ADD requirements.txt .
RUN pip install -r requirements.txt

# start new django project and add EleFAnt to it
RUN django-admin startproject django_project
ADD elefant django_project/elefant/
# add custom configuration files
ADD docker_files/settings.py django_project/django_project/
ADD docker_files/urls.py django_project/django_project/

# add startup script
ADD docker_files/run.sh .

# install server dependencies
RUN apt-get update && apt-get install -y \
        nginx-extras \
        uwsgi \
        uwsgi-plugin-python3 \
        # needed to check for database connection:
        netcat
