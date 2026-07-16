# ---------- Stage 1: Build ----------
# Baut die React-App zu statischen Dateien (dist/)
FROM node:22-alpine AS build

WORKDIR /app

# Erst nur package*.json → Layer-Cache für npm ci
COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build

# ---------- Stage 2: Serve ----------
# Nur der Webserver + die gebauten Dateien – kein Node, kein Quellcode.
# Ergebnis: kleines, sauberes Produktions-Image.
FROM nginx:alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
