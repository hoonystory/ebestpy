from src.utils.log import log
from src.utils.calendar import calendar
from src.service.login import Login
from src.constant import future_option, stock
from src.service.request import request_api
from src.db.mongo import MongoDB
import pprint
import json
import asyncio


def main():
    # 로그인 객체 생성
    login = Login()
    if login.response.status_code != 200:
        return False

    # 날짜 정보를 저장하는 캘린더 객체 생성
    ins_calendar = calendar.Calendar()
    log.info('Today: %s', ins_calendar.get_today_date())
    log.info('Closest_Trade_Day: %s', ins_calendar.get_closest_trade_day())

    # DB 객체 생성
    # mongo_db = MongoDB()
    # log.info(mongo_db.client.list_database_names())

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
    main()
