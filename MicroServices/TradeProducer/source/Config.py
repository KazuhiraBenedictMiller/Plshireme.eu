import os

from dotenv import load_dotenv

# Dinamically Crawl in search of a .env file
# load_dotenv(find_dotenv())

# Or Declaratively
load_dotenv('../.env')

TradeProducerConsumerGroup = 'TradeProducer'
ProductID = 'BTC/USD'
KrakenWebSocketChannel = 'trade'
KrakenWebSocketURL = 'wss://ws.kraken.com/v2'
KafkaBrokerAddress = os.environ['DockerInternalKafkaBrokerAddress']
KafkaInputTopic = 'Trades'
