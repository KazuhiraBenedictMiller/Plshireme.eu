from datetime import timedelta
from typing import Dict

from Config import Config
from loguru import logger
from quixstreams import Application


def InitOHLCCandle(Trade: Dict) -> Dict:
    """
    Initialize the state for aggregation when a new window starts, with the First Trade of the Window.
    It will prime the aggregation when the first record arrives in the window.

    Args:
        Trade (Dict): Data and Values from the Trade

    Returns:
        Dict containing the Initialization of the Candle with OHLC set as the Trade Price Value.
    """

    return {
        'productid': Trade['productid'],
        'timestamp': Trade['timestamp'],
        'open': Trade['price'],
        'high': Trade['price'],
        'low': Trade['price'],
        'close': Trade['price'],
    }


def UpdateOHLCCandle(ActualCandle: Dict, Trade: Dict) -> Dict:
    """
    Update the Previously Init and Running Forming Candle with new Data

    Args:
        ActualCandle (Dict): Init or Candle in Formation to be Updated
        Trade (Dict): Actual Incoming Trade Data

    Returns:
        Dict Containing Updated Candle.
    """

    return {
        'productid': Trade['productid'],
        #'timestamp': Trade['timestamp'],
        'open': ActualCandle['open'],
        'high': max(ActualCandle['high'], Trade['price']),
        'low': min(ActualCandle['low'], Trade['price']),
        'close': Trade['price'],
    }


def AggregateOHLC(
    kafka_input_topic: str,
    kafka_output_topic: str,
    kafka_broker_address: str,
    ohlc_tumblingwindow_secs: int,
) -> None:
    """
    Reads Raw Trades from the Kafka Input Topic (Trade Producer).
    Aggregates them by time in an OHLC Candle, which Session is the ohlc_tumblingwindow_secs.
    Pushes the Trades Aggregated in ohlc_tumblingwindow_secs seconds to the Kafka Output Topic.

    Args:
        kafka_input_topic (str): The name of the Kafka Input Topic
        kafka_output_topic (str): The name of the Kafka Output Topic
        kafka_broker_address (str): The address of the Kafka Broker (Containerized with RedPanda)
        ohlc_tumblingwindow_secs (int): The time period in seconds for Trades Aggregation

    Returns:
        None
    """

    app = Application(
        broker_address=kafka_broker_address,
        consumer_group=Config.TradeAggregatorConsumerGroup,
        # auto_create_reset='latest', #Forget about past Messages process from last one on
        auto_offset_reset='earliest',  # Process from the First Message Pushed to the Topic
    )

    # Defining the topic with JSON serialization where we'll save the Candles
    input_topic = app.topic(name=kafka_input_topic, value_serializer='json')
    output_topic = app.topic(name=kafka_output_topic, value_serializer='json')

    # Creating Streaming DataFrame and Connecting it to Input Topic to Apply Aggregation and Transformation to incoming Data
    sdf = app.dataframe(topic=input_topic)

    # Apply Transformations to Incoming Data with Tumbling Window
    sdf = (
        # Setting Up Tumbling Window Processing
        sdf.tumbling_window(duration_ms=timedelta(seconds=Config.WindowSecondsOHLC))
        # Actual Transformation to OHLC with Initializer and Reducer Functions
        .reduce(reducer=UpdateOHLCCandle, initializer=InitOHLCCandle)
        # Only Emit Final Values when Window is Closed
        .final()
    )

    # Changing Data Format of our Candles
    sdf['productid'] = sdf['value']['productid']
    sdf['timestamp'] = sdf['start']
    sdf['open'] = sdf['value']['open']
    sdf['high'] = sdf['value']['open']
    sdf['low'] = sdf['value']['open']
    sdf['close'] = sdf['value']['open']

    # Keeping only Columns we care about in our message before pushing it to Output Topic
    sdf = sdf[['productid', 'timestamp', 'open', 'high', 'low', 'close']]

    # Logging
    sdf = sdf.update(logger.info)

    # Pushing Candles to Topic
    sdf = sdf.to_topic(output_topic)

    # Running the App
    app.run(sdf)


if __name__ == '__main__':
    AggregateOHLC(
        kafka_input_topic=Config.KafkaInputTopic,
        kafka_output_topic=Config.KafkaOutputTopic,
        kafka_broker_address=Config.KafkaBrokerAddress,
        ohlc_tumblingwindow_secs=Config.WindowSecondsOHLC,
    )
