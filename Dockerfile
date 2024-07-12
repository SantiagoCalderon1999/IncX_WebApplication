FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y \
    curl \
    libpq-dev \
    build-essential \
    ffmpeg \
    libsm6 \
    libxext6 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/usr/local python3 -

ENV PATH="/usr/local/bin:$PATH"

COPY ./ .

RUN poetry config virtualenvs.create false && \
    poetry install --no-root

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
