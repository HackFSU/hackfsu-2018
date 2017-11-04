# `hackfsu.com` v5

## Installation

These are some docs on how to set up this repository.

### Getting Started

We utilize Docker to containerize our application so that whether you are using linux, macOS, or Windows, you run exactly the same as everyone else.

There are many advantages to Docker, including automatic dependency installation, a simple deployment strategy, and increased security via sandboxed components.

1. [Get Docker](https://docs.docker.com/engine/getstarted/step_one/#/step-1-get-docker)
2. [Get Docker Compose](https://docs.docker.com/compose/install/)
3. Clone this repo: `git clone https://github.com/hackfsu/hackfsu_com`

*Also see `/docs/Docker.md` for details on what to install and how to configure your Docker hosts.*

### Docker Compose Configs
We provide several Compose configurations in the `.docker` folder. We recommend copying the `dev.yml` configuration into the project root as `docker-compose.yml`, so you may use the `docker-compose ...` commands without the `-f .docker/dev.yml` option. You also can customize the `docker-compose.yml` file to your liking as it will be ignored by git. 

To reiterate; if you choose the use a `docker-compose.yml` file you can use `docker-compose [command]`, otherwise you will need `docker-compose -f <.docker/compose_file> [command]`. 

*Also see README.md in the `.docker` folder for a full list of pre-made configurations and details on environmental variable configuration.*

## Contributing

Before starting, see `/docs/IDEs.md` for instructions on configuring Pycharm (API development) or Webstorm (Webapp development).

### Webapp Development

You can launch the webapp with the following commannd:

```
docker-compose up webapp
```

If you want to connect to use the local API, don't include the webapp tag. Also, see the **Database Migration** section under **API Development**.

**Notes**:
1. Windows users may need to type `docker-compose.exe`.
2. Windows users will need to edit the launch commannd, see the `dev.yml` comment below the command tag in the webapp service.
3. Use `up -d` to detach from the container.

### API Development
Be sure to setup Pycharm per `/docs/IDEs.md` before starting.

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
docker-compose [-f compose_file] run api python manage.py createsuperuser
```

Then, log in at `<hostname>/login`. Then navigate to `<hostname>/admin/django`, and click on the `hackathon` class. Create a hackathon object and check the `current` checkbox.

#### API v5+ and the v4 Webapp
HackFSU 4 hosted the website as static files served by Django. These files were built using Node.js + Gulp. 

Currently the API/Dockerfile contains instructions for compatibility with the v4 webapp. However, the Docker Compose volumes directive to mount the API for development causes some sort of conflict with the build step and the templates are not rendered into pages. 

To use the legacy site, disable the volume flag in the Compose file. 

Eventually we will remove the legacy site from the API, and this notice should also be removed. 
