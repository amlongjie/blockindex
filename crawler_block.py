# coding=utf-8
# !/usr/bin/python

from bs4 import BeautifulSoup
from crawler.crawler_api import do_crawler
import cjson
from decimal import Decimal

import database


def price_content(tag):
    return tag.name == 'li' and tag.has_attr('class') and 'price' in tag['class']


def crawler_otc(url):
    r = do_crawler(url)
    html_doc = r
    soup = BeautifulSoup(html_doc, 'html.parser')
    symbol = soup.find_all(price_content)
    lowest = symbol[0].text
    return int(100 * float(lowest.split("\n")[2].strip()))


def crawler_current(url):
    r = do_crawler(url)
    data = cjson.decode(r)['data']
    return Decimal(float(data['detail']['price']) * float(data['rate']) * 100).quantize(Decimal('0')), float(
        data['rate'])


def crawler_money_flow(url, usd_rate):
    r = do_crawler(url)
    data = cjson.decode(r)['data']
    return {
        '1w': int(((data['inflow_1w'] - data['outflow_1w']) * usd_rate) / 10000),
        '1d': int(((data['inflow_1d'] - data['outflow_1d']) * usd_rate) / 10000),
        '1h': int((data['inflow_1h'] - data['outflow_1h']) * usd_rate / 10000),
        '30m': int((data['inflow_30m'] - data['outflow_30m']) * usd_rate / 10000),
    }


otc_eos_buy_price = crawler_otc('https://otcbtc.com/sell_offers?currency=eos&fiat_currency=cny&payment_type=all')
otc_eos_sell_price = crawler_otc('https://otcbtc.com/buy_offers?currency=eos&fiat_currency=cny&payment_type=all')
cur_eos_price, cur_usd_rate = crawler_current('https://api.schail.com/v1/ticker/summary/detail?id=eos')
cur_money_flow_price = crawler_money_flow('https://block.cc/api/v1/coin/get?coin=eos', cur_usd_rate)

print otc_eos_buy_price, otc_eos_sell_price, cur_eos_price, cur_money_flow_price

db = database.Connection(host="127.0.0.1",
                         database='blockindex',
                         user='root',
                         password='root')
sql = "INSERT INTO `otc_index` (otc_buy, otc_sell, real_price, minute_money_in, hour_money_in, day_money_in, " \
      "week_money_in,token) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)" % (
          otc_eos_buy_price, otc_eos_sell_price, cur_eos_price, cur_money_flow_price['30m'], cur_money_flow_price['1h'],
          cur_money_flow_price['1d'], cur_money_flow_price['1w'], '"eos"')
print sql
affected = db.execute_rowcount(sql)
print affected
#
# affected = db.execute_rowcount("INSERT INTO bindex (idx) VALUES(%s)" % index)
