FROM node:18.17-alpine3.18 AS production
ENV NODE_ENV production

WORKDIR /react

COPY package.json ./
COPY package-lock.json ./
COPY . .

RUN npm install
RUN npm install react-scripts@5.0.1 -g


CMD ["npm", "start"]