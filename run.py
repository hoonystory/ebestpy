from src.utils.log import log
from src.utils.calendar import Calendar
from src.api.login import Login
from src.common import template
import requests


def main():
    calendar = Calendar()
    login = Login()

    log.debug('init main')
    log.info('today: ' + calendar.get_today_date())
    log.info('closest trade day: ' + calendar.get_closest_trade_day())

    # db login

    login.init()

    code_list = []
    chart_list = []
    for i in template.code_list:
        code_list.append(template.code_list[i])
    for i in template.chart_list:
        chart_list.append(template.chart_list[i])

    # set header
    template.header['Authorization'] = 'Bearer ' + login.access_token

    for k, v in template.code_list.items():
        # set parameter and send post request
        # print(k, v)
        get_response(k, v, template.header)

    # for i in chart_list:
    # set parameter and send post request
    # get_response(i)


def get_response(tr_code, data, header):
    template.header['tr_cd'] = tr_code
    json_data = {tr_code + 'InBlock': data['InBlock']}
    response = requests.post(data['url'], json=json_data, headers=header)
    print(response)
    print(response.text)


if __name__ == '__main__':
    main()

