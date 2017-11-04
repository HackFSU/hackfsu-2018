# Docker Compose Configurations
Available configurations for this project. 

#### `base.yml`
Base definitions of our codebase (`webapp` + `api`) and directly dependant database. 

#### `dev.yml`
Extends `base.yml` with extra options for ease of development. Copy this as `docker-compose.yml` to the root of the project. 

#### `production.yml` 
(TODO) Will extend `base.yml` and add deployment containers such as Nginx. 

## Environment Variables
You need to set these on your host or manually write them in the
a compose file – BUT DO NOT COMMIT ANY PASSWORDS TO SOURCE CONTROL.

#### `APP_DEBUG`
Debug variable for Django API. If this is set at all, it risks triggering debug mode.

#### `POSTGRES_PASSWORD`
Sets the password for the postgres contna
