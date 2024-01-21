from src.utils.log import log
from src.utils.calendar import Calendar
from src.api.login import Login
from src.constant import request
from src.request import future_option
from src.request import stock
from src.request import real_time
from src.utils.request import request_api
from src.utils.db.mongo import MongoDB
import pprint
import json
import asyncio


def main():
    login = Login()
    if login.response.status_code != 200:
        return False

    calendar = Calendar()
    log.info('Today: %s', calendar.get_today_date())
    log.info('Closest_Trade_Day: %s', calendar.get_closest_trade_day())

    mongo_db = MongoDB()
    log.info(mongo_db.client.list_database_names())

    # 코드 리스트 추가, Transaction 요청
    for i in [
        'stock.market_data'
        , 'stock.chart'
        # , 'future.market_data'
    ]:
        response = asyncio.run(request_api(get_list(i), login.access_token))
        print(response)
        if response[0].get('t8410') is not None:
            # insert_into_mongo_db(response, mongo_db)
            print_mongo_db_data(mongo_db)


def print_mongo_db_data(instance):
    db = instance.client.ebest
    t8410 = db.t8410
    pprint.pprint(t8410.find_one({'date': '20240119'}))


def insert_into_mongo_db(res, instance):
    db = instance.client.ebest
    t8410 = db.t8410
    json_str = res[0]['t8410'][0]
    post_id = t8410.insert_one(json.loads(json_str)).inserted_id
    print(post_id)


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
