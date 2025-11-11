FROM node:22-slim AS build

WORKDIR /app

ARG PUBLIC_API_URL=http://localhost:8080
ENV PUBLIC_API_URL=$PUBLIC_API_URL

COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:22-slim

WORKDIR /app

COPY --from=build /app/build ./build
COPY package*.json ./

RUN npm ci --omit=dev

EXPOSE 3000

CMD ["node", "build"]
