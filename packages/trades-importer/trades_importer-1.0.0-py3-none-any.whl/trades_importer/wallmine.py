import logging
import re
from typing import Optional, List

from bs4 import BeautifulSoup
from requests import Session

logger = logging.getLogger()


def get_authenticated_session(email: str, password: str) -> Session:
    http_session = Session()

    url = "https://wallmine.com/users/sign-in"
    r = http_session.get(url)

    soup = BeautifulSoup(r.text, "html.parser")
    authenticity_token = soup.find_all("meta", {"name": "csrf-token"})[0]["content"]

    url = "https://wallmine.com/users/sign-in"
    form_data = {
        "user[email]": email,
        "user[password]": password,
        "authenticity_token": authenticity_token,
        "user[remember_me]": "1"
    }
    http_session.post(url, form_data)

    return http_session


def get_portfolio_ticker_id(http_session: Session, portfolio_id: str, ticker: str) -> Optional[str]:
    url = f"https://wallmine.com/portfolios/{portfolio_id}/transactions#{ticker}"
    r = http_session.get(url)

    soup = BeautifulSoup(r.text, "html.parser")
    tags: List = soup.find_all("a", {"data-symbol": ticker.upper(), "title": f"Add a {ticker.upper()} transaction"})

    if len(tags) > 0:
        portfolio_ticker_id_search = re.search(r"/portfolios/\d+/item/(\d+)/transaction", tags[0].get("data-url"), re.IGNORECASE)
        if portfolio_ticker_id_search:
            return portfolio_ticker_id_search.group(1)

    return None


def create_portfolio_ticker_id(http_session: Session, portfolio_id: str, exchange: str, ticker: str):
    url = f"https://wallmine.com/portfolios/{portfolio_id}"
    r = http_session.get(url)

    soup = BeautifulSoup(r.text, "html.parser")
    authenticity_token = soup.find_all("meta", {"name": "csrf-token"})[0]["content"]

    url = f"https://wallmine.com/portfolios/{portfolio_id}/item"
    form_data = {
        "utf8": "✓",
        "portfolio_item[symbol]": f"{exchange.upper()}:{ticker.upper()}",
        "authenticity_token": authenticity_token
    }
    http_session.post(url, form_data)


def add_transaction(http_session: Session, portfolio_id: str, portfolio_ticker_id: str,
                    transaction_type: str, date: str, shares: str, price: float, note: str):
    url = f"https://wallmine.com/portfolios/{portfolio_id}/transactions"
    r = http_session.get(url)

    soup = BeautifulSoup(r.text, "html.parser")
    authenticity_token = soup.find_all("meta", {"name": "csrf-token"})[0]["content"]

    url = f"https://wallmine.com/portfolios/{portfolio_id}/item/{portfolio_ticker_id}/transaction"
    form_data = {
        "authenticity_token": authenticity_token,
        "portfolio_transaction[transaction_type]": transaction_type,
        "portfolio_transaction[date]": date,
        "portfolio_transaction[shares]": f"{shares}",
        "portfolio_transaction[price]": f"{price}",
        "portfolio_transaction[commission]": "0.00",
        "portfolio_transaction[notes]": f"{note}",
        "utf8": "✓",
        "_method": "",
        "button": ""
    }
    http_session.post(url, form_data)
