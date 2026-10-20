FROM node:22

WORKDIR /app/front

# Package management
COPY ./front/package.json \
  ./front/pnpm-lock.yaml \
  ./

  # Install packages
RUN corepack enable && pnpm install --frozen-lockfile

# Copy source code
COPY ./front/index.html \
  ./front/tsconfig.json \
  ./front/vite.config.ts \
  ./
COPY ./front/src ./src

EXPOSE 5173

ENTRYPOINT ["pnpm", "dev", "--host", "0.0.0.0"]
