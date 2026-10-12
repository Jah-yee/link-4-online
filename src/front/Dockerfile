FROM node:22

WORKDIR /app

COPY index.html .
COPY package.json .
COPY tsconfig.json .
COPY vite.config.ts .
COPY pnpm-lock.yaml .
COPY src/front ./src/front/

RUN npm install -g pnpm && pnpm install

CMD ["pnpm","dev","--host"]

EXPOSE 5173

