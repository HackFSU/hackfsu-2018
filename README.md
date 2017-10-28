# `hackfsu.com` v5

## Installation

These are some notes for how to set up this repository

### Getting Started

We utilize Docker to containerize our application so that whether you are using linux, macOS, or Windows, you run exactly the same as everyone else.

There are many advantages to Docker, including automatic dependency installation, a simple deployment strategy, and increased security via sandboxed components.

1. [Get Docker](https://docs.docker.com/engine/getstarted/step_one/#/step-1-get-docker)
2. [Get Docker Compose](https://docs.docker.com/compose/install/)
3. Clone this repo: `git clone https://github.com/hackfsu/hackfsu_com`

### Docker Compose Configs
Existing configs for `docker-compose` exist already in the `.docker` folder of the project root. We recommend copying the

## Contributing

### Webapp Development

You can launch the webapp with the following commannd:

```
docker-compose -f dev.yml up webapp
```

If you want to connect to use the local API, don't include the webapp tag. Also, see the **Database Migration** section under **API Development**.

**Notes**:
1. Windows users may need to type `docker-compose.exe`
2. Windows users will need to edit the launch commannd, see the `dev.yml` comment below the command tag in the webapp service
3. Use `up -d` to detach from the container

### API Development

#### Database Migration
The first time the API launches, you need to apply the database migrations.

```bash
docker-compose [-f compose_file] run api python manage.py migrate
```

#### Setting current hackathon
The core of the system requires a `hackathon` object to function. In order to set this up, you need to:
1. Create and login with a superuser account
2. Create a hackathon object


Create a superuser using an email address as the username.
```bash
docker-compose [-f compose file] run api python manage.py createsuperuser
```

Then, log in at `<hostname>/login`. Then navigate to `<hostname>/django/admin`, and click on the `hackathon` class. Create a hackathon object and check the `current` checkbox.

#### API v5 note
Dockerfile currently contains Nodejs depts for compatibility with v4. These can be removed when webpages are no longer served from the API.
