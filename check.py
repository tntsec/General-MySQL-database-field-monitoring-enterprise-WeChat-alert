import requests,redis
import mysql.connector
def post_weixin(data):

    url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=用自己的'
    body = {
        "msgtype": "news",
        "news": {
            "articles": [
                {
                    "title": "卡号监控机器人",
                    "description": data,
                    "url": "90apt.com",
                    "picurl": "https://www.zkteco.com/cn/uploads/image/20210301/3e1adaa2dce94812e658c5d42afc1525.png"
                }
            ]
        }
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=body)
    print(response.text)
    print(response.status_code)

def sqlread():
    mqdb = mysql.connector.connect(
        host="127.0.0.1",
        user="admin",
        passwd="password",
        database="mysqldata"
    )
    mqcursor = mqdb.cursor()
    getconfig_sql = "SELECT number,card,name FROM userinfo where ifnull(name, '') <> ''"
    mqcursor.execute(getconfig_sql)
    mqconfig = mqcursor.fetchall()
    global cardchange
    cardchange = ""
    readredis = redis.Redis(connection_pool=redis.ConnectionPool(host="127.0.0.1", port="6379", password="password",decode_responses=True))
    for i in mqconfig:
        if readredis.get(i[0]) == str(i[1]):
            None
        else:
            cardchange = cardchange + i[2]+readredis.get(i[0])+"变为"+str(i[1])+"\n"
            readredis.set(i[0], str(i[1]))
sqlread()
post_weixin(cardchange)
