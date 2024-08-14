import json
from typing import Dict, List

from loguru import logger
from websocket import create_connection


class KrakenWebSocket:
    def __init__(self, product_id: str, URL: str, channel: str):
        self.ProductID = product_id
        self.URL = URL
        self.Channel = channel

        self._ws = create_connection(self.URL)

        self.Subscibe()

    def Subscibe(self):
        """
        Dummy Function that Subscribes to the Kraken API WebSocket
        """

        SubscribingMessage = {
            'method': 'subscribe',
            'params': {
                'channel': self.Channel,
                'symbol': [self.ProductID],
                'snapshot': False,
            },
        }

        try:
            self._ws.send(json.dumps(SubscribingMessage))

        except Exception as e:
            # Handle exception
            logger.error(
                f'An error occurred whilist trying to Subscribe to the KrakenAPI WebSocket: {e}'
            )

        else:
            logger.success('Successfully Subscribed to the KrakenAPI WebSocket.')
            # Then, Dumping the First 2 Useless Messages. Connection ID and Connection Status
            _ = self._ws.recv()
            _ = self._ws.recv()

    def FetchTrades(self) -> List[Dict]:
        Message = self._ws.recv()

        logger.info(f'Message Received: {Message}')

        # Data is returned in the str format like as follows:
        #'{"channel":"trade","type":"update","data":[{"symbol":"BTC/USD","side":"sell","price":59121.8,"qty":0.00022946,"ord_type":"market","trade_id":72823289,"timestamp":"2024-08-12T19:38:30.575191Z"}]}''

        # Now, checking if the there is any data in the message or if it contains the heartbeat (no Data Update)
        if 'heartbeat' in Message:
            # Rerutning an Empty List
            return []

        else:
            Message = json.loads(Message)
            Trades = []

            for trade in Message['data']:
                # Extract Trade info, there could be more than one message at time, building smaller and smarter dict.
                Trades.append(
                    {
                        'product_id': self.ProductID,
                        'price': trade['price'],
                        'volume': trade['qty'],
                        'timestamp': trade['timestamp'],
                    }
                )

            # pp(Message)

        # Interactive command to actually debug code from a snapshot
        # breakpoint()

        return Trades
