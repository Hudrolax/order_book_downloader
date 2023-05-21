from binance_api import download_order_book
import logging
from time import sleep
import os
import requests
from datetime import datetime

logging.basicConfig(format='%(asctime)s: %(message)s',
                    datefmt='%d/%m/%y %H:%M:%S', level=logging.INFO)

SERVER_HOST = os.environ.get('SERVER_HOST', 'api')
SERVER_PORT = os.environ.get('SERVER_PORT', 8000)

url = f'http://{SERVER_HOST}:{SERVER_PORT}/depth'

logger = logging.getLogger(__name__)


def add_depth(symbol: str, time:int, depth: list) -> requests.Response:
    """Adding klines to DB

    Args:
        symbol (str): symbol
        depth (list): grouped depth list

    Returns:
        requests.Response: response from DB API
    """
    payload = dict(
        symbol=symbol,
        time=time,
        depth=depth,
    )

    return requests.post(url, json=payload)


def main_loop():
    while True:
        try:
            # symbols = get_symbols()
            symbols = ['BTCUSDT']
            for symbol in symbols:
                start_time = datetime.now()
                logger.info(f'Download depth for {symbol}')

                preprocessed_depth, time = download_order_book(symbol)
                add_depth(symbol, time, preprocessed_depth)
                elapsed_time = (datetime.now() - start_time).total_seconds()
                sleep_time = 60 - elapsed_time
                sleep(sleep_time if sleep_time > 0 else 0)

        except OSError as ex:
            logger.error(ex)

        logger.info('All order books are downloaded.')


if __name__ == '__main__':
    main_loop()
