FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y \
    curl \
    libpq-dev \
    build-essential \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/usr/local python

COPY . .

RUN poetry config virtualenvs.create false
RUN poetry install

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]