# coding=utf-8
import smtplib
from email.mime.text import MIMEText
import database

mailto_list = ['398110112@qq.com']
mail_host = "smtp.163.com"  # 设置服务器
mail_user = "15101186970@163.com"  # 用户名
mail_pass = "woaitumen521"  # 口令
mail_postfix = "163.com"  # 发件箱的后缀


def send_mail(otc_eos_sell_price):
    repeat = query_flag_data()
    if repeat['flag'] == 1:
        return

    if otc_eos_sell_price / 100 < repeat['next']:
        return
    content = "EOS目前价格:%s" % str(otc_eos_sell_price)

    me = "hello" + "<" + mail_user + "@" + mail_postfix + ">"
    msg = MIMEText(content, _subtype='plain', _charset='utf-8')
    msg['Subject'] = "短线助手"
    msg['From'] = me
    msg['To'] = ";".join(mailto_list)
    try:
        server = smtplib.SMTP_SSL("smtp.163.com", "465")
        server.login(mail_user, mail_pass)
        server.sendmail(me, mailto_list, msg.as_string())
        server.close()
        do_not_send_again()
        return True
    except Exception, e:
        print str(e)
        return False


def query_flag_data():
    db = database.Connection(host="127.0.0.1",
                             database='blockindex',
                             user='root',
                             password='123456')
    data = db.get("SELECT * FROM flag WHERE id = 1")
    return data


def do_not_send_again():
    db = database.Connection(host="127.0.0.1",
                             database='blockindex',
                             user='root',
                             password='123456')
    db.execute_rowcount("UPDATE flag set flag = 1 WHERE id = 1")
