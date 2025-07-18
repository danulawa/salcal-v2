import requests
from bs4 import BeautifulSoup

# Target URL
url = 'https://www.cbsl.gov.lk/en/rates-and-indicators/exchange-rates/daily-buy-and-sell-exchange-rates'

def fetch_rates():
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')
    rates = {}
    # The rates are usually in a table with currency names and Buy/Sell columns
    for row in soup.select('table tr'):
        cols = [c.get_text(strip=True) for c in row.find_all('td')]
        if len(cols) >= 3 and cols[0] in ('USD', 'AUD', 'EUR', 'GBP'):
            currency, buy, sell = cols[0], cols[1], cols[2]
            rates[currency] = float(sell)
    return rates

if __name__ == '__main__':
    rates = fetch_rates()
    # Print in final-first order
    for c in ['USD', 'AUD', 'EUR', 'GBP']:
        print(f"{c}: {rates.get(c, 'N/A')}")
