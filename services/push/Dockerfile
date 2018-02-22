FROM node:8

# Config container
WORKDIR /usr/src/app
EXPOSE 3000

# Install deps
ADD package.json yarn.lock ./
RUN yarn

# Add files
ADD . .

CMD [ "yarn" , "start" ]
