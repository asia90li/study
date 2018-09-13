import urllib.request
import os
import datetime
import schedule
import time
import pymysql
def url_open(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36')
    response = urllib.request.urlopen(url)
    html = response.read()
    #print(html)
    return html


def get_page(url,mesage):
    html = url_open(url).decode('utf-8')
    # print(html)
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(now)
    mesage.append(now)
    yesterday = (datetime.datetime.now() + datetime.timedelta(days=-1))
    yesterday1=yesterday.strftime('%Y-%m-%d')
    print(yesterday1)
    mesage.append(yesterday1)
    yesterday2 = yesterday.strftime('%d')
    print(yesterday2)
    a = html.find('<em>'+yesterday2)
    b = html.find('</li>',a)
    # print(html[a:b])
    return (html[a:b])

#获取天气、温度、风向、风级
def find_date(date,mesage):
    tianqi = ["alt=","<p>","&nbsp"]
    for i in tianqi:
        #获取天气
        if i == "alt=":
            aa = date.find(i)
            print(date[aa:aa + 10])
            mesage.append(date[aa+5:aa + 10])
        #获取温度
        elif i == "<p>":
            aa = date.find(i)
            print(date[aa:aa + 10])
            mesage.append(date[aa+3:aa + 9])
        #获取风向、级数
        else :
            aa = date.find(i)
            print(date[aa-4:aa + 10])
            mesage.append(date[aa-3:aa + 1])
            mesage.append(date[aa + 12:aa + 16])

def save(mesage):
    db = pymysql.connect("localhost", "root", "123456", "tianqi",use_unicode=True, charset="utf8")
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    data = cursor.fetchone()
    print("Database version : %s " % data)

    sql = "INSERT INTO dbtianqi(join_date, tianqi_date, tianqi, wendu, fengxiang, fengji)  VALUES ('%s', '%s', '%s', '%s', '%s', '%s' )" % (mesage[0], mesage[1], mesage[2], mesage[3], mesage[4],mesage[5])
    print(str(mesage[0]), str(mesage[1]), mesage[2], mesage[3], mesage[4],mesage[5])
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 执行sql语句
        db.commit()
        print("OK")
    except  :
        # 发生错误时回滚
        db.rollback()
        print(EOFError)
        print("NG")
        raise
    # 关闭数据库连接
    db.close()
    print(mesage)



def download_mm():
    mesage = []
    url ="http://tianqi.moji.com/"
    date = get_page(url,mesage)
    # print("**************")
    # print(date)
    find_date(date,mesage)
    # print(mesage)

    save(mesage)
def job():
    # print("I'm working...")
    download_mm()


schedule.every(1).minutes.do(job)
# schedule.every().hour.do(job)
# schedule.every().day.at("8:50").do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)


if __name__ == '__main__':
    download_mm()