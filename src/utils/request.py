from src.constant import request
from src.utils.log import log
import requests
import asyncio


async def request_api(tr_list, access_token):
    # for k, v in request.future_option.items():
    #     if k.startswith('t'):
    #         await asyncio.create_task(get_response(k, v, access_token))

    # func_list = [get_response('t9943', request.future_option['t9943'], access_token)
    #     , get_response('t8415', request.future_option['t8415'], access_token)]

    futures = [asyncio.ensure_future(get_response(tr_list[k], access_token))
               for k, v in tr_list.items() if k.startswith('t')]
    result = await asyncio.gather(*futures)

    # print(result)
    return result
    # log.info(result)
    # await asyncio.gather(func_list)


# async def request_api(tr_info, access_token):
#     await asyncio.create_task(get_response(tr_info, access_token))


async def get_response(tr_info, access_token):
    # result object
    result = {}
    # set header
    tr_code = tr_info['tr_code']
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
    param_key = tr_code + 'InBlock'
    request_param = {
        param_key: tr_info['inblock']
    }
    # generate key from parameter
    generated_key = ''
    for k, v in tr_info['inblock'].items():
        generated_key += str(v)
    log.info(generated_key.lower())

    # 현재 tr 요청에 필요한 종목 코드 로딩.
    #   선물/옵션인 경우, t9943, t9944 에 저장된 정보를 가져온다.
    #       'shcode'
    #   코드 리스트 사이즈만큼 for 문을 돌면서 request

    code_list = tr_info.get('code_list')
    if code_list is None:
        code_list = [1]

    for i in range(len(code_list)):
        # tr 초당 전송 건수 적용
        log.debug(request_param)

        response = requests.post(
            request.hostname + tr_info['pathname']
            , json=request_param
            , headers=header
        )
        await asyncio.sleep(1 / tr_info['limit'])
        # log.info(response.text)

        if result.get(tr_code) is None:
            result[tr_code] = []
        result[tr_code].append(response.text)

    result['generated_key'] = generated_key.lower()

    return result


def save_response(response):
    pass


def manage_request():
    pass


def connect_websocket():
    pass
