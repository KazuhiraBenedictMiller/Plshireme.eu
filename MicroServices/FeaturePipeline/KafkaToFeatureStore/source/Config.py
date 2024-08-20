import os

from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings

# Dinamically Crawl in search of a .env file
load_dotenv(find_dotenv())


class Configurations(BaseSettings):
    PushToFSConsumerGroup: str = 'PushToFS'
    KafkaBrokerAddress: str = os.environ['DockerInternalKafkaBrokerAddress']
    KafkaTopic: str = 'Candles'
    HopsworksAPIKey: str = os.environ['HopsworksAPIKey']
    HopsworksProjectName: str = os.environ['HopsworksProjectName']
    FeatureGroupName: str = (os.environ['FeatureGroupName'],)
    FeatureGroupVersion: int = (os.environ['FeatureGroupVersion'],)


Config = Configurations()
