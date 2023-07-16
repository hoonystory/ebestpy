from src.utils.log import logger
from src.utils.calendar import Calendar
from config import trcode
from src.api.login import Login
from src.api.transaction.txn import Transaction


def main():
    logger.debug('init main')

    # multiprocessing.freeze_support()
    calendar = Calendar()
    login = Login()
    # tr_code = TrCode()
    # mysql = MySql()

    logger.info('today: ' + calendar.get_today_date())
    logger.info('closest trade day: ' + calendar.get_closest_trade_day())

    # db login

    txn_list = []
    login.init()

    # 공휴일이 아닌 경우,
    # if calendar.is_holiday() is False:
        # 코드 정보 세팅: 휴장일인 경우, t3518(해외지수)만 작동하고, 해외지수는 코드리스트 업데이트 필요없음
    for tr_code in trcode.future_market_code_tr_list:
        txn_list.append(Transaction(tr_code))
        # 월요일(0)~ 금요일(4), 오후 16시 이후에는 주간데이터, (혹은 에러로 인해 야간에 실행해야하는 경우),
    # else:

    for txn in txn_list:
        print(txn.tr_code)
        print(txn.field_info)


if __name__ == '__main__':
    main()
