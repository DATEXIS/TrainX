FROM node:lts-alpine

WORKDIR /app

COPY package.json ./
RUN npm install

COPY .eslint* ./
COPY vue.config.js ./
COPY .postcssrc.js ./
COPY src/ ./src/
COPY build/ ./build/
COPY static/ ./static/
COPY public/ ./public/

EXPOSE 4200
CMD [ "npm", "start" ]