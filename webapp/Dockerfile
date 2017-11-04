FROM node:8
RUN npm install -g nodemon

WORKDIR /usr/src/app

COPY package.json .
COPY package-lock.json .

RUN yarn install

ADD . .

EXPOSE 3000
CMD ["yarn", "start"]
