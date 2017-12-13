# !/usr/bin/python

from bs4 import BeautifulSoup
import requests
import database

r = requests.get('https://coinmarketcap.com/')

html_doc = r.text

soup = BeautifulSoup(html_doc, 'html.parser')


def span_symbol(tag):
    return tag.name == 'span' and tag.has_attr('class') and 'currency-symbol' in tag['class']


def td_cap(tag):
    return tag.name == 'td' and tag.has_attr('class') and 'market-cap' in tag['class'] \
           and 'text-right' in tag['class'] and 'no-wrap' in tag['class']


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
cap = soup.find_all(td_cap)
total = 0
base = 1.43797450258e+11
print symbol
print cap
for i in range(0, len(cap)):
    symbol_ = symbol[i].text.strip().encode()
    cap_ = int(cap[i].text.strip().strip("$").replace(",", ""))
    if symbol_ in holder:
        total += cap_ * holder[symbol_]
db = database.Connection(host="127.0.0.1",
                         database='blockindex',
                         user='root',
                         password='123456')
index = int((total / base) * 1000)
if index > 0:
    affected = db.execute_rowcount("INSERT INTO bindex (idx) VALUES(%s)" % index)
