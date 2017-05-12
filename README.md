# eleFant
> _Das **ele**ktronische **F**inanz**ant**ragssystem des AStAs der TU Darmstadt._

#### **_eleFant_ is currently under active developement and everything you see here may change in the future!**

*eleFant* is a tool to manage applications for financial support (Finanzanträge) at the students' council executive committee ([AStA](https://www.asta.tu-darmstadt.de)) of the TU Darmstadt university.

It is written in python using the [Django](https://www.djangoproject.com/) framework. Because eleFant is just a simple Django app you can use it in any of your Django projects. *eleFant* features a responsive and mobile friendly frontend which is built with [Material Design Lite](https://github.com/google/material-design-lite).

You are welcome to use eleFant for any purpose as long as you follow the terms of the [AGPL License](./LICENSE.md). eleFant can be customized quite easily to manage any kind of application at your university, club or association.

Although the code and all documentation for *elefant* is in English language, the frontend is currently only available in Geman.

## Installation

Currently the easiest way to get *eleFant* up and running is via `docker-compose` using the `docker-compose.yml` file coming with this repository.

After installing [docker](https://docs.docker.com/) and [docker-compose](https://docs.docker.com/compose/) you can simply do the following:
```bash
$ git clone git@github.com:AStA-TU-Darmstadt/eleFant.git
$ cd eleFant/src
$ sudo PORT=8000 EMAIL_HOST_USER=myuser EMAIL_HOST_PASSWORD=mypassword ALLOWED_HOSTS=host1.example.com,host2.example.com docker-compose up
```

`docker-compose` will create two docker containers running on your machine. One with a [PostgreSQL](https://www.postgresql.org/) Database and a second one running *eleFant* using [nginx](https://www.nginx.com/) and [uWSGI](http://uwsgi-docs.readthedocs.io/en/latest/). Using `docker-compose up -d` you can run eleFant in background. Using `docker-compose stop` you can stop the running containers. See th [docker-compose documentation](https://docs.docker.com/compose/) for more information.

### Configuration
As you see configuration parameters for eleFant are passed via environment variables. Currently all supported options are:

#### Required Settings
- **ALLOWED_HOSTS**: A comma-seperated list of allowed hosts. Django will reject any connections adressing different hosts. (e.g. "host1.example.com, host2.example.com")
- **EMAIL_HOST_USER**: The username Django will use to authenticate on your SMTP server.
- **EMAIL_HOST_PASSWORD:** The password Django will use to authenticate on your SMTP server.
- **PORT**: The port on which eleFant is served.

#### Optional Settings
- **DEBUG**: If set to `True` you will get Django's debug outputs if anything fails. This is **not** recommendet for production use. Default is `False`.
- **EMAIL_HOST**: The host of your SMTP server. Default is `localhost`.
- **EMAIL_PORT**: The port of your SMTP server. Default is `25`.
- **EMAIL_SSL_CERTFILE:** If `EMAIL_USE_SSL` or `EMAIL_USE_TLS` is `True`, you can optionally specify the path to a PEM-formatted certificate chain file to use for the SSL connection.
- **EMAIL_SSL_KEYFILE:** If `EMAIL_USE_SSL` or `EMAIL_USE_TLS` is `True`, you can optionally specify the path to a PEM-formatted private key file to use for the SSL connection.
- **EMAIL_USE_SSL:** If set to `True` Django will use a SSL connection (on port 465) to communicate with your SMTP Server. Default is `True`.
- **EMAIL_USE_TLS:** If set to `True` Django will use a TLS connection (on port 587) to communicate with your SMTP Server. Default is `False`.
- **LANGUAGE_CODE**: an IETF language code used to guess number formats. Default is `de-de`.
- **TIMEZONE**: The timezone to use. Default is `Europe/Berlin`.

#### Using a .env file
If you do not want to re-enter your settings every time you run *eleFant* you can create a `.env` file in the same directory where your `docker-compose` resides and put all your environment variables in it.
For example:

```bash
#.env
PORT=8000
EMAIL_HOST=mail.fancyhost.com
EMAIL_HOST_USER=myfancyusername
EMAIL_HOST_PASSWORD=myfancypassword
ALLOWED_HOSTS=myallowedhosts
```

## Contributing
**Code contributions and bug reports are very much appreciated.** If you found a bug please take some time to create a [GitHub Issue](https://github.com/AStA-TU-Darmstadt/EleFAnt/issues). If you want to add new features or improve the code you are welcome to submit a [pull request](https://github.com/AStA-TU-Darmstadt/EleFAnt/pulls).

## Screenshot
<img src="https://cloud.githubusercontent.com/assets/9250536/26017849/08501d9e-376c-11e7-8bda-04f5f302a351.png" alt="Screenshot"/>
