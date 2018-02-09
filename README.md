# `hackfsu.com` v5
Welcome to the HackFSU Webapp & API repository.

### Table of Contents
1. [Webapp Setup](#webapp)
2. [API Setup](#api)
3. [Docker Installation](#docker)

## Webapp

We don't recommend using Docker for webapp development. We _do_ recommend [Yarn](https://yarnpkg.com).

Install the dependencies by typing `yarn` and then launch the Express app with `yarn dev`. This will use `nodemon` to automatically relaunch the app when you change things.

### PugJS and Sass

Our setup uses the [Pug](https://pugjs.org/) templating language in lieu of HTML, and [Sass](http://sass-lang.com/) instead of CSS. Express automatically complies these at runtime. The Pug files are in `webapp/views` and the Sass is in `webapp/public/sass`.

#### Styles Framework: [Bulma.io](https://bulma.io)

We use Bulma for its Sass styles, which are imported and inherited by our own.

**Important note**: For the navbar, instead of following the recommended approach for the fixed navbar header padding, we use a custom navbar spacer in the base Pug template, inside the `content` block. Therefore, to keep the spacer, you must use `block append content`, and to disregard the spacer, use `block content`.

### Javascript

We have two kinds of Javascript in the webapp. The first are small scripts, some of which are inline, for UI things.

We also use Webpack to handle the registration logic. If you want to edit the registration JS, use `webpack --watch --config webpack.dev.js` to pack up the files.

## API
Also check out the Docker instructions in the next section.

### PyCharm Setup
Setup Guides for **[PyCharm](https://www.jetbrains.com/pycharm/)**. We recommend PyCharm not only as a powerful Python IDE, but also as a robust Docker Deployment UI.

#### JetBrains Student License
JetBrains, the producers of PyCharm and Webstorm, offer free student licenses which are automatically approved with a `.edu` email. Create an account and apply for a student license before proceeding, as most of the features used in this guide rely on the *Professional* editions of the software.

**Be sure to install the *Professional* editions of the software.**

#### Configure PyCharm with Docker
1. Create a run configuration via the top-right dropdown menu option "Edit Configurations".
    * Click the plus button in the top-right and select "Docker Deployment".
    * Select "Server" as your Docker Host (see **Docker Host Setup** in `.docker/README.md`).
    * Select "Deployment" as `docker-compose.yml` (see **Docker Compose Configs** above).
    * Check "Single Instance Only".
2. Add the Compose service as a remote project interpreter:
    * Open Preferences > Project: HackFSU > Project Interpreter
    * Click the options button next to the 'Project Interpreter' dropdown, select "Add Remote".
    * Select "Docker Compose" from the radio buttons.
        * Choose your Docker host as the server (same as step 1).
        * Make sure it automatically selected your `docker-compose.yml` file.
        * Service should be "api", and interpreter should be "python".

### Database Migration
The first time the API launches, you need to apply the database migrations. First, launch into the bash terminal using the API's migration file.

```bash
docker-compose -f api/migrate.yml run api bash
```
Once in the terminal, you need to apply the migrations.

```bash
python manage.py migrate
```

If you change the models at all, you'll need to make migrations and then apply them

```bash
python manage.py makemigrations
python manage.py migrate
```

### Setting current hackathon
The core of the system requires a `hackathon` object to function. In order to set this up, you need to:
1. Create and login with a superuser account
2. Create a hackathon object


Create a superuser using an email address as the username.
```bash
docker-compose run api python manage.py createsuperuser
```

Then, log in at `<hostname>/login`. Then navigate to `<hostname>/admin/django`, and click on the `hackathon` class. Create a hackathon object and check the `current` checkbox.

### API v5+ and the v4 Webapp
HackFSU 4 hosted the website as static files served by Django. These files were built using Node.js + Gulp.

The HackFSU API Dockerfile extends `hackfsu/api-base` image. We include the Dockerfile in the `api` folder as api-base.dockerfile. However, an `hackfsu/api-base` image is also hosted on the Docker Hub.

All the legacy site comes prebuilt in base, and the Dockerfile file included in API is what actually gets used to build the modern API.

## Docker

There are many advantages to Docker, including automatic dependency installation, a simple deployment strategy, and increased security via sandboxed components.

We use Docker for deploying our apps on our servers. We also use it during development for our databases and the API.

1. [Get Docker](https://docs.docker.com/engine/getstarted/step_one/#/step-1-get-docker)
2. [Get Docker Compose](https://docs.docker.com/compose/install/)
3. Clone this repo: `git clone https://github.com/hackfsu/hackfsu_com`

*Also see `.docs/Docker.md` for details on what to install and how to configure your Docker hosts.*

### Docker Compose Configs
`docker-compose.yml` is the default configuration for all components of our suite. If you want for ease of development, you can copy/edit/extend the Compose configuration to meet your needs.

You can find documentation on how to edit the Docker Compose file [here](https://docs.docker.com/compose/compose-file/compose-file-v2/).

If you choose the use a `docker-compose.yml` file you can use `docker-compose [command]`, otherwise you will need `docker-compose -f <.docker/compose_file> [command]`.
