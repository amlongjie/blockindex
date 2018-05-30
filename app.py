# -*- coding: utf-8 -*-
import datetime
import json
import os
import time
import urllib
import urllib2
import uuid

import xlwt
from flask import Flask, request, render_template, send_file, make_response, jsonify
from flask_cors import CORS, cross_origin

import database

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
        crawler_data = crawler_option_id()
        return render_template('form.html', data=crawler_data)
    else:
        op_id = request.form.get("opId")
        first_n = request.form.get("first_n").encode("utf-8")
        second_n = request.form.get("second_n").encode("utf-8")
        name = "%s.xls" % uuid.uuid1()

        res_list = []
        for page_id in range(0, 10):
            res = do_crawler(op_id, page_id)
            if res:
                res_list.extend(res)
            else:
                break
        dir_ = os.path.split(os.path.realpath(__file__))[0] + '/excel/'
        full_file_name = dir_ + '%s' % name
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

        if not os.path.exists(dir_):
            os.makedirs(dir_)
        write_workbook.save(full_file_name)

        response = make_response(send_file(full_file_name))
        download_name = name
        if not first_n or not second_n:
            pass
        else:
            download_name = urllib.pathname2url("%s-%s-%s.xls" % (first_n, second_n, time.strftime("%Y-%m-%d")))
            # time.strftime("%Y-%m-%d")
        response.headers["Content-Disposition"] = "attachment; filename=%s; filename*=utf-8''%s" % (
            download_name, download_name)
        return response


@cross_origin(origin='*')
@app.route('/crawler_s', methods=['GET', 'POST'])
def crawler_s():
    op_id = request.args.get("opId")
    res_list = do_crawler_opt(op_id)
    return jsonify(result=json.dumps({'data': res_list}))


def crawler_option_id():
    url = "http://apiv3.yangkeduo.com/operations?pdduid=7068208265&is_back=1"
    req_header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    }
    req = urllib2.Request(url, None, req_header)
    response = urllib2.urlopen(req, timeout=10).read()
    op_list = json.loads(response)
    res = [{'name': u'请选择', 'opt_id': -1}]
    for op in op_list:
        name = op['opt_name']
        children = op['children']
        for child in children:
            key = "%s/%s" % (name, child['opt_name'])
            value = child['opt_id']
            res.append({'name': key, 'opt_id': value})
    return res


def do_crawler(op_id, page_id):
    # page_id = int(request.args['pageId'])
    url_format = "http://apiv3.yangkeduo.com/v4/operation/%s/groups?opt_type=3&offset=%s&size=100&sort_type=DEFAULT&flip=&pdduid=0"
    url = url_format % (op_id, 100 * page_id)
    req_header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    }
    req = urllib2.Request(url, None, req_header)
    response = urllib2.urlopen(req, timeout=10).read()
    data_list = json.loads(response)['goods_list']
    res_list = [{'id': x['goods_id'], 'n': x['goods_name'], 'c': x['cnt'], 'p': x['group']['price']} for x in data_list]
    return res_list


def do_crawler_opt(op_id):
    url_format = "http://apiv3.yangkeduo.com/v4/operation/%s/groups?opt_type=2&offset=0&size=100&sort_type=DEFAULT&flip=&pdduid=0"
    url = url_format % (op_id)
    req_header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    }
    req = urllib2.Request(url, None, req_header)
    response = urllib2.urlopen(req, timeout=10).read()
    opt_info = json.loads(response)['opt_infos']
    res = [{'id': op_id, 'n': u'全部'}]
    res.extend([{'id': x['id'], 'n': x['opt_name']} for x in opt_info])
    return res


@cross_origin(origin='*')
@app.route('/get_all', methods=['GET', 'POST'])
def do_get_all_data():
    db = database.Connection(host="127.0.0.1",
                             database='blockindex',
                             user='root',
                             password='123456')
    datas = db.query("SELECT * FROM otc_index order by id asc")
    res = {'code': 200}
    data = [{'buy': x['otc_buy'] - x['real_price'],
             'datetime': str(x['create_time']),
             'sell': x['otc_sell'] - x['real_price'],
             'cur': x['real_price'] - datas[0]['real_price'],
             'm_flow': x['minute_money_in'] - datas[0]['minute_money_in'],
             'h_flow': x['hour_money_in'] - datas[0]['hour_money_in'],
             'd_flow': x['day_money_in'] - datas[0]['day_money_in'],
             'w_flow': x['week_money_in'] - datas[0]['week_money_in']}
            for x in datas]
    res['data'] = data
    return jsonify(res)


@cross_origin(origin='*')
@app.route('/reset/email', methods=['GET', 'POST'])
def reset_email():
    if request.method == 'GET':
        return render_template("reset.html")
    else:
        next = request.form.get("next")
        db = database.Connection(host="127.0.0.1",
                                 database='blockindex',
                                 user='root',
                                 password='123456')
        affect = db.execute_rowcount("UPDATE flag set flag = 0, next=%s WHERE id = 1" % next)
        return jsonify({'code': 200, 'affect': affect})
