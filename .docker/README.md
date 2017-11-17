# Docker Compose Configurations
Available configurations for this project.

Use the configs by copying them into the `hackfsu_com` folder as
`docker-compose.yml`.

#### `base.yml`
Base definitions of our codebase (`webapp` + `api`) and directly dependent database. Do **not** use this as your `docker-compose.yml`.

#### `dev.yml`
Extends `base.yml` with extra options for ease of development.

#### `webapp.yml`
Custom dev profile for working strictly on the webapp development.

#### `production.yml`
Configuration for deploying to the server.

## Environment Variables
You need to set these on your host or manually write them in the
a compose file – BUT DO NOT COMMIT ANY PASSWORDS TO SOURCE CONTROL.

#### `APP_DEBUG`
Debug variable for Django API. If this is set at all, it risks triggering debug mode.

#### `POSTGRES_PASSWORD`
Sets the password for the postgres contna
