from src.constant import request
from src.utils.log import log
import requests
import asyncio


"""
- 

- 아래와 같이 요청 시,
    header 
    content-type:application/json
    tr_cd:t8415
    tr_cont:N
    Authorization:Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0b2tlbiIsImF1ZCI6IjIxYjQxYWEyLTgyM2YtNDk0MS04OGFiLWVlZmU5ZTAzNTVhNCIsIm5iZiI6MTY5Njc0NTE4OCwiZ3JhbnRfdHlwZSI6IkNsaWVudCIsImlzcyI6InVub2d3IiwiZXhwIjoxNjk2ODAyMzk5LCJpYXQiOjE2OTY3NDUxODgsImp0aSI6IlBTZlEzdHkwNkMxcHFNc0FDMUpCdVB3SWVPdFZlZm40b1ozbCJ9.hpqcgOE4lDKE5HZkZaL8IsODiGd8Uu3-jMqba-XehJRa2ZrpOHyGp7IglP8Qa9602DLNKlKagP3AW3z69gad
    tr_cont_key:0
    {
      "t8415InBlock": {
        "shcode": "101TC000",
        "ncnt": 0,
        "qrycnt": 500,
        "nday": "0",
        "sdate": "20230727",
        "stime": "084500",
        "edate": "20230727",
        "etime": "154500",
        "cts_date": "20230727",
        "cts_time": "",
        "comp_yn": "N"
      }
    }
    
- outBlock 
- cts_date, cts_time 값이 리턴된 경우,
- header tr_cont: Y 변경 후, 재요청 
    "t8415OutBlock": {
        "shcode": "101TC000",
        "jisiga": "322.00",
        "jihigh": "323.15",
        "jilow": "319.70",
        "jiclose": "319.75",
        "jivolume": 258976,
        "disiga": "319.90",
        "dihigh": "322.10",
        "dilow": "319.75",
        "diclose": "320.50",
        "highend": "345.30",
        "lowend": "294.20",
        "cts_date": "20230727",
        "cts_time": "112530",
        "s_time": "084500",
        "e_time": "154500",
        "dshmin": "10",
        "rec_count": 500
    },
"""


async def request_future_api(access_token):
    # for k, v in request.future_option.items():
    #     if k.startswith('t'):
    #         await asyncio.create_task(get_response(k, v, access_token))

    # func_list = [get_response('t9943', request.future_option['t9943'], access_token)
    #     , get_response('t8415', request.future_option['t8415'], access_token)]

    futures = [asyncio.ensure_future(get_response(k, request.future_option[k], access_token))
               for k, v in request.future_option.items() if k.startswith('t')]
    await asyncio.gather(*futures)
    # await asyncio.gather(func_list)


async def request_api(tr_code, tr_info, access_token):
    await asyncio.create_task(get_response(tr_code, tr_info, access_token))


async def get_response(tr_code, tr_info, access_token):
    # set header
    header = {
        'content-type': 'application/json',
        'tr_cd': tr_code,
        'Authorization': 'Bearer ' + access_token,
        'tr_cont': 'N',
        'tr_cont_key': '0'
    }
    # request.header['Authorization'] = 'Bearer ' + access_token
    # request.header['tr_cd'] = tr_code

    # tr_info['code_list'] =
    request_param = {tr_code + 'InBlock': tr_info['inblock']}

    # 현재 tr 요청에 필요한 종목 코드 로딩.
    #   선물/옵션인 경우, t9943, t9944 에 저장된 정보를 가져온다.
    #       'shcode'
    #   코드 리스트 사이즈만큼 for 문을 돌면서 request

    for i in range(len( tr_info['code_list'])):
        # tr 초당 전송 건수 적용
        # log.debug(request_param)
        response = requests.post(
            request.hostname + tr_info['pathname']
            , json=request_param
            , headers=header
        )
        await asyncio.sleep(1 / tr_info['limit'])
        # log response
        # log.info(response)
        log.info(response.text)


def save_response(response):
    pass


def manage_request():
    pass


def connect_websocket():
    pass
