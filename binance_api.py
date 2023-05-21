from binance.spot import Spot
import pandas as pd
import logging


logger = logging.getLogger(__name__)


def preprocessing_depth(depth:dict, num_bins:int = 10) -> list:
    """Function make for raw depth data from Binance order book

    Args:
        depth (dict): Raw depth data
        time (int): Timestamp in ms
        num_bins (int, optional): Num of bins in one dirrection. Defaults to 10.

    Returns:
        list: list with depth like [[timestamp, price, vol]]
    """
    bids = pd.DataFrame(depth['bids'], columns=['price', 'vol']).astype({'price': 'float32', 'vol': 'float32'})
    asks = pd.DataFrame(depth['asks'], columns=['price', 'vol']).astype({'price': 'float32', 'vol': 'float32'})

    bids['price_bins'] = pd.cut(bids['price'], bins=num_bins)
    bids_grouped = bids.groupby('price_bins')['vol'].sum().reset_index()
    bids_grouped['price_bins'] = bids_grouped['price_bins'].apply(lambda x: x.right)
    bids_grouped.columns = ['price', 'vol']

    asks['price_bins'] = pd.cut(asks['price'], bins=num_bins)
    asks_grouped = asks.groupby('price_bins')['vol'].sum().reset_index()
    asks_grouped['price_bins'] = asks_grouped['price_bins'].apply(lambda x: x.right)
    asks_grouped.columns = ['price', 'vol']

    result = pd.concat([bids_grouped, asks_grouped]).sort_values(by=['price'], ascending=False)
    
    return result.values.tolist()


def download_order_book(symbol: str) -> tuple[list[list], int]:
    """Function downloads order book from broker api

    Args:
        symbol (str): symbol

    Returns:
        list[list]: list of klines.
    """
    client = Spot()

    try:
        time = client.time()['serverTime']
        raw_depth = client.depth(symbol, limit=5000)
        depth_list = preprocessing_depth(depth=raw_depth)
    except Exception as ex:
        logger.error(f'symbol {symbol}')
        raise ex

    return depth_list, time
