from src.utils.log import log
from src.utils.calendar import Calendar
from src.api.login import Login
from src.constant import request
from src.utils.request import request_future_api
import asyncio


def main():
    calendar = Calendar()
    login = Login()
    log.info('today: ' + calendar.get_today_date())
    log.info('closest trade day: ' + calendar.get_closest_trade_day())

    code_list = []
    for i in request.future_option:
        code_list.append(request.future_option[i])

    # for k, v in request.future_option.items():
        # set parameter and send post request
        # only for transaction code (tr_code)
        # 비동기 작업 세트 등록
        # if k.startswith('t'):
        #     asyncio.run(request_api(k, v, login.access_token))

    asyncio.run(request_future_api(login.access_token))


if __name__ == '__main__':
    main()

