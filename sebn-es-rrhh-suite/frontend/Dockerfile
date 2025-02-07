FROM node:21-alpine
WORKDIR /app
COPY package*.json ./
RUN npm i
COPY . .
RUN npm run build
EXPOSE 8864
CMD ["npm", "run", "serve"]