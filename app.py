# -*- coding: utf-8 -*-
from flask import Flask, request
import database
import json
import datetime
import urllib2
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)


def encoder(obj):
    if isinstance(obj, datetime.datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(obj, datetime.date):
        return obj.strftime('%Y-%m-%d')
    else:
        raise TypeError('%r is not JSON serializable' % obj)


@app.route('/index')
@cross_origin(origin='*')
def q_index():
    db = database.Connection(host="127.0.0.1",
                             database='blockindex',
                             user='root',
                             password='123456')
    datas = db.query("SELECT createtime,idx FROM bindex")
    return json.dumps(datas, default=encoder)


@app.route('/crawler', methods=['GET', 'POST'])
@cross_origin(origin='*')
def crawler():
    op_id = request.args['opId']
    # page_id = int(request.args['pageId'])
    url_format = "http://apiv3.yangkeduo.com/v4/operation/%s/groups?opt_type=3&offset=0&size=100&sort_type=DEFAULT&flip=&pdduid=0"
    url = url_format % (op_id,)
    req_header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Connection': 'close',
        'Referer': None  # 注意如果依然不能抓取的话，这里可以设置抓取网站的host
    }
    req = urllib2.Request(url, None, req_header)
    response = urllib2.urlopen(req, timeout=10).read()
    data_list = json.loads(response)['goods_list']
    res_list = [{'id': x['goods_id'], 'n': x['goods_name'], 'c': x['cnt'], 'p': x['group']['price']} for x in data_list]
    return json.dumps({'data': res_list, 'code': '0'})
