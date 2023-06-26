from xaquery import XAQueryResultHandler
import pandas as pd
import time
import xacom
import eBestLogin
import dbconn
import datetime
import xasys
import logging

db_name = 'ebestdb'
# db_name = 'ebest_test'


def parseInfield(trCode):
    """
    :param trCode:
    :return:
    """
    return xacom.parseInfield(trCode)


def parseOutfield(trCode):
    """
    :param trCode:
    :return:
    """
    return xacom.parseOutfield(trCode)


def apiLogin(log):
    # ----------------------------------------------------------------------------
    # Login
    # ----------------------------------------------------------------------------
    # pid = xasys.return_pid()
    log.info('Start on eBestAPI Login')
    # print('---[p' + str(pid) + ' Info] Start on eBest Login---')
    try:
        login = eBestLogin.Login.get_instance()
        login.initLogin(log)
    except Exception as e:
        log.error('error Occurred when logging eBestAPI: ', str(e))
    # login 객체 리턴하여 핸들러로 사용할 수 있도록 함
    return login


def dbLogin(log):
    # ----------------------------------------------------------------------------
    # DB Connect
    # ----------------------------------------------------------------------------
    # pid = xasys.return_pid()
    log.info('Start on Database Login')
    # print('---[p' + str(pid) + ' Info] Start on Database Login---')
    try:
        dbConnect = dbconn.DBConnect()
        db = dbConnect.login(db_name, log)
        # print(db_name)
    except Exception as e:
        log.error('error Occurred when logging database: ', str(e))

    # db 리턴하여 핸들러로 사용할 수 있도록 함
    return db


def t1485(tday):
    trCode = 't1485'
    log = logger(trCode)
    login = apiLogin(log)
    engine = dbLogin(log)
    receiver = XAQueryResultHandler.get_instance()

    tableOne = trCode + 'outblock1'
    gubunList = ['1', '2']
    upCodeList = ['001', '301', '501', '101', '515', '404', '516', '517']

    # 당일 추가된 data count
    result_len = 0

    start_time = currentTime()

    # 장전 -> 장후 순서로 데이터 조회
    for gubun in gubunList:
        for upcode in upCodeList:
            InBlock = parseInfield(trCode)
            OutBlock = parseOutfield(trCode)
            # 각 회차에 필요한 inBlock 값을 infield에 대입
            InBlockValue = [upcode, gubun]
            receiver.query(trCode, InBlock, OutBlock, InBlockValue, log)

            # 최종 결과값을 출력
            result = receiver.finalResult[1]
            resultCol = OutBlock[1]
            appenData(result, upcode, 0)
            appendCol(resultCol, 'upcode', 0)

            appenDate(result, tday)
            appendCol(resultCol, 'date', 0)

            saveData(result, resultCol, tableOne, engine, log)

            result_len += len(result)

            receiver.reset()
            XAQueryResultHandler.query_state = 0

            xasys.time_sleep(3.1)

    endTime(trCode, engine, start_time, result_len, log)

    login.logoutServer(log)


def t1511(tday):
    trCode = 't1511'
    log = logger(trCode)
    login = apiLogin(log)
    engine = dbLogin(log)
    receiver = XAQueryResultHandler.get_instance()

    tableOne = trCode + 'outblock'

    result_len = 0
    start_time = currentTime()

    upCodeList = ['001', '101', '501', '301']

    for upcode in upCodeList:
        InBlockValue = [upcode]
        InBlock = parseInfield(trCode)
        OutBlock = parseOutfield(trCode)
        receiver.query(trCode, InBlock, OutBlock, InBlockValue, log)

        result = receiver.finalResult[0]
        resultCol = OutBlock[0]
        appenData(result, upcode, 0)
        appendCol(resultCol, 'upcode', 0)

        appenDate(result, tday)
        appendCol(resultCol, 'date', 0)

        saveData(result, resultCol, tableOne, engine, log)

        result_len += len(result)

        receiver.reset()
        XAQueryResultHandler.query_state = 0
        xasys.time_sleep(3.1)

    endTime(trCode, engine, start_time, result_len, log)
    login.logoutServer(log)


def t1603(tday):
    trCode = 't1603'
    log = logger(trCode)
    login = apiLogin(log)
    engine = dbLogin(log)
    receiver = XAQueryResultHandler.get_instance()

    tableOne = trCode + 'outblock1'

    # 코스피, 코스닥은 업종코드에 따라 좌우되므로, market은 1로 고정
    market = '1'
    gubun1List = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C']
    gubun2 = '0'
    cnt = '800'
    upCodeList = ['001', '301', '501', '101', '515', '404', '516', '517']

    result_len = 0
    start_time = currentTime()

    for gubun1 in gubun1List:
        for upcode in upCodeList:
            InBlock = parseInfield(trCode)
            OutBlock = parseOutfield(trCode)
            InBlockValue = [market, gubun1, gubun2, cnt, upcode]
            receiver.query(trCode, InBlock, OutBlock, InBlockValue, log)

            # gubun1 값을 tjjcode 컬럼에 넣어주어야함.. (불러온값이 null이라서)
            # 가져온 result 값으로 제일 먼저 tjjcode 값을 2번째 인덱스 (1) 에 넣어준다
            result = receiver.finalResult[1]
            resultCol = OutBlock[1]

            updateData(result, gubun1, 1)      # 투자자코드 삽입

            appenData(result, upcode, 0)       # 업종코드 추가
            appendCol(resultCol, 'upcode', 0)

            appenDate(result, tday)  # 날짜 추가
            appendCol(resultCol, 'date', 0)

            saveData(result, resultCol, tableOne, engine, log)

            result_len += len(result)

            receiver.reset()
            XAQueryResultHandler.query_state = 0
            xasys.time_sleep(3.1)

    # 선물, 콜옵션, 풋옵션, ELW, ETF는 업종코드에 관계없으므로 업종코드 001 고정
    marketList = ['3', '4', '5', '6', '7']
    upcode = '001'

    for market in marketList:
        for gubun1 in gubun1List:
            InBlock = parseInfield(trCode)
            OutBlock = parseOutfield(trCode)
            InBlockValue = [market, gubun1, gubun2, cnt, upcode]
            receiver.query(trCode, InBlock, OutBlock, InBlockValue, log)

            # gubun1 값을 tjjcode 컬럼에 넣어주어야함.. (불러온값이 null이라서)
            result = receiver.finalResult[1]
            resultCol = OutBlock[1]

            updateData(result, gubun1, 1)  # 투자자코드 삽입

            appenData(result, upcode, 0)  # 업종코드 추가
            appendCol(resultCol, 'upcode', 0)

            appenDate(result, tday)  # 날짜 추가
            appendCol(resultCol, 'date', 0)
            # 컬럼을 맞추기 위해 업종코드 컬럼을 추가하되, 값은 넣지 않는다

            saveData(result, resultCol, tableOne, engine, log)

            result_len += len(result)

            receiver.reset()
            XAQueryResultHandler.query_state = 0
            xasys.time_sleep(3.1)

    endTime(trCode, engine, start_time, result_len, log)

    login.logoutServer(log)


def t1662(tday):
    trCode = 't1662'
    log = logger(trCode)
    login = apiLogin(log)
    engine = dbLogin(log)
    receiver = XAQueryResultHandler.get_instance()

    tableOne = trCode + 'outblock'

    result_len = 0
    start_time = currentTime()

    gubunList = ['0', '1']
    gubun1List = ['0', '1']
    gubun3 = '0'

    for gubun in gubunList:
        for gubun1 in gubun1List:
            InBlock = parseInfield(trCode)
            OutBlock = parseOutfield(trCode)
            InBlockValue = [gubun, gubun1, gubun3]
            receiver.query(trCode, InBlock, OutBlock, InBlockValue, log)

            result = receiver.finalResult[0]
            resultCol = OutBlock[0]

            appenDate(result, tday)
            appendCol(resultCol, 'date', 0)

            appenData(result, gubun, 0)
            appendCol(resultCol, 'gubun', 0)

            saveData(result, resultCol, tableOne, engine, log)
            result_len += len(result)

            receiver.reset()
            XAQueryResultHandler.query_state = 0
            xasys.time_sleep(3.1)

    endTime(trCode, engine, start_time, result_len, log)
    login.logoutServer(log)


# infield 에 들어갈 변수에 따라,
# 변수 1개이면, for문 1개 함수
# 변수 2개이면, for문 2개 함수,...
# tr 값을 넣었을 때 분기처리하여 변수 개수에 따라 각 함수에 들어갈 수 있도록 처리
# Date 필요한 경우, append 하도록 처리


def t1921(shcode):
    trCode = 't1921'
    log = logger(trCode)
    login = apiLogin(log)
    engine = dbLogin(log)
    receiver = XAQueryResultHandler.get_instance()

    tableOne = trCode + 'outblock1'

    result_len = 0
    start_time = currentTime()

    shcodeList = []
    shcodeList = shcodeList + shcode
    # 1, 2가 있으나, 1과 2가 동일하여 하나로만 요청
    gubunList = ['1']
    date = ''

    for shcode in shcodeList:
        for gubun in gubunList:
            cycle = 0
            continue_Yn = True

            while continue_Yn is True:
                cycle = cycle + 1

                # 만약, 두번째 조회로 넘어왔는데, cts_time 값이 존재한다면,
                if cycle != 1 and date == '':
                    continue_Yn = False
                    # 연속조회 request를 해제해야함
                    receiver.request = False

                    # print('---[' + trCode + ' Info] pid: ' + str(login.pid), end='')
                    # print(', ' + shcode + ' Continuous Request Ended')
                    log.info(shcode + ' continuous request Ended')
                    break
                else:
                    # print('---[' + trCode + ' Info] pid: ' + str(login.pid), end='')
                    # print(', Requesting ' + str(cycle) + ' cycle...')
                    log.info('requesting ' + str(cycle) + ' cycle')
                    InBlock = parseInfield(trCode)
                    OutBlock = parseOutfield(trCode)
                    InBlockValue = [shcode, gubun, date]

                    # 1회 이후에도 조회가 필요하면, 연속조회 request를 설정해야함
                    if cycle != 1:
                        receiver.request = True

                        # 연속조회와 관련된 값을 append
                        InBlock.append('date')
                        InBlockValue.append(date)

                receiver.query(trCode, InBlock, OutBlock, InBlockValue, log)

                # 결과값 OutBlock1의 첫번째 row만 가져온다
                # 2차원 리스트가 필요하므로, 리스트 대괄호로 감싸준다
                if len(receiver.finalResult[1]) != 0:
                    result = [receiver.finalResult[1][0]]
                else:
                    result = []
                resultCol = OutBlock[1]

                saveData(result, resultCol, tableOne, engine, log)

                result_len += len(result)

                receiver.reset()
                XAQueryResultHandler.query_state = 0

                xasys.time_sleep(3.1)

                # 쿼리 결과로부터 cts_date, cts_time을 불러옴
                # 무한루프 방지 처리 해줘야함
                # if sdate == edate:
                #     date = ''
                # else:
                date = receiver.date

    endTime(trCode, engine, start_time, result_len, log)
    login.logoutServer(log)


def t1926(shcode, tday):
    trCode = 't1926'
    log = logger(trCode)
    login = apiLogin(log)
    engine = dbLogin(log)
    receiver = XAQueryResultHandler.get_instance()

    tableOne = trCode + 'outblock'
    result_len = 0
    start_time = currentTime()

    shcodeList = []
    shcodeList = shcodeList + shcode

    for shcode in shcodeList:
        cycle = 0
        continue_Yn = True

        while continue_Yn is True:
            cycle = cycle + 1

            # 만약, 두번째 조회로 넘어왔는데, cts_time 값이 존재한다면,
            if cycle != 1 and date == '':
                continue_Yn = False
                # 연속조회 request를 해제해야함
                receiver.request = False

                # print('---[' + trCode + ' Info] pid: ' + str(login.pid), end='')
                # print(', ' + shcode + ' Continuous Request Ended')
                log.info(shcode + ' continuous request Ended')
                break
            else:
                # print('---[' + trCode + ' Info] pid: ' + str(login.pid), end='')
                # print(', Requesting ' + str(cycle) + ' cycle...')
                log.info('requesting ' + str(cycle) + ' cycle')

                InBlock = parseInfield(trCode)
                OutBlock = parseOutfield(trCode)
                InBlockValue = [shcode]

                # 1회 이후에도 조회가 필요하면, 연속조회 request를 설정해야함
                if cycle != 1:
                    receiver.request = True

                    # 연속조회와 관련된 값을 append
                    InBlock.append('date')
                    InBlockValue.append(date)

            receiver.query(trCode, InBlock, OutBlock, InBlockValue, log)

            result = receiver.finalResult[0]
            resultCol = OutBlock[0]

            appenDate(result, tday)
            appendCol(resultCol, 'date', 0)

            appenData(result, shcode, 0)
            appendCol(resultCol, 'shcode', 0)

            saveData(result, resultCol, tableOne, engine, log)

            result_len += len(result)

            receiver.reset()
            XAQueryResultHandler.query_state = 0

            xasys.time_sleep(3.1)

            date = receiver.date
            """
            # 왜 무한루프 도는지 확인
            """

    endTime(trCode, engine, start_time, result_len, log)
    login.logoutServer(log)


def t1927(shcode, sdate, edate):
    trCode = 't1927'
    log = logger(trCode)
    login = apiLogin(log)
    engine = dbLogin(log)
    receiver = XAQueryResultHandler.get_instance()

    tableOne = trCode + 'outblock1'

    result_len = 0
    start_time = currentTime()

    shcodeList = []
    shcodeList = shcodeList + shcode
    date = ''

    for shcode in shcodeList:
        cycle = 0
        continue_Yn = True

        while continue_Yn is True:
            cycle = cycle + 1

            # 만약, 두번째 조회로 넘어왔는데, cts_time 값이 존재한다면,
            if cycle != 1 and date == '':
                continue_Yn = False
                # 연속조회 request를 해제해야함
                receiver.request = False

                # print('---[' + trCode + ' Info] pid: ' + str(login.pid), end='')
                # print(', ' + shcode + ' Continuous Request Ended')
                log.info(shcode + ' continuous request Ended')
                break
            else:
                # print('---[' + trCode + ' Info] pid: ' + str(login.pid), end='')
                # print(', Requesting ' + str(cycle) + ' cycle...')
                log.info('requesting ' + str(cycle) + ' cycle')

                InBlock = parseInfield(trCode)
                OutBlock = parseOutfield(trCode)
                InBlockValue = [shcode, date, sdate, edate]

                # 1회 이후에도 조회가 필요하면, 연속조회 request를 설정해야함
                if cycle != 1:
                    receiver.request = True

                    # 연속조회와 관련된 값을 append
                    InBlock.append('date')
                    InBlockValue.append(date)

            receiver.query(trCode, InBlock, OutBlock, InBlockValue, log)

            # 공매도 일일 추이가 없는 경우를 처리
            if len(receiver.finalResult[1]) != 0:
                result = [ receiver.finalResult[1][0] ]
            else:
                result = []
            resultCol = OutBlock[1]

            appenData(result, shcode, 1)
            appendCol(resultCol, 'shcode', 1)

            saveData(result, resultCol, tableOne, engine, log)

            result_len += len(result)

            receiver.reset()
            XAQueryResultHandler.query_state = 0

            # receiver로 query_state를 제어할 수 있는지 테스트

            xasys.time_sleep(3.1)

            # 쿼리 결과로부터 cts_date, cts_time을 불러옴
            if sdate == edate:
                date = ''
            else:
                # sdate, edate가 같으면, 패스하도록 수정
                date = receiver.date

    endTime(trCode, engine, start_time, result_len, log)
    login.logoutServer(log)


def t2201(focode, tday):
    trCode = 't2201'

    log = logger(trCode)
    login = apiLogin(log)
    engine = dbLogin(log)
    receiver = XAQueryResultHandler.get_instance()

    tableOne = trCode + 'outblock1'

    result_len = 0
    start_time = currentTime()

    focodeList = []
    focodeList = focodeList + focode
    cvolume = ''
    stime = ''
    etime = ''
    cts_time = ''

    for focode in focodeList:
        cycle = 0
        continue_Yn = True

        while continue_Yn is True:
            cycle = cycle + 1

            # 만약, 두번째 조회로 넘어왔는데, cts_time 값이 존재한다면,
            if cycle != 1 and cts_time == '':
                continue_Yn = False
                # 연속조회 request를 해제해야함
                receiver.request = False

                # print('---[' + trCode + ' Info] pid: ' + str(login.pid), end='')
                # print(', ' + focode + ' Continuous Request Ended')
                log.info(focode + ' continuous request Ended')
                break
            else:
                # print('---[' + trCode + ' Info] pid: ' + str(login.pid), end='')
                # print(', Requesting ' + str(cycle) + ' cycle...')
                log.info('requesting ' + str(cycle) + ' cycle')

                InBlock = parseInfield(trCode)
                OutBlock = parseOutfield(trCode)
                InBlockValue = [focode, cvolume, stime, etime, cts_time]

                # 1회 이후에도 조회가 필요하면, 연속조회 request를 설정해야함
                if cycle != 1:
                    receiver.request = True

                    # 연속조회와 관련된 값을 append
                    InBlock.append('cts_time')
                    InBlockValue.append(cts_time)

            receiver.query(trCode, InBlock, OutBlock, InBlockValue, log)

            result = receiver.finalResult[1]
            resultCol = OutBlock[1]

            appenDate(result, tday)
            appendCol(resultCol, 'date', 0)

            appenData(result, focode, 0)
            appendCol(resultCol, 'focode', 0)

            saveData(result, resultCol, tableOne, engine, log)

            result_len += len(result)

            receiver.reset()
            XAQueryResultHandler.query_state = 0

            xasys.time_sleep(0.55)

            # 쿼리 결과로부터 cts_date, cts_time을 불러옴
            if cts_time != receiver.cts_time:
                cts_time = receiver.cts_time
            else:
                cts_time = ''

    endTime(trCode, engine, start_time, result_len, log)
    login.logoutServer(log)


def t2203(shcode):
    trCode = 't2203'

    log = logger(trCode)
    login = apiLogin(log)
    engine = dbLogin(log)
    receiver = XAQueryResultHandler.get_instance()

    tableOne = trCode + 'outblock1'

    shcodeList = []
    shcodeList = shcodeList + shcode
    futcheck = '0'
    cnt = '500'

    result_len = 0
    start_time = currentTime()

    date = ''
    cts_code = ''
    lastdate = ''

    for shcode in shcodeList:
        cycle = 0
        continue_Yn = True

        while continue_Yn is True:
            cycle = cycle + 1

            # 만약, 두번째 조회로 넘어왔는데, cts_time 값이 존재한다면,
            if cycle != 1 and date == '':
                continue_Yn = False
                # 연속조회 request를 해제해야함
                receiver.request = False

                # print('---[' + trCode + ' Info] pid: ' + str(login.pid), end='')
                # print(', ' + shcode + ' Continuous Request Ended')
                log.info(shcode + ' continuous request Ended')
                break
            else:
                # print('---[' + trCode + ' Info] pid: ' + str(login.pid), end='')
                # print(', Requesting ' + str(cycle) + ' cycle...')
                log.info('requesting ' + str(cycle) + ' cycle')
                InBlock = parseInfield(trCode)
                OutBlock = parseOutfield(trCode)
                InBlockValue = [shcode, futcheck, date, cts_code, lastdate, cnt]

                # 1회 이후에도 조회가 필요하면, 연속조회 request를 설정해야함
                if cycle != 1:
                    receiver.request = True

                    # 연속조회와 관련된 값을 append
                    InBlock.append('date')
                    InBlock.append('cts_code')
                    InBlock.append('lastdate')

                    InBlockValue.append(date)
                    InBlockValue.append(cts_code)
                    InBlockValue.append(lastdate)

            receiver.query(trCode, InBlock, OutBlock, InBlockValue, log)

            result = receiver.finalResult[1]
            resultCol = OutBlock[1]

            appenData(result, shcode, 0)
            appendCol(resultCol, 'shcode', 0)

            saveData(result, resultCol, tableOne, engine, log)

            result_len += len(result)

            receiver.reset()
            XAQueryResultHandler.query_state = 0

            xasys.time_sleep(3.1)

            # 쿼리 결과로부터 cts_date, cts_time을 불러옴
            date = receiver.date
            cts_code = receiver.cts_code
            lastdate = receiver.lastdate

    endTime(trCode, engine, start_time, result_len, log)
    login.logoutServer(log)


def t2301(yyyymm):
    trCode = 't2301'

    log = logger(trCode)
    login = apiLogin(log)
    engine = dbLogin(log)
    receiver = XAQueryResultHandler.get_instance()

    # 디비에 저장할 테이블 여러개일 경우, List로 정의해줌
    tableList = [trCode+'outblock', trCode+'outblock1', trCode+'outblock2']

    result_len = 0
    start_time = currentTime()

    yyyymm = yyyymm
    gubunList = ['M', 'G']

    for gubun in gubunList:
        InBlock = parseInfield(trCode)
        OutBlock = parseOutfield(trCode)
        InBlockValue = [yyyymm, gubun]
        receiver.query(trCode, InBlock, OutBlock, InBlockValue, log)

        result = receiver.finalResult
        resultCol = OutBlock

        # 구분값을 append 해준다
        for item in result:
            appenData(item, gubun, 0)
        for col in resultCol:
            appendCol(col, 'gubun', 0)

        saveDataList2(result, resultCol, tableList, engine, log)

        result_len += len(result)

        receiver.reset()
        XAQueryResultHandler.query_state = 0
        xasys.time_sleep(3.1)

    endTime(trCode, engine, start_time, result_len, log)
    login.logoutServer(log)


def t2405(focode):
    trCode = 't2405'

    log = logger(trCode)
    login = apiLogin(log)
    engine = dbLogin(log)
    receiver = XAQueryResultHandler.get_instance()

    tableOne = trCode + 'outblock1'

    focodeList = []
    focodeList = focodeList + focode
    bgubun = '0'
    nmin = ''
    etime = ''
    hgubun = '0'
    cnt = '500'

    result_len = 0
    start_time = currentTime()

    cts_time = ''
    for focode in focodeList:
        cycle = 0
        continue_Yn = True

        while continue_Yn is True:
            cycle = cycle + 1

            # 만약, 두번째 조회로 넘어왔는데, cts_time 값이 존재한다면,
            if cycle != 1 and cts_time == '':
                continue_Yn = False
                # 연속조회 request를 해제해야함
                receiver.request = False

                # print('---[' + trCode + ' Info] pid: ' + str(login.pid), end='')
                # print(', ' + focode + ' Continuous Request Ended')
                log.info(focode + ' continuous request Ended')
                break
            else:
                # print('---[' + trCode + ' Info] pid: ' + str(login.pid), end='')
                # print(', Requesting ' + str(cycle) + ' cycle...')
                log.info('requesting ' + str(cycle) + ' cycle')

                InBlock = parseInfield(trCode)
                OutBlock = parseOutfield(trCode)
                InBlockValue = [focode, bgubun, nmin, etime, hgubun, cnt]

                # 1회 이후에도 조회가 필요하면, 연속조회 request를 설정해야함
                if cycle != 1:
                    receiver.request = True

                    # 연속조회와 관련된 값을 append
                    InBlock.append('cts_time')
                    InBlockValue.append(cts_time)

            receiver.query(trCode, InBlock, OutBlock, InBlockValue, log)

            result = receiver.finalResult[1]
            resultCol = OutBlock[1]

            appenData(result, focode, 0)
            appendCol(resultCol, 'focode', 0)

            saveData(result, resultCol, tableOne, engine, log)

            result_len += len(result)

            receiver.reset()
            XAQueryResultHandler.query_state = 0

            # receiver로 query_state를 제어할 수 있는지 테스트
            xasys.time_sleep(3.1)

            # 쿼리 결과로부터 cts_date, cts_time을 불러옴
            if cts_time != receiver.cts_time:
                cts_time = receiver.cts_time
            else:
                cts_time = ''

    endTime(trCode, engine, start_time, result_len, log)
    login.logoutServer(log)


def t2804(focode, tday):
    trCode = 't2804'

    log = logger(trCode)
    login = apiLogin(log)
    engine = dbLogin(log)
    receiver = XAQueryResultHandler.get_instance()

    tableOne = trCode + 'outblock1'

    result_len = 0
    start_time = currentTime()

    focodeList = []
    focodeList = focodeList + focode
    cvolume = ''
    stime = ''
    etime = ''
    cts_time = ''

    for focode in focodeList:
        cycle = 0
        continue_Yn = True

        while continue_Yn is True:
            cycle = cycle + 1

            # 만약, 두번째 조회로 넘어왔는데, cts_time 값이 존재한다면,
            if cycle != 1 and cts_time == '':
                continue_Yn = False
                # 연속조회 request를 해제해야함
                receiver.request = False

                # print('---[' + trCode + ' Info] pid: ' + str(login.pid), end='')
                # print(', ' + focode + ' Continuous Request Ended')
                log.info(focode + ' continuous request Ended')
                break
            else:
                # print('---[' + trCode + ' Info] pid: ' + str(login.pid), end='')
                # print(', Requesting ' + str(cycle) + ' cycle...')
                log.info('requesting ' + str(cycle) + ' cycle')

                InBlock = parseInfield(trCode)
                OutBlock = parseOutfield(trCode)
                InBlockValue = [focode, cvolume, stime, etime, cts_time]

                # 1회 이후에도 조회가 필요하면, 연속조회 request를 설정해야함
                if cycle != 1:
                    receiver.request = True

                    # 연속조회와 관련된 값을 append
                    InBlock.append('cts_time')
                    InBlockValue.append(cts_time)

            receiver.query(trCode, InBlock, OutBlock, InBlockValue, log)

            result = receiver.finalResult[1]
            resultCol = OutBlock[1]

            appenDate(result, tday)
            appendCol(resultCol, 'date', 0)

            appenData(result, focode, 0)
            appendCol(resultCol, 'focode', 0)

            saveData(result, resultCol, tableOne, engine, log)

            result_len += len(result)

            receiver.reset()
            XAQueryResultHandler.query_state = 0

            xasys.time_sleep(0.15)

            # 쿼리 결과로부터 cts_date, cts_time을 불러옴
            if cts_time != receiver.cts_time:
                cts_time = receiver.cts_time
            else:
                cts_time = ''

    endTime(trCode, engine, start_time, result_len, log)
    login.logoutServer(log)


def t2805(shcode):
    trCode = 't2805'

    log = logger(trCode)
    login = apiLogin(log)
    engine = dbLogin(log)
    receiver = XAQueryResultHandler.get_instance()

    tableOne = trCode + 'outblock1'

    shcodeList = []
    shcodeList = shcodeList + shcode
    futcheck = '0'
    # 임의로 1로 설정함, 추후 변경 필요
    cnt = '500'

    result_len = 0
    start_time = currentTime()

    date = ''
    cts_code = ''
    lastdate = ''

    for shcode in shcodeList:
        cycle = 0
        continue_Yn = True

        while continue_Yn is True:
            cycle = cycle + 1

            # 만약, 두번째 조회로 넘어왔는데, cts_time 값이 존재한다면,
            if cycle != 1 and date == '':
                continue_Yn = False
                # 연속조회 request를 해제해야함
                receiver.request = False

                # print('---[' + trCode + ' Info] pid: ' + str(login.pid), end='')
                # print(', ' + shcode + ' Continuous Request Ended')
                log.info(shcode + ' continuous request Ended')
                break
            else:
                # print('---[' + trCode + ' Info] pid: ' + str(login.pid), end='')
                # print(', Requesting ' + str(cycle) + ' cycle...')
                log.info('requesting ' + str(cycle) + ' cycle')

                InBlock = parseInfield(trCode)
                OutBlock = parseOutfield(trCode)
                InBlockValue = [shcode, futcheck, date, cts_code, lastdate, cnt]

                # 1회 이후에도 조회가 필요하면, 연속조회 request를 설정해야함
                if cycle != 1:
                    receiver.request = True

                    # 연속조회와 관련된 값을 append
                    InBlock.append('date')
                    InBlock.append('cts_code')
                    InBlock.append('lastdate')

                    InBlockValue.append(date)
                    InBlockValue.append(cts_code)
                    InBlockValue.append(lastdate)

            receiver.query(trCode, InBlock, OutBlock, InBlockValue, log)

            result = receiver.finalResult[1]
            resultCol = OutBlock[1]

            appenData(result, shcode, 0)
            appendCol(resultCol, 'shcode', 0)

            saveData(result, resultCol, tableOne, engine, log)

            result_len += len(result)

            receiver.reset()
            XAQueryResultHandler.query_state = 0

            xasys.time_sleep(3.1)

            # 쿼리 결과로부터 cts_date, cts_time을 불러옴
            date = receiver.date
            cts_code = receiver.cts_code
            lastdate = receiver.lastdate

    endTime(trCode, engine, start_time, result_len, log)
    login.logoutServer(log)


def t2813(tday):
    trCode = 't2813'

    log = logger(trCode)
    login = apiLogin(log)
    engine = dbLogin(log)
    receiver = XAQueryResultHandler.get_instance()

    tableOne = trCode + 'outblock1'

    gubun1List = ['1', '2']     # 수량, 금액 구분하는 컬럼을 추가한다
    gubun2 = '0'
    cts_idx = ''
    cnt = '500'
    gubun3 = 'C'    # 직전대비로 저장하여, 누적은 코드로 구현

    result_len = 0
    start_time = currentTime()

    cts_time = ''
    # outBlock1은 연속데이터를 모두 저장하고
    # outBlock은 1개만 저장하면 된다.
    # 한번만 저장하기 위해 isSaved 변수 추가
    isSaved = False

    for gubun1 in gubun1List:
        cycle = 0
        continue_Yn = True

        while continue_Yn is True:
            cycle = cycle + 1

            # 만약, 두번째 조회로 넘어왔는데, cts_time 값이 존재한다면,
            if cycle != 1 and cts_time == '':
                continue_Yn = False
                # 연속조회 request를 해제해야함
                receiver.request = False

                # result2 >> 전광판에서 첫번째 블록을 가져온 것
                # 첫번째 컬럼의 값을 금일로 업데이트 해줌
                if isSaved is False:
                    result2[0][0] = tday
                    resultCol = parseOutfield(trCode)[0]

                    # 첫번째 컬럼이 cts_time으로 되어있어서, date로 바꾸어줌
                    updateCol(resultCol, 'date', 0)
                    saveData(result2, resultCol, 't2813outblock1', engine, log)

                    result_len += len(result2)

                    isSaved = True

                # print('---[' + trCode + ' Info] pid: ' + str(login.pid), end='')
                # print(', Continuous Request Ended')
                log.info(' continuous request Ended')
                break
            else:
                # print('---[' + trCode + ' Info] pid: ' + str(login.pid), end='')
                # print(', Requesting ' + str(cycle) + ' cycle...')
                log.info('requesting ' + str(cycle) + ' cycle')

                InBlock = parseInfield(trCode)
                OutBlock = parseOutfield(trCode)
                InBlockValue = [gubun1, gubun2, cts_time, cts_idx, cnt, gubun3]

                # 1회 이후에도 조회가 필요하면, 연속조회 request를 설정해야함
                if cycle != 1:
                    receiver.request = True

                    # 연속조회와 관련된 값을 append
                    InBlock.append('cts_time')
                    InBlockValue.append(cts_time)

            receiver.query(trCode, InBlock, OutBlock, InBlockValue, log)

            result = receiver.finalResult[1]
            resultCol = OutBlock[1]

            appenDate(result, tday)
            appendCol(resultCol, 'date', 0)

            appenData(result, gubun1, 0)
            appendCol(resultCol, 'gubun1', 0)

            saveData(result, resultCol, tableOne, engine, log)

            result_len += len(result)

            # 첫번째 outblock을 저장하기 위한 임시 리스트
            result2 = receiver.finalResult[0]

            receiver.reset()
            XAQueryResultHandler.query_state = 0

            xasys.time_sleep(3.1)

            # 쿼리 결과로부터 cts_date, cts_time을 불러옴
            if cts_time != receiver.cts_time:
                cts_time = receiver.cts_time
            else:
                cts_time = ''

    endTime(trCode, engine, start_time, result_len, log)
    login.logoutServer(log)


def t2814(From, To):
    trCode = 't2814'

    log = logger(trCode)
    login = apiLogin(log)
    engine = dbLogin(log)
    receiver = XAQueryResultHandler.get_instance()

    tableOne = trCode + 'outblock1'
    InBlock = parseInfield(trCode)
    OutBlock = parseOutfield(trCode)
    start_time = currentTime()

    gubun1 = '1'    # 수치로 저장하여 누적은 코드로 구현
    gubun2 = '1'    # 일로 저장하여 주, 월은 코드로 구현
    from_date = From
    to_date = To
    result_len = 0

    InBlockValue = [gubun1, gubun2, from_date, to_date]
    receiver.query(trCode, InBlock, OutBlock, InBlockValue, log)

    result = receiver.finalResult
    resultCol = OutBlock[1]

    saveData(result, resultCol, tableOne, engine, log)

    result_len += len(result)

    receiver.reset()
    XAQueryResultHandler.query_state = 0
    xasys.time_sleep(3.1)

    endTime(trCode, engine, start_time, result_len, log)
    login.logoutServer(log)


def t2832(focode, tday):
    trCode = 't2832'

    log = logger(trCode)
    login = apiLogin(log)
    engine = dbLogin(log)
    receiver = XAQueryResultHandler.get_instance()

    tableOne = trCode + 'outblock1'

    result_len = 0
    start_time = currentTime()

    focodeList = []
    focodeList = focodeList + focode
    cvolume = ''
    stime = ''
    etime = ''

    cts_time = ''
    for focode in focodeList:
        cycle = 0
        continue_Yn = True

        while continue_Yn is True:
            cycle = cycle + 1

            # 만약, 두번째 조회로 넘어왔는데, cts_time 값이 존재한다면,
            if cycle != 1 and cts_time == '':
                continue_Yn = False
                # 연속조회 request를 해제해야함
                receiver.request = False

                # print('---[' + trCode + ' Info] pid: ' + str(login.pid), end='')
                # print(', ' + focode + ' Continuous Request Ended')
                log.info(focode + ' continuous request Ended')
                break
            else:
                # print('---[' + trCode + ' Info] pid: ' + str(login.pid), end='')
                # print(', Requesting ' + str(cycle) + ' cycle...')
                log.info('requesting ' + str(cycle) + ' cycle')

                InBlock = parseInfield(trCode)
                OutBlock = parseOutfield(trCode)
                InBlockValue = [focode, cvolume, stime, etime]

                # 1회 이후에도 조회가 필요하면, 연속조회 request를 설정해야함
                if cycle != 1:
                    receiver.request = True

                    # 연속조회와 관련된 값을 append
                    InBlock.append('cts_time')
                    InBlockValue.append(cts_time)

            receiver.query(trCode, InBlock, OutBlock, InBlockValue, log)

            result = receiver.finalResult[1]
            resultCol = OutBlock[1]

            appenDate(result, tday)
            appendCol(resultCol, 'date', 0)

            appenData(result, focode, 0)
            appendCol(resultCol, 'focode', 0)

            saveData(result, resultCol, tableOne, engine, log)

            result_len += len(result)

            receiver.reset()
            XAQueryResultHandler.query_state = 0

            xasys.time_sleep(0.6)

            # 쿼리 결과로부터 cts_date, cts_time을 불러옴
            if cts_time != receiver.cts_time:
                cts_time = receiver.cts_time
            else:
                cts_time = ''

    endTime(trCode, engine, start_time, result_len, log)
    login.logoutServer(log)


def t2833(shcode):
    trCode = 't2833'

    log = logger(trCode)
    login = apiLogin(log)
    engine = dbLogin(log)
    receiver = XAQueryResultHandler.get_instance()

    tableOne = trCode + 'outblock1'

    shcodeList = []
    shcodeList = shcodeList + shcode
    futcheck = '0'
    cnt = '500'

    result_len = 0
    start_time = currentTime()

    date = ''
    cts_code = ''
    lastdate = ''

    for shcode in shcodeList:
        cycle = 0
        continue_Yn = True

        while continue_Yn is True:
            cycle = cycle + 1

            # 만약, 두번째 조회로 넘어왔는데, cts_time 값이 존재한다면,
            if cycle != 1 and date == '':
                continue_Yn = False
                # 연속조회 request를 해제해야함
                receiver.request = False

                # print('---[' + trCode + ' Info] pid: ' + str(login.pid), end='')
                # print(', ' + shcode + ' Continuous Request Ended')
                log.info(shcode + ' continuous request Ended')
                break
            else:
                # print('---[' + trCode + ' Info] pid: ' + str(login.pid), end='')
                # print(', Requesting ' + str(cycle) + ' cycle...')
                log.info('requesting ' + str(cycle) + ' cycle')

                InBlock = parseInfield(trCode)
                OutBlock = parseOutfield(trCode)
                InBlockValue = [shcode, futcheck, date, cts_code, lastdate, cnt]

                # 1회 이후에도 조회가 필요하면, 연속조회 request를 설정해야함
                if cycle != 1:
                    receiver.request = True

                    # 연속조회와 관련된 값을 append
                    InBlock.append('date')
                    InBlock.append('cts_code')
                    InBlock.append('lastdate')

                    InBlockValue.append(date)
                    InBlockValue.append(cts_code)
                    InBlockValue.append(lastdate)

            receiver.query(trCode, InBlock, OutBlock, InBlockValue, log)

            result = receiver.finalResult[1]
            resultCol = OutBlock[1]

            appenData(result, shcode, 0)
            appendCol(resultCol, 'shcode', 0)

            saveData(result, resultCol, tableOne, engine, log)

            result_len += len(result)

            receiver.reset()
            XAQueryResultHandler.query_state = 0

            xasys.time_sleep(3.1)

            # 쿼리 결과로부터 cts_date, cts_time을 불러옴
            date = receiver.date
            cts_code = receiver.cts_code
            lastdate = receiver.lastdate

    endTime(trCode, engine, start_time, result_len, log)
    login.logoutServer(log)


def t2835(yyyymm):
    trCode = 't2835'

    log = logger(trCode)
    login = apiLogin(log)
    engine = dbLogin(log)
    receiver = XAQueryResultHandler.get_instance()

    tableList = [trCode+'outblock1', trCode+'outblock2']
    InBlock = parseInfield(trCode)
    OutBlock = parseOutfield(trCode)
    start_time = currentTime()

    yyyymm = yyyymm

    InBlockValue = [yyyymm]
    receiver.query(trCode, InBlock, OutBlock, InBlockValue, log)

    result = receiver.finalResult
    resultCol = OutBlock
    # print(result)
    # print(resultCol)

    saveDataList2(result, resultCol, tableList, engine, log)

    result_len = 0
    result_len += len(result)

    receiver.reset()
    XAQueryResultHandler.query_state = 0
    xasys.time_sleep(3.1)

    endTime(trCode, engine, start_time, result_len, log)
    login.logoutServer(log)


def t3102(sNewsno, engine):
    trCode = 't3102'

    log = logger(trCode)
    login = apiLogin(log)
    # engine = dbLogin(log)
    receiver = XAQueryResultHandler.get_instance()

    tableOne = trCode+'outblock'

    result_len = 0
    start_time = currentTime()

    sNewsnoList = []
    sNewsnoList = sNewsnoList + sNewsno

    for sNewsno in sNewsnoList:
        InBlock = parseInfield(trCode)
        OutBlock = parseOutfield(trCode)
        InBlockValue = [sNewsno]
        receiver.query(trCode, InBlock, OutBlock, InBlockValue, log)

        # OutBlock들을 합친 후에 디비에 저장해아할 때 사용하는 코드 : 리스트 합치기 사용
        result = []
        resultCol = []

        tempResult = []
        # print(receiver.finalResult)
        idx = 0
        for item in receiver.finalResult:
            # 여기서 리스트를 하나의 변수로 처리한 후, result에 합친다
            tempList = []
            concatList = ''
            for temp in item:
                tempList = tempList + temp
            # print(tempList)
            # idx = 0인 경우, 콤마 처리
            # idx = 1인 경우, 이어 붙이기 처리
            if idx == 0:
                concatList = ",".join(tempList)
            if idx == 1:
                concatList = "".join(tempList)
            # print(concatList)

            tempResult.append(concatList)
            resultCol = resultCol + OutBlock[idx]
            idx = idx + 1

        # appenData(result, sNewsno, 0)      # 뉴스코드 추가
        # print(result)
        tempResult.insert(0, sNewsno)
        appendCol(resultCol, 'sNewsno', 0)

        # inner join으로 날짜처리
        # appenDate(result, tday)              # 날짜 추가
        # appendCol(resultCol, 'date', 0)

        # 2차원 리스트로 변환해준다.
        result.append(tempResult)
        # print(result)
        # print(resultCol)

        saveData(result, resultCol, tableOne, engine, log)

        result_len += len(result)

        receiver.reset()
        XAQueryResultHandler.query_state = 0
        xasys.time_sleep(3.1)

    endTime(trCode, engine, start_time, result_len, log)
    login.logoutServer(log)


def t3202(shcode, tday):
    trCode = 't3202'

    log = logger(trCode)
    login = apiLogin(log)
    engine = dbLogin(log)
    receiver = XAQueryResultHandler.get_instance()

    tableOne = trCode + 'outblock'

    result_len = 0
    start_time = currentTime()

    shcodeList = []
    shcodeList = shcodeList + shcode

    for shcode in shcodeList:
        InBlock = parseInfield(trCode)
        OutBlock = parseOutfield(trCode)
        InBlockValue = [shcode, tday]
        receiver.query(trCode, InBlock, OutBlock, InBlockValue, log)

        result = receiver.finalResult[0]
        resultCol = OutBlock[0]

        appenDate(result, tday)
        appendCol(resultCol, 'date', 0)

        saveData(result, resultCol, tableOne, engine, log)

        result_len += len(result)

        receiver.reset()
        XAQueryResultHandler.query_state = 0
        xasys.time_sleep(3.1)

    endTime(trCode, engine, start_time, result_len, log)
    login.logoutServer(log)


def t3320(gicode):
    trCode = 't3320'

    log = logger(trCode)
    login = apiLogin(log)
    engine = dbLogin(log)
    receiver = XAQueryResultHandler.get_instance()
    result_len = 0

    tableList = [trCode+'outblock', trCode+'outblock1']
    InBlock = parseInfield(trCode)
    OutBlock = parseOutfield(trCode)
    start_time = currentTime()

    InBlockValue = [gicode]
    receiver.query(trCode, InBlock, OutBlock, InBlockValue, log)

    result = receiver.finalResult
    resultCol = OutBlock

    # 리스트 데이터의 저장
    saveDataList(result, resultCol, tableList, engine, log)

    result_len += len(result)

    receiver.reset()
    XAQueryResultHandler.query_state = 0
    xasys.time_sleep(3.1)

    endTime(trCode, engine, start_time, result_len, log)
    login.logoutServer(log)


## symbol 코드 정리해야함
def t3518():
    trCode = 't3518'

    log = logger(trCode)
    login = apiLogin(log)
    engine = dbLogin(log)
    receiver = XAQueryResultHandler.get_instance()

    tableOne = trCode + 'outblock1'

    kindList = ['S', 'F', 'R']
    symbolList = ['NAS@IXIC', 'SPI@SPX', 'USI@SOXX', 'NII@NI225', 'TWS@TI01',
                  'SHS@000002', 'SHS@000003', 'SGI@STI', 'HSI@HSI', 'PAS@CAC40',
                  'LNS@FTSE100', 'XTR@DAX30']

    cnt = '900' # 가져올 수 있는 최대치
    jgbn = '3'  # 우선은 분봉만 가져옴
    nmin = '1'  # 1분봉

    result_len = 0
    start_time = currentTime()

    cts_time = ''
    cts_date = ''

    for kind in kindList:
        for symbol in symbolList:
            cycle = 0
            continue_Yn = True

            while continue_Yn is True:
                cycle = cycle + 1

                # 만약, 두번째 조회로 넘어왔는데, cts_time 값이 존재한다면,
                if cycle != 1 and cts_time == '':
                    continue_Yn = False
                    # 연속조회 request를 해제해야함
                    receiver.request = False

                    # print('---[' + trCode + ' Info] pid: ' + str(login.pid), end='')
                    # print(', ' + symbol + ' Continuous Request Ended')
                    log.info(symbol + ' continuous request Ended')
                    break
                else:
                    # print('---[' + trCode + ' Info] pid: ' + str(login.pid), end='')
                    # print(', Requesting ' + str(cycle) + ' cycle...')
                    log.info('requesting ' + str(cycle) + ' cycle')

                    InBlock = parseInfield(trCode)
                    OutBlock = parseOutfield(trCode)
                    InBlockValue = [kind, symbol, cnt, jgbn, nmin, cts_date, cts_time]

                    # 1회 이후에도 조회가 필요하면, 연속조회 request를 설정해야함
                    if cycle != 1:
                        receiver.request = True

                        # 연속조회와 관련된 값을 append
                        InBlock.append('cts_time')
                        InBlock.append('cts_date')

                        InBlockValue.append(cts_time)
                        InBlockValue.append(cts_date)

                receiver.query(trCode, InBlock, OutBlock, InBlockValue, log)

                result = receiver.finalResult[1]
                resultCol = OutBlock[1]

                # symbol은 이미 있으나, 값이 들어오지 않으므로, update해준다
                # appenData(result, symbol, 0)
                # appendCol(resultCol, 'symbol', 0)
                updateData(result, kind, 14)
                updateData(result, symbol, 15)
                # print(result)
                # print(resultCol)

                saveData(result, resultCol, tableOne, engine, log)

                result_len += len(result)

                receiver.reset()
                XAQueryResultHandler.query_state = 0

                xasys.time_sleep(3.1)

                # 쿼리 결과로부터 cts_date, cts_time을 불러옴
                cts_date = receiver.cts_date
                if cts_time != receiver.cts_time:
                    cts_time = receiver.cts_time
                else:
                    cts_time = ''
                    cts_date = ''

    endTime(trCode, engine, start_time, result_len, log)
    login.logoutServer(log)


def t8408(focode, tday):
    trCode = 't8408'

    log = logger(trCode)
    login = apiLogin(log)
    engine = dbLogin(log)
    receiver = XAQueryResultHandler.get_instance()

    tableOne = trCode + 'outblock1'

    focodeList = []
    focodeList = focodeList + focode
    cgubunList = ['B']     # 틱, 분 모두 저장
    bgubun = '1'
    cnt = '900'

    result_len = 0
    start_time = currentTime()

    for focode in focodeList:
        for cgubun in cgubunList:
            InBlock = parseInfield(trCode)
            OutBlock = parseOutfield(trCode)
            InBlockValue = [focode, cgubun, bgubun, cnt]
            receiver.query(trCode, InBlock, OutBlock, InBlockValue, log)

            result = receiver.finalResult[1]
            resultCol = OutBlock[1]

            appenDate(result, tday)
            appendCol(resultCol, 'date', 0)

            appenData(result, focode, 0)
            appendCol(resultCol, 'focode', 0)

            saveData(result, resultCol, tableOne, engine, log)

            result_len += len(result)

            receiver.reset()
            XAQueryResultHandler.query_state = 0
            xasys.time_sleep(3.1)

    endTime(trCode, engine, start_time, result_len, log)
    login.logoutServer(log)


def t8409(focode, tday):
    trCode = 't8409'

    log = logger(trCode)
    login = apiLogin(log)
    engine = dbLogin(log)
    receiver = XAQueryResultHandler.get_instance()

    tableOne = trCode + 'outblock1'

    focodeList = []
    focodeList = focodeList + focode
    bdgubun = '0'   # 30초
    nmin = '1'      # 분인 경우, 1분
    tcgubun = '1'   # 당일 자료만
    cnt = '1400'

    result_len = 0
    start_time = currentTime()

    for focode in focodeList:
        InBlock = parseInfield(trCode)
        OutBlock = parseOutfield(trCode)
        InBlockValue = [focode, bdgubun, nmin, tcgubun, cnt]
        receiver.query(trCode, InBlock, OutBlock, InBlockValue, log)

        result = receiver.finalResult[1]
        resultCol = OutBlock[1]

        appenDate(result, tday)
        appendCol(resultCol, 'date', 0)

        appenData(result, focode, 0)
        appendCol(resultCol, 'focode', 0)

        saveData(result, resultCol, tableOne, engine, log)

        result_len += len(result)

        receiver.reset()
        XAQueryResultHandler.query_state = 0
        xasys.time_sleep(3.1)

    endTime(trCode, engine, start_time, result_len, log)
    login.logoutServer(log)


def t8412(shcode, sdate, edate):
    # 로그인 실행: main 부분에서 실행하도록 한다
    # login()
    # 로그를 출력하는 함수에 메세지 스트링을 대입
    # strt_msg = xacom.strtFunction
    # message_info(strt_msg)

    # 로그인하면서 db 접속 후, 리턴받는 engine 을 저장함
    trCode = 't8412'

    log = logger(trCode)
    login = apiLogin(log)
    engine = dbLogin(log)
    receiver = XAQueryResultHandler.get_instance()

    tableOne = trCode + 'outblock1'
    # InBlock = parseInfield(trCode)

    shcodeList = []
    shcodeList = shcodeList + shcode
    ncnt = '1'      # 30초 >> 1분으로 변경
    qrycnt = '500'  # 비압축 500건
    comp_yn = 'N'   # 비압축

    result_len = 0
    start_time = currentTime()

    cts_time = ''
    cts_date = ''

    for shcode in shcodeList:
        cycle = 0
        continue_Yn = True

        while continue_Yn is True:
            cycle = cycle + 1

            # 만약, 두번째 조회로 넘어왔는데, cts_time 값이 존재한다면,
            if cycle != 1 and cts_time == '':
                continue_Yn = False
                # 연속조회 request를 해제해야함
                receiver.request = False

                # print('---[' + trCode + ' Info] pid: ' + str(login.pid), end='')
                # print(', ' + shcode + ' Continuous Request Ended')
                log.info(shcode + ' continuous request Ended')
                continue
            else:
                # print('---[' + trCode + ' Info] pid: ' + str(login.pid), end='')
                # print(', Requesting ' + str(cycle) + ' cycle...')
                log.info('requesting ' + str(cycle) + ' cycle')

                InBlock = parseInfield(trCode)
                OutBlock = parseOutfield(trCode)
                InBlockValue = [shcode, ncnt, qrycnt, sdate, edate, comp_yn]

                # 1회 이후에도 조회가 필요하면, 연속조회 request를 설정해야함
                if cycle != 1:
                    receiver.request = True

                    # 연속조회와 관련된 값을 append
                    InBlock.append('cts_time')
                    InBlock.append('cts_date')

                    InBlockValue.append(cts_time)
                    InBlockValue.append(cts_date)

            receiver.query(trCode, InBlock, OutBlock, InBlockValue, log)
            # 압축해제 과정
            # if comp_yn == 'Y':
            #     print(receiver.finalResult[1])
            #     result = receiver.Decompress(tableOne)
            #     print(result)
            # else:
            result = receiver.finalResult[1]
            # print(result)
            resultCol = OutBlock[1]

            # time과 open 사이에 shcode 입력
            appenData(result, shcode, 2)
            appendCol(resultCol, 'shcode', 2)

            saveData(result, resultCol, tableOne, engine, log)

            result_len += len(result)

            receiver.reset()
            receiver.query_state = 0

            # receiver로 query_state를 제어할 수 있는지 테스트
            # print(XAQueryResultHandler.query_state)
            # print(receiver.query_state)

            xasys.time_sleep(3.1)

            # 쿼리 결과로부터 cts_date, cts_time을 불러옴
            cts_date = receiver.cts_date
            if cts_time != receiver.cts_time:
                cts_time = receiver.cts_time
            else:
                cts_time = ''
                cts_date = ''

    endTime(trCode, engine, start_time, result_len, log)
    login.logoutServer(log)


def t8413(shcode, sdate, edate):
    trCode = 't8413'

    log = logger(trCode)
    login = apiLogin(log)
    engine = dbLogin(log)
    receiver = XAQueryResultHandler.get_instance()

    tableOne = trCode + 'outblock1'

    shcodeList = []
    shcodeList = shcodeList + shcode
    gubun = '2'
    comp_yn = 'N'  # 비압축

    result_len = 0
    start_time = currentTime()

    cts_date = ''
    for shcode in shcodeList:
        cycle = 0
        continue_Yn = True

        while continue_Yn is True:
            cycle = cycle + 1

            # 만약, 두번째 조회로 넘어왔는데, cts_time 값이 존재한다면,
            if cycle != 1 and cts_date == '':
                continue_Yn = False
                # 연속조회 request를 해제해야함
                receiver.request = False

                # print('---[' + trCode + ' Info] pid: ' + str(login.pid), end='')
                # print(', ' + shcode + ' Continuous Request Ended')
                log.info(shcode + ' continuous request Ended')
                break
            else:
                # print('---[' + trCode + ' Info] pid: ' + str(login.pid), end='')
                # print(', Requesting ' + str(cycle) + ' cycle...')
                log.info('requesting ' + str(cycle) + ' cycle')

                InBlock = parseInfield(trCode)
                OutBlock = parseOutfield(trCode)
                InBlockValue = [shcode, gubun, sdate, edate, comp_yn]

                # 1회 이후에도 조회가 필요하면, 연속조회 request를 설정해야함
                if cycle != 1:
                    receiver.request = True

                    # 연속조회와 관련된 값을 append
                    InBlock.append('cts_date')
                    InBlockValue.append(cts_date)

            receiver.query(trCode, InBlock, OutBlock, InBlockValue, log)

            result = receiver.finalResult[1]
            resultCol = OutBlock[1]
            # date과 open 사이에 shcode 입력
            appenData(result, shcode, 1)
            appendCol(resultCol, 'shcode', 1)

            saveData(result, resultCol, tableOne, engine, log)

            result_len += len(result)

            receiver.reset()
            XAQueryResultHandler.query_state = 0

            # receiver로 query_state를 제어할 수 있는지 테스트
            # print(XAQueryResultHandler.query_state)
            # print(receiver.query_state)

            xasys.time_sleep(3.1)

            # 쿼리 결과로부터 cts_date, cts_time을 불러옴
            cts_date = receiver.cts_date

    endTime(trCode, engine, start_time, result_len, log)
    login.logoutServer(log)


def t8414(shcode, sdate, edate):
    trCode = 't8414'

    log = logger(trCode)
    login = apiLogin(log)
    engine = dbLogin(log)
    receiver = XAQueryResultHandler.get_instance()

    tableOne = trCode + 'outblock1'

    shcodeList = []
    shcodeList = shcodeList + shcode
    ncnt = '1'  # 1틱
    qrycnt = '500'  # 비압축 500건
    comp_yn = 'N'  # 비압축

    result_len = 0
    start_time = currentTime()

    cts_time = ''
    cts_date = ''

    for shcode in shcodeList:
        cycle = 0
        continue_Yn = True

        while continue_Yn is True:
            cycle = cycle + 1

            # 만약, 두번째 조회로 넘어왔는데, cts_time 값이 존재한다면,
            if cycle != 1 and cts_time == '':
                continue_Yn = False
                # 연속조회 request를 해제해야함
                receiver.request = False

                # print('---[' + trCode + ' Info] pid: ' + str(login.pid), end='')
                # print(', ' + shcode + ' Continuous Request Ended')
                log.info(shcode + ' continuous request Ended')
                continue
            else:
                # print('---[' + trCode + ' Info] pid: ' + str(login.pid), end='')
                # print(', Requesting ' + str(cycle) + ' cycle...')
                log.info('requesting ' + str(cycle) + ' cycle')

                InBlock = parseInfield(trCode)
                OutBlock = parseOutfield(trCode)
                InBlockValue = [shcode, ncnt, qrycnt, sdate, edate, comp_yn]

                # 1회 이후에도 조회가 필요하면, 연속조회 request를 설정해야함
                if cycle != 1:
                    receiver.request = True

                    # 연속조회와 관련된 값을 append
                    InBlock.append('cts_time')
                    InBlock.append('cts_date')

                    InBlockValue.append(cts_time)
                    InBlockValue.append(cts_date)

            receiver.query(trCode, InBlock, OutBlock, InBlockValue, log)

            result = receiver.finalResult[1]
            resultCol = OutBlock[1]

            # time과 open 사이에 shcode 입력
            appenData(result, shcode, 2)
            appendCol(resultCol, 'shcode', 2)

            saveData(result, resultCol, tableOne, engine, log)

            result_len += len(result)

            receiver.reset()
            XAQueryResultHandler.query_state = 0

            xasys.time_sleep(3.1)

            # 쿼리 결과로부터 cts_date, cts_time을 불러옴
            cts_date = receiver.cts_date
            if cts_time != receiver.cts_time:
                cts_time = receiver.cts_time
            else:
                cts_time = ''
                cts_date = ''

    endTime(trCode, engine, start_time, result_len, log)
    login.logoutServer(log)


def t8415(shcode, sdate, edate):
    trCode = 't8415'

    log = logger(trCode)
    login = apiLogin(log)
    engine = dbLogin(log)
    receiver = XAQueryResultHandler.get_instance()

    tableOne = trCode + 'outblock1'

    shcodeList = []
    shcodeList = shcodeList + shcode
    ncnt = '0'  # 30초
    qrycnt = '500'  # 비압축 500건
    comp_yn = 'N'  # 비압축

    result_len = 0
    start_time = currentTime()

    cts_time = ''
    cts_date = ''

    for shcode in shcodeList:
        cycle = 0
        continue_Yn = True

        while continue_Yn is True:
            cycle = cycle + 1

            # 만약, 두번째 조회로 넘어왔는데, cts_time 값이 존재한다면,
            if cycle != 1 and cts_time == '':
                continue_Yn = False
                # 연속조회 request를 해제해야함
                receiver.request = False

                # print('---[' + trCode + ' Info] pid: ' + str(login.pid), end='')
                # print(', ' + shcode + ' Continuous Request Ended')
                log.info(shcode + ' continuous request Ended')
                break
            else:
                # print('---[' + trCode + ' Info] pid: ' + str(login.pid), end='')
                # print(', Requesting ' + str(cycle) + ' cycle...')
                log.info('requesting ' + str(cycle) + ' cycle')

                InBlock = parseInfield(trCode)
                OutBlock = parseOutfield(trCode)
                InBlockValue = [shcode, ncnt, qrycnt, sdate, edate, comp_yn]

                # 1회 이후에도 조회가 필요하면, 연속조회 request를 설정해야함
                if cycle != 1:
                    receiver.request = True

                    # 연속조회와 관련된 값을 append
                    InBlock.append('cts_time')
                    InBlock.append('cts_date')

                    InBlockValue.append(cts_time)
                    InBlockValue.append(cts_date)

            receiver.query(trCode, InBlock, OutBlock, InBlockValue, log)

            result = receiver.finalResult[1]
            resultCol = OutBlock[1]

            # time과 open 사이에 shcode 입력
            appenData(result, shcode, 2)
            appendCol(resultCol, 'shcode', 2)

            saveData(result, resultCol, tableOne, engine, log)

            result_len += len(result)

            receiver.reset()
            XAQueryResultHandler.query_state = 0

            xasys.time_sleep(3.1)

            # 쿼리 결과로부터 cts_date, cts_time을 불러옴
            cts_date = receiver.cts_date
            # 데이터가 없으면 cts_time, date가 갱신이 안되어 무한루프 도는 것 방지
            if cts_time != receiver.cts_time:
                cts_time = receiver.cts_time
            else:
                cts_time = ''
                cts_date = ''

    endTime(trCode, engine, start_time, result_len, log)
    login.logoutServer(log)


def t8416(shcode, sdate, edate):
    trCode = 't8416'

    log = logger(trCode)
    login = apiLogin(log)
    engine = dbLogin(log)
    receiver = XAQueryResultHandler.get_instance()

    tableOne = trCode + 'outblock1'

    shcodeList = []
    shcodeList = shcodeList + shcode
    gubun = '2'
    comp_yn = 'N'  # 비압축

    result_len = 0
    start_time = currentTime()

    cts_date = ''

    for shcode in shcodeList:
        cycle = 0
        continue_Yn = True

        while continue_Yn is True:
            cycle = cycle + 1

            # 만약, 두번째 조회로 넘어왔는데, cts_time 값이 존재한다면,
            if cycle != 1 and cts_date == '':
                continue_Yn = False
                # 연속조회 request를 해제해야함
                receiver.request = False

                # print('---[' + trCode + ' Info] pid: ' + str(login.pid), end='')
                # print(', ' + shcode + ' Continuous Request Ended')
                log.info(shcode + ' continuous request Ended')
                break
            else:
                # print('---[' + trCode + ' Info] pid: ' + str(login.pid), end='')
                # print(', Requesting ' + str(cycle) + ' cycle...')
                log.info('requesting ' + str(cycle) + ' cycle')

                InBlock = parseInfield(trCode)
                OutBlock = parseOutfield(trCode)
                InBlockValue = [shcode, gubun, sdate, edate, comp_yn]

                # 1회 이후에도 조회가 필요하면, 연속조회 request를 설정해야함
                if cycle != 1:
                    receiver.request = True

                    # 연속조회와 관련된 값을 append
                    InBlock.append('cts_date')
                    InBlockValue.append(cts_date)

            receiver.query(trCode, InBlock, OutBlock, InBlockValue, log)

            result = receiver.finalResult[1]
            resultCol = OutBlock[1]
            # date과 open 사이에 shcode 입력
            appenData(result, shcode, 1)
            appendCol(resultCol, 'shcode', 1)

            saveData(result, resultCol, tableOne, engine, log)

            result_len += len(result)

            receiver.reset()
            XAQueryResultHandler.query_state = 0

            xasys.time_sleep(3.1)

            cts_date = receiver.cts_date

    endTime(trCode, engine, start_time, result_len, log)
    login.logoutServer(log)


def t8417(shcode, sdate, edate):
    trCode = 't8417'

    log = logger(trCode)
    login = apiLogin(log)
    engine = dbLogin(log)
    receiver = XAQueryResultHandler.get_instance()

    tableOne = trCode + 'outblock1'

    shcodeList = []
    shcodeList = shcodeList + shcode
    ncnt = '1'      # 1틱
    qrycnt = '500'  # 비압축 500건
    comp_yn = 'N'  # 비압축

    result_len = 0
    start_time = currentTime()

    cts_time = ''
    cts_date = ''

    for shcode in shcodeList:
        cycle = 0
        continue_Yn = True

        while continue_Yn is True:
            cycle = cycle + 1

            # 만약, 두번째 조회로 넘어왔는데, cts_time 값이 존재한다면,
            if cycle != 1 and cts_time == '':
                continue_Yn = False
                # 연속조회 request를 해제해야함
                receiver.request = False

                # print('---[' + trCode + ' Info] pid: ' + str(login.pid), end='')
                # print(', ' + shcode + ' Continuous Request Ended')
                log.info(shcode + ' continuous request Ended')
                break
            else:
                # print('---[' + trCode + ' Info] pid: ' + str(login.pid), end='')
                # print(', Requesting ' + str(cycle) + ' cycle...')
                log.info('requesting ' + str(cycle) + ' cycle')

                InBlock = parseInfield(trCode)
                OutBlock = parseOutfield(trCode)
                InBlockValue = [shcode, ncnt, qrycnt, sdate, edate, comp_yn]

                # 1회 이후에도 조회가 필요하면, 연속조회 request를 설정해야함
                if cycle != 1:
                    receiver.request = True

                    # 연속조회와 관련된 값을 append
                    InBlock.append('cts_time')
                    InBlock.append('cts_date')

                    InBlockValue.append(cts_time)
                    InBlockValue.append(cts_date)

            receiver.query(trCode, InBlock, OutBlock, InBlockValue, log)

            result = receiver.finalResult[1]
            resultCol = OutBlock[1]
            # time과 open 사이에 shcode 입력
            appenData(result, shcode, 2)
            appendCol(resultCol, 'shcode', 2)

            saveData(result, resultCol, tableOne, engine, log)

            result_len += len(result)

            receiver.reset()
            XAQueryResultHandler.query_state = 0

            xasys.time_sleep(3.1)

            # 쿼리 결과로부터 cts_date, cts_time을 불러옴
            cts_date = receiver.cts_date
            if cts_time != receiver.cts_time:
                cts_time = receiver.cts_time
            else:
                cts_time = ''
                cts_date = ''

    endTime(trCode, engine, start_time, result_len, log)
    login.logoutServer(log)


def t8418(shcode, sdate, edate):
    trCode = 't8418'

    log = logger(trCode)
    login = apiLogin(log)
    engine = dbLogin(log)
    receiver = XAQueryResultHandler.get_instance()

    tableOne = trCode + 'outblock1'

    shcodeList = []
    shcodeList = shcodeList + shcode
    ncnt = '0'  # 30초
    qrycnt = '500'  # 비압축 500건
    comp_yn = 'N'  # 비압축

    result_len = 0
    start_time = currentTime()

    cts_time = ''
    cts_date = ''

    for shcode in shcodeList:
        cycle = 0
        continue_Yn = True

        while continue_Yn is True:
            cycle = cycle + 1

            # 만약, 두번째 조회로 넘어왔는데, cts_time 값이 존재한다면,
            if cycle != 1 and cts_time == '':
                continue_Yn = False
                # 연속조회 request를 해제해야함
                receiver.request = False

                # print('---[' + trCode + ' Info] pid: ' + str(login.pid), end='')
                # print(', ' + shcode + ' Continuous Request Ended')
                log.info(shcode + ' continuous request Ended')
                break
            else:
                # print('---[' + trCode + ' Info] pid: ' + str(login.pid), end='')
                # print(', Requesting ' + str(cycle) + ' cycle...')
                log.info('requesting ' + str(cycle) + ' cycle')

                InBlock = parseInfield(trCode)
                OutBlock = parseOutfield(trCode)
                InBlockValue = [shcode, ncnt, qrycnt, sdate, edate, comp_yn]

                # 1회 이후에도 조회가 필요하면, 연속조회 request를 설정해야함
                if cycle != 1:
                    receiver.request = True

                    # 연속조회와 관련된 값을 append
                    InBlock.append('cts_time')
                    InBlock.append('cts_date')

                    InBlockValue.append(cts_time)
                    InBlockValue.append(cts_date)

            receiver.query(trCode, InBlock, OutBlock, InBlockValue, log)

            result = receiver.finalResult[1]
            resultCol = OutBlock[1]

            # time과 open 사이에 shcode 입력
            appenData(result, shcode, 2)
            appendCol(resultCol, 'shcode', 2)

            saveData(result, resultCol, tableOne, engine, log)

            result_len += len(result)

            receiver.reset()
            XAQueryResultHandler.query_state = 0

            xasys.time_sleep(3.1)

            # 쿼리 결과로부터 cts_date, cts_time을 불러옴
            cts_date = receiver.cts_date
            if cts_time != receiver.cts_time:
                cts_time = receiver.cts_time
            else:
                cts_time = ''
                cts_date = ''

    endTime(trCode, engine, start_time, result_len, log)
    login.logoutServer(log)


def t8419(shcode, sdate, edate):
    trCode = 't8419'

    log = logger(trCode)
    login = apiLogin(log)
    engine = dbLogin(log)
    receiver = XAQueryResultHandler.get_instance()

    tableOne = trCode + 'outblock1'

    shcodeList = []
    shcodeList = shcodeList + shcode
    gubun = '2'
    comp_yn = 'N'  # 비압축

    result_len = 0
    start_time = currentTime()

    cts_date = ''

    for shcode in shcodeList:
        cycle = 0
        continue_Yn = True

        while continue_Yn is True:
            cycle = cycle + 1

            # 만약, 두번째 조회로 넘어왔는데, cts_time 값이 존재한다면,
            if cycle != 1 and cts_date == '':
                continue_Yn = False
                # 연속조회 request를 해제해야함
                receiver.request = False

                # print('---[' + trCode + ' Info] pid: ' + str(login.pid), end='')
                # print(', ' + shcode + ' Continuous Request Ended')
                log.info(shcode + ' continuous request Ended')
                break
            else:
                # print('---[' + trCode + ' Info] pid: ' + str(login.pid), end='')
                # print(', Requesting ' + str(cycle) + ' cycle...')
                log.info('requesting ' + str(cycle) + ' cycle')

                InBlock = parseInfield(trCode)
                OutBlock = parseOutfield(trCode)
                InBlockValue = [shcode, gubun, sdate, edate, comp_yn]

                # 1회 이후에도 조회가 필요하면, 연속조회 request를 설정해야함
                if cycle != 1:
                    receiver.request = True

                    # 연속조회와 관련된 값을 append
                    InBlock.append('cts_date')
                    InBlockValue.append(cts_date)

            receiver.query(trCode, InBlock, OutBlock, InBlockValue, log)

            result = receiver.finalResult[1]
            resultCol = OutBlock[1]
            # date과 open 사이에 shcode 입력
            appenData(result, shcode, 1)
            appendCol(resultCol, 'shcode', 1)

            saveData(result, resultCol, tableOne, engine, log)

            result_len += len(result)

            receiver.reset()
            XAQueryResultHandler.query_state = 0

            # print(XAQueryResultHandler.query_state)
            # print(receiver.query_state)
            xasys.time_sleep(3.1)

            # 쿼리 결과로부터 cts_date, cts_time을 불러옴
            cts_date = receiver.cts_date

    endTime(trCode, engine, start_time, result_len, log)
    login.logoutServer(log)


def t8424():
    trCode = 't8424'

    log = logger(trCode)
    login = apiLogin(log)
    engine = dbLogin(log)
    receiver = XAQueryResultHandler.get_instance()
    # 코드 리스트를 담을 객체생성
    upcodeList = codeList()

    InBlock = parseInfield(trCode)
    OutBlock = parseOutfield(trCode)
    start_time = currentTime()

    InBlockValue = ' '
    receiver.query(trCode, InBlock, OutBlock, InBlockValue, log)

    tableOne = trCode + 'outblock'
    result = upcodeList.upcodeList(receiver.finalResult[0])
    resultCol = [OutBlock[0][1]]

    saveData2(result, resultCol, tableOne, engine, log)

    result_len = 0
    result_len += len(result)

    receiver.reset()
    XAQueryResultHandler.query_state = 0
    xasys.time_sleep(3.1)

    endTime(trCode, engine, start_time, result_len, log)
    login.logoutServer(log)

    # return result
    upcodeList.upcodeList(result)


# 매뉴얼로 데이터를 조회하는 함수이므로, 모두 다 입력하도록 해준다
def t8427(fo_gbn, yyyy, mm, cp_gbn, actprice, focode, dt_gbn, min_term):
    trCode = 't8427'

    log = logger(trCode)
    login = apiLogin(log)
    engine = dbLogin(log)
    receiver = XAQueryResultHandler.get_instance()

    tableOne = trCode + 'outblock1'

    time = ''
    date = ''
    continue_Yn = True
    cycle = 0
    result_len = 0

    start_time = currentTime()

    while continue_Yn is True:
        cycle = cycle + 1

        # 만약, 두번째 조회로 넘어왔는데, cts_time 값이 존재한다면,
        if cycle != 1 and time == '':

            # continue_Yn 왜 사용되지 않음으로 표시.. ?
            continue_Yn = False
            # 연속조회 request를 해제해야함
            receiver.request = False

            # print('---[' + trCode + ' Info] pid: ' + str(login.pid), end='')
            # print(', ' + focode + ' Continuous Request Ended')
            log.info(focode + ' continuous request Ended')
            break
        else:
            # print('---[' + trCode + ' Info] pid: ' + str(login.pid), end='')
            # print(', Requesting ' + str(cycle) + ' cycle...')
            log.info('requesting ' + str(cycle) + ' cycle')

            InBlock = parseInfield(trCode)
            OutBlock = parseOutfield(trCode)
            # OutBlock1에 focode 추가
            InBlockValue = [fo_gbn, yyyy, mm, cp_gbn, actprice, focode, dt_gbn, min_term]

            # 1회 이후에도 조회가 필요하면, 연속조회 request를 설정해야함
            if cycle != 1:
                receiver.request = True

                # 연속조회와 관련된 값을 append
                InBlock.append('time')
                InBlock.append('date')

                InBlockValue.append(time)
                InBlockValue.append(date)

        receiver.query(trCode, InBlock, OutBlock, InBlockValue, log)

        result = receiver.finalResult[1]
        resultCol = OutBlock[1]

        appenData(result, focode, 0)
        appendCol(resultCol, 'focode', 0)

        saveData(result, resultCol, tableOne, engine, log)

        result_len += len(result)

        receiver.reset()
        XAQueryResultHandler.query_state = 0

        xasys.time_sleep(3.1)

        # 쿼리 결과로부터 cts_date, cts_time을 불러옴
        date = receiver.cts_date
        if time != receiver.time:
            time = receiver.time
        else:
            time = ''
            date = ''

    endTime(trCode, engine, start_time, result_len, log)
    login.logoutServer(log)


def t8428(fdate, tdate):
    trCode = 't8428'

    log = logger(trCode)
    login = apiLogin(log)
    engine = dbLogin(log)
    receiver = XAQueryResultHandler.get_instance()

    tableOne = trCode + 'outblock1'
    start_time = currentTime()

    # gubunList = ['1', '2']
    gubun = '1'     # gubun 값 의미없음
    upcodeList = ['001', '301']
    key_date = ''
    cnt = '300' # 1년치 정도
    # 만약, 월요일인 경우, 금요일을 가르키도록 해야하므로,
    # TODAY = datetime.datetime(dt.year, dt.month, dt.day - 1).strftime('%Y%m%d')
    """
    # 추후, 평일 공휴일 처리도 해주어야 한다..o
    오늘 날짜는 공휴일 처리된 날짜
    오늘로부터 -2일인 날짜가 공휴일인지 아닌지 처리가 필요..o
    """
    fdate = returnTradeDay(returnDateFromThisDay(fdate, 2))
    result_len = 0

    # fdate, tdate는 기본적으로 sdate, edate를 가져오므로
    # 여기서 날짜 처리를 해야함.. 기준날짜의 -2 처리

    # for gubun in gubunList:
    for upcode in upcodeList:
        # 업종코드를 컬럼에 추가
        InBlock = parseInfield(trCode)
        OutBlock = parseOutfield(trCode)
        InBlockValue = [fdate, tdate, gubun, key_date, upcode, cnt]
        receiver.query(trCode, InBlock, OutBlock, InBlockValue, log)

        result = receiver.finalResult[1]
        resultCol = OutBlock[1]

        appenData(result, upcode, 1)
        appendCol(resultCol, 'upcode', 1)
        # print(result)
        # print(resultCol)

        saveData(result, resultCol, tableOne, engine, log)

        result_len += len(result)

        receiver.reset()
        XAQueryResultHandler.query_state = 0
        xasys.time_sleep(3.1)

    endTime(trCode, engine, start_time, result_len, log)
    login.logoutServer(log)


def t8429(focode, tday):
    trCode = 't8429'

    log = logger(trCode)
    login = apiLogin(log)
    engine = dbLogin(log)
    receiver = XAQueryResultHandler.get_instance()

    tableOne = trCode + 'outblock1'
    start_time = currentTime()

    focodeList = []
    focodeList = focodeList + focode
    # cgubunList = ['T', 'B']     # 틱, 분 모두 저장
    cgubunList = ['B']
    bgubun = '1'
    cnt = '900'

    result_len = 0

    for focode in focodeList:
        for cgubun in cgubunList:
            InBlock = parseInfield(trCode)
            OutBlock = parseOutfield(trCode)
            InBlockValue = [focode, cgubun, bgubun, cnt]
            receiver.query(trCode, InBlock, OutBlock, InBlockValue, log)

            result = receiver.finalResult[1]
            resultCol = OutBlock[1]

            appenData(result, focode, 0)
            appendCol(resultCol, 'focode', 0)

            appenDate(result, tday)
            appendCol(resultCol, 'date', 0)

            saveData(result, resultCol, tableOne, engine, log)

            result_len += len(result)

            receiver.reset()
            XAQueryResultHandler.query_state = 0
            xasys.time_sleep(3.1)

    endTime(trCode, engine, start_time, result_len, log)
    login.logoutServer(log)


def t8430():
    trCode = 't8430'

    log = logger(trCode)
    login = apiLogin(log)
    engine = dbLogin(log)
    receiver = XAQueryResultHandler.get_instance()
    shcodeList = codeList()

    InBlock = parseInfield(trCode)
    OutBlock = parseOutfield(trCode)
    start_time = currentTime()

    InBlockValue = '0'
    receiver.query(trCode, InBlock, OutBlock, InBlockValue, log)

    tableOne = trCode + 'outblock'
    result = shcodeList.shcodeList(receiver.finalResult[0])
    resultCol = [OutBlock[0][1]]

    saveData2(result, resultCol, tableOne, engine, log)

    result_len = 0
    result_len += len(result)

    receiver.reset()
    XAQueryResultHandler.query_state = 0
    xasys.time_sleep(3.1)

    endTime(trCode, engine, start_time, result_len, log)
    login.logoutServer(log)

    # return result
    shcodeList.shcodeList(result)


def t9943():
    trCode = 't9943'

    log = logger(trCode)
    login = apiLogin(log)
    engine = dbLogin(log)
    receiver = XAQueryResultHandler.get_instance()
    fucodeList = codeList()

    InBlock = parseInfield(trCode)
    OutBlock = parseOutfield(trCode)
    start_time = currentTime()

    result = []
    gubunList = ['V', 'S', '']

    for gubun in gubunList:
        InBlockValue = [gubun]
        receiver.query(trCode, InBlock, OutBlock, InBlockValue, log)
        result.extend(fucodeList.fucodeList(receiver.finalResult[0]))
        # print(result)

        receiver.reset()
        XAQueryResultHandler.query_state = 0
        xasys.time_sleep(1.3)

    tableOne = trCode + 'outblock'
    resultCol = [OutBlock[0][1]]
    saveData2(result, resultCol, tableOne, engine, log)

    result_len = 0
    result_len += len(result)

    xasys.time_sleep(1.3)

    endTime(trCode, engine, start_time, result_len, log)
    login.logoutServer(log)

    # return result
    fucodeList.fucodeList(result)


def t9944():
    """
    지수옵션 마스터조회 api용
    정기
    :return:
    """
    trCode = 't9944'
    log = logger(trCode)
    login = apiLogin(log)
    engine = dbLogin(log)
    receiver = XAQueryResultHandler.get_instance()
    opcodeList = codeList()

    tableOne = trCode + 'outblock'
    InBlock = parseInfield(trCode)
    OutBlock = parseOutfield(trCode)
    start_time = currentTime()

    # '' 을 넣어주면 에러가 발생하여 space를 입력
    InBlockValue = ' '
    receiver.query(trCode, InBlock, OutBlock, InBlockValue, log)

    result = opcodeList.opcodeList(receiver.finalResult[0])
    resultCol = [OutBlock[0][1]]

    saveData2(result, resultCol, tableOne, engine, log)

    result_len = 0
    result_len += len(result)

    receiver.reset()
    XAQueryResultHandler.query_state = 0
    xasys.time_sleep(3.1)

    endTime(trCode, engine, start_time, result_len, log)
    login.logoutServer(log)

    # return result
    # finalResult = []
    # finalResult.extend(opcodeList.opcodeList(result))
    # return finalResult
    # return_list[0] = opcodeList.opcodeList(result)

    ## db에 저장
    # real은 여기까지 도달하지 않음,.. receive에서 처리해줘야 함
    # result = receiver.finalResult
    # resultCol = OutBlock
    #
    # saveData(result, resultCol, trCode, tableOne, engine)


"""
# 저장되는 데이터 시간대 판단
def getTimeSchedule(engine):
    nextime = pd.read_sql(sql='select nextime from tb_setting', con=engine).nextime.tolist()
    return nextime


# 다음 스케줄 시간대 세팅
def setNextime(engine):
    nextime = ''
    return nextime
"""


# 중복되는 데이터가 없도록 처리해야함
def saveData(result, resultCol, tableOne, engine, log):
    """
    db에 데이터 저장
    :param result:
    :param resultCol:
    :param trCode:
    :param tableOne:
    :param engine:
    :return:
    """
    # print('---[Info] trCode: ' + trCode + ', dataFrame to_sql')
    if len(result) != 0:
        try:
            df = pd.DataFrame(result)
            # print(df)
            df.columns = resultCol
            # 중복되는 데이터가 없도록 처리해야함
            df.to_sql(name=tableOne, con=engine, if_exists='append', index=False)
            log.info('to_sql success')
        except Exception as e:
            log.error('error Occured when to_sql: ', str(e))
        # print('---[' + trCode + ' Info] to_sql success')
    else:
        # print('---[' + trCode + ' Info] failed to_sql: list is empty')
        log.info('failed to_sql: list is empty')


def saveData2(result, resultCol, tableOne, engine, log):
    """
    종목코드를 위한 db 저장 함수
    :param result:
    :param resultCol:
    :param trCode:
    :param tableOne:
    :param engine:
    :return:
    """
    if len(result) != 0:
        try:
            df = pd.DataFrame(result)
            df.columns = resultCol
            df.to_sql(name=tableOne, con=engine, if_exists='replace', index=False)
            log.info('to_sql success')
        except Exception as e:
            log.error('error Occured when to_sql: ', str(e))
        # print('---[' + trCode + ' Info] to_sql success')
    else:
        log.info('failed to_sql: list is empty')
        # print('---[' + trCode + ' Info] failed to_sql: list is empty')


def saveDataList(result, resultCol, tableList, engine, log):
    # 디비에 저장할 테이블 여러개일 때, 처리 코드
    for table in tableList:
        # tableList의 OutBlock 인덱스를 가져옴
        idx = table[len(table) - 1]
        if idx == 'k':
            idx = 0
        else:
            idx = int(idx)

        if len(result[idx]) != 0:
            try:
                df = pd.DataFrame(result[idx])
                df.columns = resultCol[idx]
                df.to_sql(name=table, con=engine, if_exists='append', index=False)
                log.info('to_sql success')
            except Exception as e:
                log.error('error Occured when to_sql: ', str(e))
            # print('---[' + trCode + ' Info] to_sql success')
        else:
            log.info('failed to_sql: list is empty')
            # print('---[' + trCode + ' Info] failed to_sql: list is empty')


def saveDataList2(result, resultCol, tableList, engine, log):
    """
    db에 저장 리스트형
    :param result:
    :param resultCol:
    :param trCode:
    :param tableList:
    :param receiver:
    :param engine:
    :return:
    """

    for table in tableList:
        # tableList의 OutBlock 인덱스를 가져옴
        idx = table[len(table) - 1]
        if idx == 'k':
            idx = 0
        else:
            idx = int(idx)

        appenDate(result[idx], '')
        appendCol(resultCol[idx], 'date', 0)

        if len(result[idx]) != 0:
            try:
                df = pd.DataFrame(result[idx])
                df.columns = resultCol[idx]
                df.to_sql(name=table, con=engine, if_exists='append', index=False)
                log.info('to_sql success')
            except Exception as e:
                log.error('error Occured when to_sql: ', str(e))
            # print('---[' + trCode + ' Info] to_sql success')
        else:
            log.info('failed to_sql: list is empty')
            # print('---[' + trCode + ' Info] failed to_sql: list is empty')


def appenDate(dataList, date):
    """
    :param data_list: 리스트 형식의 한 outBlock 데이터
    :return: 날짜가 추가된 데이터 반환
    """
    result = dataList
    if date == '':
        date = closestTradeDay()

    for i in range(len(result)):
        result[i].insert(0, date)

    return result


def appenData(dataList, item, idx):
    """
    idx 위치에 item을 삽입한다
    :param data_list:
    :param item:
    :param idx:
    :return:
    """
    result = dataList
    rng = len(result)

    for i in range(rng):
        result[i].insert(idx, item)

    return result


def appendCol(colList, item, idx):
    """
    테이블 컬럼을 추가
    :param colList:
    :param item:
    :param idx:
    :return:
    """
    result = colList
    # 중복으로 컬럼이 등록되는 것을 방지
    for list_item in colList:
        if list_item == item:
            return
    result.insert(idx, item)

    return result


def updateData(dataList, item, idx):
    """
    dataList의 idx 컬럼의 데이터를 item으로 수정
    :param dataList:
    :param item:
    :param idx:
    :return:
    """
    result = dataList
    for i in range(len(result)):
        result[i][idx] = item

    return result


def updateCol(colList, item, idx):
    """
    columnList의 idx 번째 컬럼을 item으로 수정
    :param colList:
    :param item:
    :param idx:
    :return:
    """
    result = colList
    result[idx] = item
    return result


class codeList:

    def __init__(self):
        self.shcode = []
        self.focode = []
        self.opcode = []
        self.fucode = []
        self.upcode = []

        self.shcodeRaw = []
        self.opcodeRaw = []
        self.fucodeRaw = []
        self.upcodeRaw = []

    def shcodeList(self, shcode):
        self.shcodeRaw = self.shcodeRaw + shcode
        for i in range(len(self.shcodeRaw)):
            self.shcode.append(self.shcodeRaw[i][1])
        # print(self.shcode)
        return self.shcode

    def focodeList(self, fucode, opcode):
        self.focode = self.focode + fucode + opcode
        # print(self.focode)
        return self.focode

    def opcodeList(self, opcode):
        self.opcodeRaw = self.opcodeRaw + opcode
        for i in range(len(self.opcodeRaw)):
            self.opcode.append(self.opcodeRaw[i][1])
        # print(self.opcode)
        return self.opcode

    def fucodeList(self, fucode):
        self.fucodeRaw = self.fucodeRaw + fucode
        for i in range(len(self.fucodeRaw)):
            self.fucode.append(self.fucodeRaw[i][1])
        # print(self.fucode)
        return self.fucode

    def upcodeList(self, upcode):
        self.upcodeRaw = self.upcodeRaw + upcode
        for i in range(len(self.upcodeRaw)):
            self.upcode.append(self.upcodeRaw[i][1])
        # print(self.upcode)
        return self.upcode


def closestTradeDay():
    """
    공휴일 및 휴일 처리한 날짜를 리턴함
    : 토, 일요일 처리 제외. 공휴일, 야간 처리만 하는 것으로 변경함
    :return:
    """
    dt = datetime.datetime.now()
    hour = dt.hour

    # 야간 날짜 처리:
    if hour in range(0, 9):
        # dt_day = dt.day
        # dt_month = dt.month
        # dt_year = dt.year
        TODAY = (dt + datetime.timedelta(days=-1)).strftime('%Y%m%d')
        return TODAY

        # if (dt.day - 1) == 0:
        # extraDay = [1, 3, 5, 7, 8, 10, 12]
        # normalDay = [4, 6, 9, 11]
        #
        # if dt_month in extraDay:
        #     dt_day = 31
        # elif dt_month in normalDay:
        #     dt_day = 30
        # else:
        #     if dt_year % 4 == 0:
        #         dt_day = 29
        #     else:
        #         dt_day = 28
        #
        # dt_month = dt.month - 1

        # TODAY = (dt + datetime.timedelta(days=-1)).strftime('%Y%m%d')
        # return TODAY
        # else:
        #     dt.strftime()
        # else:
        #     TODAY = datetime.datetime(dt.year, dt_month, dt_day - 1).strftime('%Y%m%d')
        # return TODAY

    else:
        TODAY = datetime.datetime.now().strftime('%Y%m%d')
        return TODAY

    # 토요일, 일요일인 경우 처리
    # if dt.weekday() == 5:
    #     TODAY = returnDate(1)
    #     # 공휴일인 경우를 처리함
    #     resultDay = str(returnTradeDay(TODAY))
    #     return resultDay
    #
    # elif dt.weekday() == 6:
    #     TODAY = returnDate(2)
    #     resultDay = str(returnTradeDay(TODAY))
    #     return resultDay
    #
    # else:
    #     resultDay = str(returnTradeDay(TODAY))
    #     return resultDay


def todayMonth():
    """
    이번 달을 리턴함
    :return:
    """
    yyyymm = datetime.datetime.now().strftime('%Y%m')
    return yyyymm


def todayDate():
    """
    오늘 일자를 리턴함
    :return:
    """
    today = datetime.datetime.now().strftime('%Y%m%d')
    return today


def todayHour():
    """
    현재 hour를 리턴함
    :return:
    """
    hour = datetime.datetime.now().strftime('%H')
    return int(hour)


def todayOfWeek():
    """
    오늘의 요일을 리턴함
    :return:
    """
    dt = datetime.datetime.now()
    dayOfWeek = dt.weekday()

    return dayOfWeek


def returnDate(cnt):
    """
    지정한 날 수를 뺀 날짜를 리턴함
    :param day:
    :return:
    """
    dt = datetime.datetime.now()
    return_date = (dt + datetime.timedelta(days=-cnt)).strftime('%Y%m%d')
    # print('>>>'+return_date + '<<<')
    return return_date


def returnDateFromThisDay(this_day, cnt):
    """
    지정한 날로부터 cnt 만큼의 날짜를 리턴함
    :param this_day:
    :param cnt:
    :return:
    """
    year = this_day[0:4]
    month = this_day[4:6]
    day = this_day[6:8]

    result = (datetime.datetime(int(year), int(month), int(day)) + datetime.timedelta(days=-cnt)).strftime('%Y%m%d')
    return result


def returnTradeDay(this_day):
    """
    공휴일, 휴일이 아닌 거래일을 리턴함
    :param day:
    :return:
    """
    '''
    시간 체크도 해야함... 
    '''
    year = this_day[0:4]
    month = this_day[4:6]
    day = this_day[6:8]

    dt = datetime.datetime(int(year), int(month), int(day))
    isHoliday = xacom.holidayList(this_day)

    if isHoliday is True:
        if (dt.day - 1) == 0:
            # extraDay = [1, 3, 5, 7, 8, 10, 12]
            # normalDay = [4, 6, 9, 11]
            #
            # dt_month = dt.month - 1
            # if dt_month in extraDay:
            #     dt_day = 31
            # elif dt_month in normalDay:
            #     dt_day = 30
            # else:
            #     if dt.year % 4 == 0:
            #         dt_day = 29
            #     else:
            #         dt_day = 28
            #
            # temp_dt = datetime.datetime(int(year), dt_month, dt_day).strftime('%Y%m%d')
            temp_dt = (dt + datetime.timedelta(days=-1)).strftime('%Y%m%d')
            return temp_dt
        else:
            temp_dt = datetime.datetime(int(year), int(month), int(day) - 1).strftime('%Y%m%d')
            return returnTradeDay(temp_dt)
    elif dt.weekday() == 5:
        temp_dt = datetime.datetime(int(year), int(month), int(day) - 1).strftime('%Y%m%d')
        return returnTradeDay(temp_dt)
    elif dt.weekday() == 6:
        temp_dt = datetime.datetime(int(year), int(month), int(day) - 2).strftime('%Y%m%d')
        return returnTradeDay(temp_dt)
    else:
        return this_day


def isHolidayTrue(today):
    print(today)
    year = today[0:4]
    month = today[4:6]
    day = today[6:8]

    dt = datetime.datetime(int(year), int(month), int(day))

    if dt.weekday() == 5:
        if dt.hour in range(0, 9):
            return False
        else:
            return True
    elif dt.weekday() == 6:
        if dt.hour > 11:
            return True
    else:
        return False


def endTime(trCode, engine, start_time, result_len, log):
    """
    tr 수행 시간, 추가한 행 수를 저장하고 리턴함
    :param trCode:
    :param engine:
    :param start_time:
    :return:
    """
    date = closestTradeDay()
    nowtime = time.strftime('%Y%m%d%H%M%S', time.localtime(currentTime()))
    endtime = round(currentTime() - start_time, 2)
    # 데이터프레임이 2차원이므로, 리스트를 2개 중첩으로 구성한다
    result = [[date, nowtime, trCode, endtime, result_len]]

    resultCol = []

    appendCol(resultCol, 'date', 0)
    appendCol(resultCol, 'time', 1)
    appendCol(resultCol, 'trcode', 2)
    appendCol(resultCol, 'endtime', 3)
    appendCol(resultCol, 'result_len', 4)

    try:
        df = pd.DataFrame(result)
        df.columns = resultCol
        df.to_sql(name='trelapse', con=engine, if_exists='append', index=False)
        log.info('--- ' + str(endtime) + ' seconds')
    except Exception as e:
        log.error('error Occured when writing endTime, ' + str(e))
        log.info('--- ' + str(endtime) + ' seconds')


def message_info(msg):
    """
    공통 메세지 출력을 위함
    :param msg:
    :return:
    """
    pid = xasys.return_pid()
    print('---[p' + str(pid) + ' Info] ' + msg)


def timeSleepForNextTr():
    """
    다음 tr 실행을 위해 60초간 sleep
    :return:
    """
    print('---------------------------------------------------------------------')
    print('----- Sleep 60 secs before next Login start....')
    print('---------------------------------------------------------------------')

    sleepBeforeNextTr = False
    sleepIndex = 0

    while sleepBeforeNextTr is False:
        sleepIndex += 1
        print('.', end='')
        xasys.time_sleep(1)

        # 60초가 지나면 슬립을 풀도록 한다
        if sleepIndex >= 60:
            sleepBeforeNextTr = True
            print('')


def logger(name):
    """
    로그 생성 함수
    :param name:
    :return:
    """
    mylogger = logging.getLogger(name)
    mylogger.setLevel(logging.INFO)

    # 2020-04-26 16:42:11,416 [t8412 INFO]:p24561- 201Q5250 server start!!!
    formatter = logging.Formatter('%(asctime)s [%(name)s %(levelname)s]: %(message)s')

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    mylogger.addHandler(stream_handler)

    file_handler = logging.FileHandler('C:\\Log\\' + name + '.log')
    file_handler.setFormatter(formatter)
    mylogger.addHandler(file_handler)

    # mylogger.info("server start!!!")

    return mylogger


def additionalFutCode(codeType):
    """
    EUREX, CME 야간코드 추가
    :param codeType:
    :return:
    """

    dt = datetime.datetime.now()
    # year = this_day[0:4]
    # month = this_day[4:6]
    # day = this_day[6:8]

    additionalFutCodeList = []
    # 추가할 야간코드들 : EUREX 야간선물, CME USD선물
    # EUREX 야간선물 : 5, 6, 7, 8, 9, 10, 11...  7개 추가 (1개 여분으로 추가)
    # CME USD 선물: 21개 추가.. (1개 여분으로 추가)
    year = dt.year
    month = dt.month

    if codeType == 'EUREX':
        for i in range(0, 7):
            yyyy = str(year)
            mm = str(month)
            returnCode = xacom.retFutCode(yyyy, mm)

            futCode = '105' + returnCode + '000'
            additionalFutCodeList.append(futCode)

            if mm == '12':
                year = year + 1
                month = 1
            else:
                month = month + 1

    if codeType == 'CME':
        for i in range(1, 22):
            yyyy = str(year)
            mm = str(month)
            returnCode = xacom.retFutCode(yyyy, mm)

            futCode = '175' + returnCode + '000'
            additionalFutCodeList.append(futCode)

            if i in range(1, 12):
                if mm == '12':
                    year = year + 1
                    month = 1
                else:
                    month = month + 1

            # 12개월 이후부터는 3개월 단위 월물로 처리해줘야한다
            elif i == 12:
                if month in range(3, 6):
                    month = 6
                elif month in range(6, 9):
                    month = 9
                elif month in range(9, 12):
                    month = 12
                elif month in range(1, 3):
                    month = 3
            else:
                if month == 12:
                    year = year + 1
                    month = 3
                else:
                    month = month + 3
            # else:
            #     month = month + 1

            # print(futCode)

    return additionalFutCodeList


def currentTime():
    """
    현재 시각을 반환
    :return:
    """
    return time.time()

