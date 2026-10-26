FROM python:3.12-slim

WORKDIR /app/server

# Create virtual environment
RUN python -m venv .venv
ENV PATH="/app/front/.venv/bin:$PATH"

# Package management
COPY ./server/requirements.txt .

# Install packages
RUN pip install -r requirements.txt

# Copy source code
COPY ./server/src ./src

CMD ["python", "src/server.py"]

EXPOSE 8000
