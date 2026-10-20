FROM astral/uv:python3.12-bookworm-slim

WORKDIR /app/server


# Package management
COPY ./server/requirements.txt .

# Install packages
RUN --mount=type=cache,target=/root/.chache/uv \
    uv pip sync requirements.txt --system

# Copy source code
COPY ./server/src ./src

EXPOSE 8000

ENTRYPOINT ["python", "src/server.py"]

