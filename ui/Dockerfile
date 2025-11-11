FROM node:22-slim AS build

WORKDIR /app

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
