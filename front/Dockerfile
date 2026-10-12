FROM node:22 AS builder

ARG VITE_API_BASE_URL
ARG VITE_WS_BASE_URL
ENV VITE_API_BASE_URL=${VITE_API_BASE_URL}
ENV VITE_WS_BASE_URL=${VITE_WS_BASE_URL}

WORKDIR /app/front

# Package management
COPY ./front/package.json \
./front/pnpm-lock.yaml \
./

# Install packages
RUN npm install -g pnpm && pnpm install --frozen-lockfile

# Copy source code
COPY ./front/index.html \
  ./front/tsconfig.json \
  ./front/vite.config.ts \
  ./
COPY ./front/src ./src

RUN pnpm build

FROM caddy:2-alpine AS server

COPY --from=builder /app/front/dist /srv
