# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, send_file, make_response
import database
import json
import datetime
import urllib2
import xlwt
import os
import uuid
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


@cross_origin(origin='*')
@app.route('/crawler', methods=['GET', 'POST'])
def crawler():
    if request.method == 'GET':
        return render_template('form.html')
    else:
        op_id = request.form.get("opId")
        res_list = do_crawler(op_id)
        return render_template("data.html", data=res_list, opId=op_id)


@cross_origin(origin='*')
@app.route('/export', methods=['GET'])
def export():
    op_id = request.args['opId']
    res_list = do_crawler(op_id)
    dir = os.path.split(os.path.realpath(__file__))[0] + '/excel/'
    file_name = dir + '%s.xls' % uuid.uuid1()
    write_workbook = xlwt.Workbook(encoding='utf-8')
    write_sheet = write_workbook.add_sheet('Sheet 1', cell_overwrite_ok=True)
    write_sheet.write(0, 0, "id")
    write_sheet.write(0, 1, "名称")
    write_sheet.write(0, 2, "价格")
    write_sheet.write(0, 3, "已团")
    for i in range(0, len(res_list)):
        write_sheet.write(i + 1, 0, res_list[i]['id'])
        write_sheet.write(i + 1, 1, res_list[i]['n'])
        write_sheet.write(i + 1, 2, (res_list[i]['p'] * 1.0 / 100))
        write_sheet.write(i + 1, 3, res_list[i]['c'])

    if not os.path.exists(dir):
        os.makedirs(dir)
    write_workbook.save(file_name)

    response = make_response(send_file(file_name))
    response.headers["Content-Disposition"] = "attachment; filename={};".format(file_name)
    return response


def do_crawler(op_id):
    # page_id = int(request.args['pageId'])
    url_format = "http://apiv3.yangkeduo.com/v4/operation/%s/groups?opt_type=3&offset=0&size=200&sort_type=DEFAULT&flip=&pdduid=0"
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
    return res_list
