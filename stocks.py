import requests
import os

api_key = os.getenv("stock_api")


def get_stock_price(ticker_symbol, api):
    try:
        url = f"https://api.twelvedata.com/price?symbol={ticker_symbol}&apikey={api}"
        response = requests.get(url).json()
        price = response['price'][:-3]
        return price
    except:
        return ("Not Availible")


def get_stock_quote(ticker_symbol, api):
    try:
        url = f"https://api.twelvedata.com/quote?symbol={ticker_symbol}&apikey={api}"
        response = requests.get(url).json()
        return response
    except:
        return ("Not Availible")


# stock_price = get_stock_price(ticker, api_key)

# Append async execution


def show_stocks(companies=("DJI", "IXIC", "SPX", "RUB/USD", "RUB/EUR", "AAPL",
                           "MSFT", "TSLA", "NFLX", "GS")):
    """Format info to readble stock list"""
    result = ""
    for i in companies:
        try:
            stockdata = get_stock_quote(i, api_key)
            if stockdata == "Not Availible":
                print("Not Availible")
            exchange = stockdata['exchange']
            open_price = float(stockdata['open'])
            price_now = float(stockdata['close'])
            name = stockdata['name']
            previous_close = float(stockdata["previous_close"])
            price_precent = str(
                ((price_now - previous_close) / previous_close) *
                100)[0:5]  # Текущая - цена закрытия / цена закрытия
            if price_precent[0] == "-":
                result = result + "▼" + str(
                    i) + ": " + price_precent + "%" + " | "
            else:
                result = result + "▲" + str(
                    i) + ": " + price_precent + "%" + " | "
        except Exception as err:
            print("Данные не получены: ", str(err), i)
            continue
        #yield result
    return result


stockinfo = show_stocks()
