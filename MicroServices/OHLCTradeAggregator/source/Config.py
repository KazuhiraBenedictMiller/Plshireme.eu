import os

from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings

# Dinamically Crawl in search of a .env file
load_dotenv(find_dotenv())

# Or Declaratively
# load_dotenv('../.env')

# TradeProducerConsumerGroup = 'TradeProducer'
# ProductID = 'BTC/USD'
# KrakenWebSocketChannel = 'trade'
# KrakenWebSocketURL = 'wss://ws.kraken.com/v2'
# KafkaBrokerAddress = os.environ['DockerInternalKafkaBrokerAddress']
# KafkaInputTopic = 'Trades'


class Configurations(BaseSettings):
    TradeAggregatorConsumerGroup: str = 'TradeAggregator'
    KafkaBrokerAddress: str = os.environ['DockerInternalKafkaBrokerAddress']
    KafkaInputTopic: str = 'Trades'
    KafkaOutputTopic: str = 'Candles'
    WindowSecondsOHLC: int = os.environ['AggregationWindowSecondsOHLC']


Config = Configurations()
