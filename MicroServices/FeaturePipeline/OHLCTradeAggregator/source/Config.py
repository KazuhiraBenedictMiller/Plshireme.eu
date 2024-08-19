import os

from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings

# Dinamically Crawl in search of a .env file
load_dotenv(find_dotenv())


class Configurations(BaseSettings):
    TradeAggregatorConsumerGroup: str = 'TradeAggregator'
    KafkaBrokerAddress: str = os.environ['DockerInternalKafkaBrokerAddress']
    KafkaInputTopic: str = 'Trades'
    KafkaOutputTopic: str = 'Candles'
    WindowSecondsOHLC: int = os.environ['AggregationWindowSecondsOHLC']


Config = Configurations()
