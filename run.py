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

    code_list = []
    future_code_list = []
    future_option_dict = request.future_option
    # future_code_tr_list = ['t9943', 't9944']
    market_data_dict = request.future_option['market_data']

    # 코드 리스트 먼저 가져오기
    for i in market_data_dict:
        if i in ['t9943', 't9944']:
            set_pathname_and_append_list(market_data_dict, i, future_code_list)

    asyncio.run(request_api_from_list(future_code_list, login.access_token))

    # 코드 리스트, 경로 추가하여 요청
    for i in future_option_dict:
        for k in future_option_dict[i]:
            if k.startswith('t'):
                set_pathname_and_append_list(future_option_dict[i], k, code_list)

    # for k, v in request.future_option.items():
        # set parameter and send post request
        # only for transaction code (tr_code)
        # 비동기 작업 세트 등록
        # if k.startswith('t'):
        #     asyncio.run(request_api(k, v, login.access_token))

    asyncio.run(request_api_from_list(code_list, login.access_token))


def set_pathname_and_append_list(root_dict, index, code_list):
    root_dict[index]['pathname'] = root_dict['pathname']
    code_list.append(root_dict[index])


if __name__ == '__main__':
    main()

