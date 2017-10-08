# `hackfsu.com` v5

## Installation

These are some notes for how to set up this repository

### Getting Started

We utilize Docker to containerize our application so that whether you are using linux, macOS, or Windows, you run exactly the same as everyone else.

There are many advantages to Docker, including automatic dependency installation, a simple deployment strategy, and increased security via sandboxed components.

1. [Get Docker](https://docs.docker.com/engine/getstarted/step_one/#/step-1-get-docker)
2. [Get Docker Compose](https://docs.docker.com/compose/install/)
3. Clone this repo: `git clone https://github.com/hackfsu/hackfsu_com`

### Webapp Development

You can launch the webapp with the following commannd:

```
docker-compose -f dev.yml up webapp
```

**Notes**:
1. Windows users may need to type `docker-compose.exe`
2. Windows users will need to edit the launch commannd, see the `dev.yml` comment below the command tag in the webapp service
3. Use `up -d` to detach from the container

### API Development

TODO add more content

#### API v5 note
Dockerfile currently contains Nodejs depts for compatibility with v4. These can be removed when webpages are no longer served from the API.
