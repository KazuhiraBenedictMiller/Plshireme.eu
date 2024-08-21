FROM python:3.11-slim-bookworm

ENV POETRY_NO_INTERACTION=1 \
	    POETRY_VIRTUALENVS_IN_PROJECT=1 \
	    POETRY_VIRTUALENVS_CREATE=1 \
	    POETRY_CACHE_DIR=/tmp/poetry_cache

#Adding /app to the PYTHONPATH to import config module containing Parametrized Values
ENV PYTHONPATH=/app

#Setting PYTHONBUFFERED to 1 to stream Python Output to the Console
ENV PYTHONBUFFERED=1

#Setting up Poetry with specific version as localhost, to ensure nothing breaks or conflicts - we want the build to be Fully Reproducible.
RUN pip install poetry==1.8.3

WORKDIR /app

ENV PYTHONPATH "${PYTHONPATH}:/app/src"

#First Copying and Installing Poetry Virtual Environment for faster build since most things can be Cached when rebuilding the image.
#When copying more than a file, destination Dir must end with a Trailing /
COPY pyproject.toml poetry.lock /app/

#Install Poetry Virtual Environment and Dependencies and not the Project (without 'dev' group) and Remove Cache
RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

#Copying all source code into the container, this can't be cached if anything in the code changes, so last Command before Entrypoint.
COPY . /app

#Actually wise and fast to Install the Project in the Virtual Environment to make sure
RUN poetry install --without dev

#Command to Run when Container Run
ENTRYPOINT ["poetry", "run", "python", "source/ProducerQuixStreamsApp.py"]

#docker build -t tradeproducer . -f TradeProducer.Dockerfile
#docker run --network redpanda-network --name tradeproducer -d -it tradeproducer