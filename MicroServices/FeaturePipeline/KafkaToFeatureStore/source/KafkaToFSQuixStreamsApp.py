import json

from Config import Config
from loguru import logger
from PushToFS import PushToFS
from quixstreams import Application


def KafkaToFS(
    kafka_topic: str,
    kafka_broker_address: str,
    feature_group_name: str,
    feature_group_version: int,
) -> None:
    """
    Reads OHLC Data from the Topic where the Aggregator Pushed Transformed Data and Pushes it to the Feature Store.
    Specifically it Pushes to the Feature Group in the Feature Store Identified by feature_group_name and feature_group_version.

    Args:
        kafka_topic (str): The name of the Kafka Topic, which happens to be the "kafka_output_topic" of the Trade Aggregator MicroService
        kafka_broker_address (str): The address of the Kafka Broker (Containerized with RedPanda)
        feature_group_name (str): Name of the Feature Group in the Feature Store to write to
        feature_group_version (int): Version of the Feature Group (Used for Data Versioning) to write to

    Returns:
        None
    """

    app = Application(
        broker_address=kafka_broker_address,
        consumer_group=Config.PushToFSConsumerGroup,
        # auto_create_reset='latest', #Forget about past Messages process from last one on
        auto_offset_reset='earliest',  # Process from the First Message Pushed to the Topic
        # auto_commit_enable=True  # AutoCommitting is useful but you have to store the Message Offset, Default=True
    )

    # Defining the Input Topic where Candles are saved
    # input_topic = app.topic(name=kafka_topic, value_serializer='json')

    # Defining Consumer and Starting Polling Loop
    with app.get_consumer() as consumer:
        # Subscribe to Topic
        consumer.subscribe(topics=[Config.KafkaTopic])

        # Polling
        while True:
            message = consumer.poll(0.1)

            if message is None:
                continue

            # breakpoint()

            elif message.error():
                # raise Exception(f'An Error with Kafka has occurred: {message.error()}')
                logger.error(f'An Error with Kafka has occurred: {message.error()}')
                continue

            else:
                # Extracting Values from Message
                # valueb = message.value()

                # Value is Binary Encoded, so you'll need to Decode it
                # valuestr = valueb.decode("utf-8")

                # Turning Value into Dict
                # value = json.loads(valuestr)

                # One-Liner
                # value = message.value()
                # candledata = json.loads(value.decode('utf-8'))
                candledata = json.loads(message.value().decode('utf-8'))

                # Pushing Value to the Feature Store in the Feature Group
                PushToFS(
                    feature_group_name=feature_group_name,
                    feature_group_version=feature_group_version,
                    data=candledata,
                )

                logger.info(
                    f'Pushed Data {candledata}\nto Feature Group {feature_group_name} Version {feature_group_version}'
                )

                # Store the offset of the processed message on the Consumer for the auto-commit mechanism.
                # It will send it to Kafka in the background.
                # Storing offset only after the message is processed enables at-least-once delivery guarantees.
                # Used to Define the Last Processed Message in case of Infrastructure Failure
                consumer.store_offsets(message=message)


if __name__ == '__main__':
    KafkaToFS(
        kafka_topic=Config.KafkaTopic,
        kafka_broker_address=Config.KafkaBrokerAddress,
        feature_group_name=Config.FeatureGroupName,
        feature_group_version=Config.FeatureGroupVersion,
    )
