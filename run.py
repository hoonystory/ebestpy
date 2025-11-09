from src.utils.log import log
from src.utils.calendar import calendar
from src.service.login import Login
from src.constant import future_option, stock
# from src.service.request import request_api
from src.db.mongo import MongoDB
import pprint
import json
import asyncio
# import requests
import websockets
import json
import time


async def main():
    # 로그인 객체 생성
    login = Login()
    if login.response.status_code != 200:
        return False

    # 날짜 정보를 저장하는 캘린더 객체 생성
    ins_calendar = calendar.Calendar()
    log.info('Today: %s', ins_calendar.get_today_date())
    log.info('Closest_Trade_Day: %s', ins_calendar.get_closest_trade_day())

    # DB 객체 생성
    mongo_db = MongoDB()
    # log.info(mongo_db.client.list_database_names())

    # response = requests.post(
    #     'wss://openapi.ls-sec.co.kr:9443/websocket'
    #     , json={
    #         "body": {
    #             "tr_cd": "NWS",
    #             "tr_key": "NWS001"
    #         }
    #     }
    #     , headers={
    #         'token': login.access_token,
    #         "tr_type": "3"
    #     }
    # )

    info = {
        "header": {
            "token": login.access_token,
            "tr_type": "3"
        },
        "body": {
            "tr_cd": "NWS",
            "tr_key": "NWS001"
        }
    }

    # print(str(json.dumps(info)))
    print(login.access_token)
    await get_news(json.dumps(info), mongo_db)

    # print(response)

    # 코드 리스트 추가, Transaction 요청
    # for i in [
    #     'stock.market_data'
    #     # , 'stock.chart'
    #     # , 'future.market_data'
    # ]:
        # 비동기 요청
        # 갈과 값이 한번에 모여서 리턴 되기 때문에,
        # DB에 저장해야하는 작업이 있다면 처리 중에 저장하도록 인스턴스를 추가한다.
        # asyncio.run(request_api(get_list(i), login.access_token))
        # response = asyncio.run(request_api(get_list(i), login.access_token))
        # print(response)

    # 1. sqlite3 로 부터 종목코드 전체를 불러온다
    # 2. t8410 월 데이터를 모두 로드하여 db 에 저장한다.
    # 3. 데이터 분석 필터 실행
    #   - 종목별로 데이터를 로딩
    #   - 월 이동평균선 데이터를 세팅
    #   - 현재가가 100 월 이동평균선 위에 있는 종목들인 경우, 종목코드를 리턴


# async def news():
#     ws_app = await websockets.connect(
#         'wss://openapi.ls-sec.co.kr:9443/websocket',
#         ping_interval=None
#     )
#     # await websocket.send("ping")
#     while True:
#         response = await ws_app.recv()
#         print(response)
#         # time.sleep(1)


async def get_news(param, database):
    async def connect(param, database):
        # 웹 소켓에 접속을 합니다.
        async with websockets.connect("wss://openapi.ls-sec.co.kr:9443/websocket") as websocket:
            while True:
                await websocket.send(param)
                # 웹 소켓 서버로 부터 메시지가 오면 콘솔에 출력합니다.
                while True:
                    data = await websocket.recv()
                    json_data = json.loads(data)
                    if json_data['body'] == None:
                        continue
                    else:
                        database.insert('realtime', 'nws', json_data)
                        # print(json_data)
    try:
        await connect(param, database)
    except Exception as e:
        print(e)
        time.sleep(10)
        await get_news(param, database)


# FUTURE_SISE = 'FC0'

# 웹 소켓 관련 신경쓸 필요없음
# import websockets
# async def real_api(real_code, ticker):
#     while True:
        # 웹 소켓에 접속을 합니다.
        # async with websockets.connect(BASE_URL_WEBS) as websocket:
        #     str = reg_future_real(real_code, ticker)
        #
        #     # 웹 소켓 서버로 데이터를 전송합니다.
        #     await websocket.send(str);
        #     print('wait')
        #     time.sleep(2)
        #
        #     while True:
        #         # 웹 소켓 서버로 부터 메시지가 오면 콘솔에 출력합니다.
        #         data_s = await websocket.recv();
        #         data = json.loads(data_s)
        #         if data['body'] == None: # 시세가 바로 오지 않음 None이면 waiting
        #             time.sleep(1)
        #             continue
        #         if real_code == FUTURE_SISE:
        #             on_future_sise(data['body'])


def save_data(db_instance, res):
    if db_instance is not None:
        if db_instance.db_name == 'mongo':
            db = db_instance.client.ebest
            t8410 = db.t8410
            json_str = res[0]['t8410'][0]
            post_id = t8410.insert_one(json.loads(json_str)).inserted_id
            print(post_id)
        if db_instance.db_name == 'mysql':
            pass


def print_mongo_db_data(instance):
    db = instance.client.ebest
    t8410 = db.t8410
    pprint.pprint(t8410.find_one({'date': '20240119'}))


def get_list(type):
    result_dict = {}
    dict_list = {
        'stock.chart': stock.chart,
        'stock.market_data': stock.market_data,
        'future.chart': future_option.chart,
        'future.market_data': future_option.market_data
    }
    if type is not None:
        selected_dict = dict_list[type]
        for k, v in selected_dict.items():
            if k.startswith('t'):
                result_dict[k] = v
                result_dict[k]['pathname'] = selected_dict['pathname']
                result_dict[k]['tr_code'] = k

    return result_dict


if __name__ == '__main__':
    asyncio.run(main())
