from typing import Dict, List, Optional

from pydantic import BaseModel, ValidationError
from pytickersymbols import PyTickerSymbols

DEFAULT_INDICES = ["DOW JONES", "S&P 500", "NASDAQ 100"]


class Stock(BaseModel):
    name: str
    symbol: str
    indices: List[str]


def _parse_stock(stock: dict) -> Optional[Stock]:
    try:
        return Stock(
            name=stock["name"],
            symbol=stock["symbol"],
            indices=stock["indices"],
        )
    except ValidationError:
        return None


def get_stocks(indices: List[str] = DEFAULT_INDICES) -> List[Stock]:
    stock_data = PyTickerSymbols()
    if indices:
        # get stocks for given indices
        all_stocks = []
        for index in indices:
            stocks = stock_data.get_stocks_by_index(index)
            all_stocks.extend(stocks)
    else:
        # get stocks for all indices
        all_stocks = stock_data.get_all_stocks()

    stocks = [_parse_stock(stock) for stock in all_stocks]
    return list(filter(None, stocks))


def get_stocks_by_symbol(indices: List[str] = DEFAULT_INDICES) -> Dict[str, Stock]:
    stocks = get_stocks(indices)
    return {stock.symbol: stock for stock in stocks}
