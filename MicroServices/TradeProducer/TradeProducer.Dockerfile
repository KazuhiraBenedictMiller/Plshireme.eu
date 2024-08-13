FROM python:3.11-slim-bookworm

RUN pip install poetry

WORKDIR /app

#Copying all source code into the container
COPY . /app

#Install Poetry Virtual Environment and Dependencies
RUN poetry install

#Command to Run when Container Run
ENTRYPOINT ["poetry", "run", "python", "source/ProducerQuixStreamsApp.py"]

#docker build -t tradeproducer . -f TradeProducer.Dockerfile
#docker run --network redpanda-network --name tradeproducer -d -i -t tradeproducer