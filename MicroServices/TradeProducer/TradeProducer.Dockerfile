FROM python:3.11-slim-bookworm

#Adding /app to the PYTHONPATH to import config module containing Parametrized Values
ENV PYTHONPATH=/app

#Setting PYTHONBUFFERED to stream Python Output to the Console
ENV PYTHONBUFFERED=1

#Setting up Poetry with specific version as localhost, to ensure nothing breaks or conflicts - we want the build to be Fully Reproducible.
RUN pip install poetry==1.8.3

WORKDIR /app

#First Copying and Installing Poetry Virtual Environment for faster build since most things can be Cached when rebuilding the image.
#When copying more than a file, destination Dir must end with a Trailing /
COPY pyproject.toml poetry.lock /app/

#Install Poetry Virtual Environment and Dependencies
RUN poetry install

#Copying all source code into the container, this can't be cached if anything in the code changes, so last Command before Entrypoint.
COPY . /app

#Command to Run when Container Run
ENTRYPOINT ["poetry", "run", "python", "source/ProducerQuixStreamsApp.py"]

#docker build -t tradeproducer . -f TradeProducer.Dockerfile
#docker run --network redpanda-network --name tradeproducer -d -it tradeproducer