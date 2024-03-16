from src.db.sqlite3 import Sqlite3
import json


def save_data(res):
    sqlite3 = Sqlite3()
    cur = sqlite3.cursor
    # 테이블 생성
    # cur.execute('create table stock_code(shcode, hname)')
    # JSON 데이터 파싱
    list_data = json.loads(res['t9945'][0])['t9945OutBlock']
    for each in list_data:
        cur.execute('insert or replace into stock_code(shcode, hname) values (?, ?)'
                    , (each['shcode'], each['hname']))
        # for k, v in request.future_option.items():

    print(list_data)
    sqlite3.conn.commit()
    sqlite3.conn.close()

    # cur.execute('select * from stock_code')
    # pass
