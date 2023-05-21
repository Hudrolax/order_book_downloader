from binance_api import download_order_book
from numpy import float32


def test_download_dept():
    """Test downloading and preprocessing order book"""
    depth, time = download_order_book('BTCUSDT')
    assert isinstance(depth, list)
    assert isinstance(depth[0], list)
    assert len(depth) == 20
    assert isinstance(depth[0][0], float)
    assert isinstance(depth[0][1], float)
    assert isinstance(time, int)
