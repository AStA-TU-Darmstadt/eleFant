FROM python:3.5
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code

# install dependencies
ADD requirements.txt .
RUN pip install -r requirements.txt

# install server dependencies
RUN apt-get update && apt-get install -y \
        nginx-extras \
        # needed to check for database connection:
        netcat-openbsd

# make nginx log to stdout to make logs accessible via docker logs
RUN ln -sf /dev/stdout /var/log/nginx/access.log && ln -sf /dev/stderr /var/log/nginx/error.log

# start new django project
RUN django-admin startproject django_project
# add elefant as django app
ADD elefant django_project/elefant/

# add custom configuration files
ADD docker_files/django_config django_project/django_project/
ADD docker_files/uwsgi.ini .
ADD docker_files/nginx.conf /etc/nginx/sites-enabled

# add startup script
ADD docker_files/run.sh .
CMD ["./run.sh"]
