FROM node:alpine3.21

RUN mkdir -p app

WORKDIR /app

COPY . .

RUN rm -rf node_modules

RUN rm -rf local

RUN npm install

RUN npm run build

EXPOSE 5173

CMD ["npm", "run", "dev"]
