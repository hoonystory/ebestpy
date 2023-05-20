
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

