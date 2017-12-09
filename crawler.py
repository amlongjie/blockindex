# !/usr/bin/python

from bs4 import BeautifulSoup
import requests
import database

r = requests.get('https://www.coingecko.com/en?sort_by=market_cap')

html_doc = r.text

soup = BeautifulSoup(html_doc, 'html.parser')


def span_symbol(tag):
    return tag.name == 'span' and tag.has_attr('class') and 'coin-content-symbol' in tag['class']


def span_cap(tag):
    return tag.name == 'span' and tag.has_attr('class') and 'currency-exchangable' in tag['class'] \
           and tag.has_attr('data-market-cap-btc')


holder = {
    "BTC": 0.51,
    "BCH": 0.07,
    "IOT": 0.07,
    "DASH": 0.07,
    "XMR": 0.07,
    "NEO": 0.07,
    "EOS": 0.07,
    "QTUM": 0.07
}
symbol = soup.find_all(span_symbol)
cap = soup.find_all(span_cap)
total = 0
base = 1.43797450258e+11
for i in range(0, len(cap)):
    symbol_ = symbol[i].text.strip().encode()
    cap_ = int(cap[i].text.strip().strip("$").replace(",", ""))
    if symbol_ in holder:
        print symbol_ + ":" + str(cap_)
        total += cap_ * holder[symbol_]
db = database.Connection(host="127.0.0.1",
                         database='blockindex',
                         user='root',
                         password='123456')

index = int((total / base) * 1000)

affected = db.execute_rowcount("INSERT INTO bindex (idx) VALUES(%s)" % index)
print affected
