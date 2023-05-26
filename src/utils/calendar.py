import datetime


class Calendar():
    def __init__(self):
        self.now = datetime.datetime.now()

    def get_today_date(self):
        """
        : 오늘 일자를 리턴
        :return: yyyymmdd
        """
        return self.now.strftime('%Y%m%d')

    def get_today_hour(self):
        """
        : 현재 시간을 리턴
        :return: hh
        """
        return int(self.now.strftime('%H'))

    def get_today_of_week(self):
        """
        : 오늘의 요일을 리턴
        :return: 0~ 6
        """
        return self.now.weekday()

    def get_today_month(self):
        """
        : 이번 달을 리턴
        :return: yyyymm
        """
        return self.now.strftime('%Y%m')

    def get_closest_trade_day(self):
        """
        : 공휴일 및 휴일 처리한 날짜를 리턴함
        : 토, 일요일 처리 제외. 공휴일, 야간 처리만 수행
        :return: yyyymmdd
        """
        if self.get_today_hour() in range(0, 9):
            return (self.now + datetime.timedelta(days=-1)).strftime('%Y%m%d')
        else:
            return self.get_today_date()

