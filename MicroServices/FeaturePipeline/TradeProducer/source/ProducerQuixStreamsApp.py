# Create an Application instance with Kafka configs
from typing import Dict, List

from Config import Config
from FetchTrades import KrakenWebSocket
from quixstreams import Application


def ProduceTrades(kafka_broker_address: str, kafka_input_topic: str) -> None:
    """
    Reads Trades from Kraken WebSocket API and Pushes them through the TradeProducer, saving them into a Kafka Topic.

    Args:
        kafka_broker_address (str): The address of the Kafka Broker (Containerized with RedPanda)
        kafka_input_topic (str): The name of the Kafka Input Topic

    Returns:
        None
    """

    # Defining the Application
    app = Application(
        broker_address=kafka_broker_address,
        consumer_group=Config.TradeProducerConsumerGroup,
    )

    # Defining the topic with JSON serialization where we'll save the Trades
    input_topic = app.topic(name=kafka_input_topic, value_serializer='json')

    # Fake Test Event
    # event = {"id": "1", "text": "Lorem ipsum dolor sit amet"}

    productid = Config.ProductID
    URL = Config.KrakenWebSocketURL
    channel = Config.KrakenWebSocketChannel

    # Establishing Kraken WebSocket Connection
    KrakenAPI = KrakenWebSocket(product_id=productid, URL=URL, channel=channel)
    # KrakenAPI.Subscibe() <--- Added to init Method of Class

    # Creating a Producer instance
    with app.get_producer() as producer:
        while True:
            # Getting Trades
            Trades: List[Dict] = KrakenAPI.FetchTrades()

            for T in Trades:
                # Serializing the event using the defined Topic
                message = input_topic.serialize(key=T['product_id'], value=T)

                # Producing a message into the Kafka topic
                producer.produce(
                    topic=input_topic.name, value=message.value, key=message.key
                )


if __name__ == '__main__':
    ProduceTrades(
        # External Port for Local Dev
        # kafka_broker_address = "localhost:19092",
        # Internal Port for Containerized Production on same Docker Network
        kafka_broker_address=Config.KafkaBrokerAddress,
        kafka_input_topic=Config.KafkaInputTopic,
    )
