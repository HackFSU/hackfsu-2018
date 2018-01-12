#   Build this Dockerfile as hackfsu/api-base.
#

FROM python:3.6
WORKDIR /usr/src/app

#
#   Install dependencies for Node.js, NPM, and Gulp
#

RUN curl -sL https://deb.nodesource.com/setup_6.x | bash - \
    && apt-get install -y nodejs

RUN npm install -g gulp

#
#   Install NPM dependencies used for rendering .pug and
#   .sass files for legacy site.
#


COPY package.json ./
RUN npm install

#
#   Install PostgreSQL dependencies
#

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*


