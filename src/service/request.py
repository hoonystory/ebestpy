from src.constant import request
from src.utils.log import log
import requests
import asyncio

import src.service.save.stock_code as t9945


async def request_api(tr_list, access_token):
    futures = [asyncio.ensure_future(process_response(tr_list[k], access_token))
               for k, v in tr_list.items() if k.startswith('t')]
    await asyncio.gather(*futures)
    # result = await asyncio.gather(*futures)
    # return result


async def process_response(tr_info, access_token):
    code_list = tr_info.get('code_list')
    in_block = tr_info['inblock']
    tr_code = tr_info['tr_code']

    # 종목 리스트 정보가 없는 경우,
    if code_list is None:
        code_list = [in_block.get('shcode') or in_block.get('gubun') or '']

    # api 호출
    for i in range(len(code_list)):
        key = 'shcode'\
            if in_block.get('shcode') is not None \
            else 'gubun'
        in_block[key] = code_list[i]
        response = get_response(tr_info, access_token)
        print(response)

        # tr 초당 전송 건수 적용
        await asyncio.sleep(1 / tr_info['limit'])

        # 임시 데이터 저장 처리 프로세스
        if tr_code == 't8410':
            pass
        if tr_code == 't9945':
            t9945.save_data(response)

    # return response


def get_response(tr_info, access_token):
    result = {}
    tr_code = tr_info['tr_code']
    tr_inblock = tr_info['inblock']
    header = {
        'content-type': 'application/json',
        'tr_cd': tr_code,
        'Authorization': 'Bearer ' + access_token,
        'tr_cont': 'N',
        'tr_cont_key': '0'
    }
    response = requests.post(
        request.hostname + tr_info['pathname']
        , json={
            tr_code + 'InBlock': tr_inblock
        }
        , headers=header
    )
    if result.get(tr_code) is None:
        result[tr_code] = []

    # generate key for mongo_db from parameter
    generated_key = ''
    for k, v in tr_inblock.items():
        generated_key += str(v)

    result[tr_code].append(response.text)
    result['generated_key'] = generated_key.lower()

    log.info(generated_key.lower())
    log.debug({tr_code + 'InBlock': tr_inblock})

    return result


def save_response(response):
    pass


def manage_request():
    pass


def connect_websocket():
    pass
