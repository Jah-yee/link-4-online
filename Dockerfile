FROM node:22 As frontend-builder

WORKDIR /app

COPY index.html .
COPY package.json .
COPY tsconfig.json .
COPY vite.config.ts .
COPY pnpm-lock.yaml .
COPY src/front ./src/front/

RUN npm install -g pnpm && pnpm install && pnpm build


FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
COPY ./src/server ./src/server
COPY --from=frontend-builder /app/dist ./dist

RUN pip install -r requirements.txt

CMD ["python","src/server/server.py"]

EXPOSE 8000

