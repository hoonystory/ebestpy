from src.utils.log import log
from src.utils.calendar import Calendar
from src.api.login import Login
from src.constant import request
from src.utils.request import request_api_from_list
from src.utils.request import request_api
import asyncio


def main():
    login = Login()
    if login.response.status_code != 200:
        return False

    calendar = Calendar()

    log.info('today: ' + calendar.get_today_date())
    log.info('closest trade day: ' + calendar.get_closest_trade_day())

    f_tr_dict = {}
    f_cd_dict = {}
    future_chart_dict = request.future_option['chart']
    # future_code_tr_list = ['t9943', 't9944']
    future_code_dict = request.future_option['market_data']

    # 코드 리스트 먼저 가져오기
    for i in future_code_dict:
        if i in ['t9943', 't9944']:
            set_pathname_and_append_list(future_code_dict, i, f_cd_dict)

    # await 확인
    asyncio.run(request_api_from_list(f_cd_dict, login.access_token))

    # 코드 리스트, 경로 추가하여 요청
    for i in future_chart_dict:
        if i.startswith('t8415'):
            set_pathname_and_append_list(future_chart_dict, i, f_tr_dict)

    # for k, v in request.future_option.items():
        # set parameter and send post request
        # only for transaction code (tr_code)
        # 비동기 작업 세트 등록
        # if k.startswith('t'):
        #     asyncio.run(request_api(k, v, login.access_token))

    asyncio.run(request_api_from_list(f_tr_dict, login.access_token))


def set_pathname_and_append_list(root_dict, key, result_dict):
    result_dict[key] = root_dict[key]
    result_dict[key]['pathname'] = root_dict['pathname']
    result_dict[key]['tr_code'] = key


if __name__ == '__main__':
    main()

