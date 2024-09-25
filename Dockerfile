FROM python:3.11

WORKDIR /code

COPY poetry.lock pyproject.toml ./
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

COPY ./app /code/app

CMD ["fastapi", "run", "app/main.py", "--port", "8000"]