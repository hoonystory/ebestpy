import multiprocessing
import pandas as pd
import src.utils.calendar

import xacom
import funcs


# db_name = 'eBestDB'
# git test

if __name__ == '__main__':
    multiprocessing.freeze_support()

    hour = funcs.todayHour()
    today = funcs.todayDate()

    closestTradeDay = funcs.closestTradeDay()
    # closestTradeDay = funcs.returnDate(1)
    # print(closestTradeDay)
    isHoliday = xacom.holidayList(closestTradeDay)

    sdate = ''
    edate = ''
    tday = ''
    yyyymm = ''

    # 현재 시간을 가져와서, 어느 시간대(주간/야간) 데이터를 수집할 것인지를 판단함
    dayOfWeek = funcs.todayOfWeek()

    weekday_dayStrtHour = 15
    weekday_dayEndHour = 4
    weekday_dayList = list(range(0, 5))

    weekday_nightStrtHour = list(range(5, 12))
    weekday_nightList = list(range(1, 6))

    # code 초기화 tr 리스트
    trForSetting_0 = ["t8424", "t8430"]
    trForSetting_1 = ["t9943", "t9944"]

    shcode = []
    focode = []
    opcode = []
    fucode = []
    upcode = []
    cmecode = []

    procs = []
    procs_tr = []

    # 정기(주간) 데이터 저장
    # trList_0 = ["t8412", "t2405", "t8414", "t8415"]

    trList_0 = ["t1485", "t1511"]
    trList_1 = ["t1603", "t1662"]
    trList_2 = ["t2301", "t8428"]
    trList_3 = ["t2201", "t8418"]
    trList_4 = ["t1926", "t1927"]
    trList_5 = ["t3202", "t2405"]
    trList_6 = ["t8412", "t8414", "t8415"]
    trList_7 = []
    # if closestTradeDay == "20200813":
    #     trList_5.append("t2203")
    # 정기(야간) 데이터 저장
    # trList_N0 = ["t2833"]
    trList_N0 = ["t2813", "t8408"]
    trList_N1 = ["t8409", "t2835"]
    trList_N2 = ["t8429", "t2832"]
    # t3518 t2804
    trList_N3 = ["t3518", "t2804"]
    trList_N4 = []
    # if closestTradeDay == "20200812":
    #     tempList = ["t2833"]
    #     trList_N2 = trList_N2 + tempList
    # 비정기 데이터 저장
    trList_NR0 = ['t2805', 't2814', 't2833']
    trList_NR1 = ['t2203', 't8413', 't8416']
    # 공휴일 데이터 저장
    trList_H0 = ["t3518"]

    trListAll = []
    trForSettingAll = []
    trForSettingAll.append(trForSetting_0)
    trForSettingAll.append(trForSetting_1)

    if xacom.expirationList(closestTradeDay):
        trList_7.append("t2203")
    if xacom.expirationList(funcs.returnDate(0)):
        trList_N4.append("t2833")

    # manager = multiprocessing.Manager()
    # return_list = manager.list([0 for x in range(1)])
    # print(return_list)

    log = funcs.logger('main')
    log.info('today: ' + today)
    log.info('closest trade day: ' + closestTradeDay)

    try:
        engine = funcs.dbLogin(log)
    except Exception as e:
        log.error('error Occurred when logging database: ', str(e))

    if isHoliday is False:
        for trList in trForSettingAll:
            is_done = False
            while is_done is not True:
                if len(trList) == 0:
                    is_done = True
                else:
                    for item in trList:
                        trFunc = xacom.parseTrFunction(item)

                        proc = multiprocessing.Process(target=trFunc, args=( ))
                        procs.append(proc)
                        procs_tr.append(item)
                        proc.start()

                    for proc in range(len(procs)):
                        procs[proc].join()
                        is_done = True
                        # 현재 프로세스 상태를 출력
                        print(procs[proc])
                        print('---------------------------------------------------------------------')
                        log.info('trCode: '+ procs_tr[proc] + ' Done')
                        print('---------------------------------------------------------------------')
                        # 다음 로그인을 위한 60초 sleep
                        funcs.timeSleepForNextTr()
    else:
        log.info('today is holiday! now terminate multiprocs for codelist')

    # 코드 정보 세팅: 휴장일인 경우, t3518(해외지수)만 작동하고, 해외지수는 코드리스트 업데이트 필요없음
    if isHoliday is False:
        try:
            upcode = pd.read_sql(sql='select distinct * from t8424outblock', con=engine).upcode.tolist()
            shcode = pd.read_sql(sql='select distinct * from t8430outblock', con=engine).shcode.tolist()
            fucode = pd.read_sql(sql='select distinct * from t9943outblock', con=engine).shcode.tolist()
            opcode = pd.read_sql(sql='select distinct * from t9944outblock', con=engine).shcode.tolist()
            cmecode = pd.read_sql(sql="select * from t9943outblock where shcode like '101%%'", con=engine).shcode.tolist()

            focode = focode + fucode + opcode
        except Exception as e:
            log.error('error Occured when reading codelist, ' + str(e))

        sdate = closestTradeDay
        edate = closestTradeDay
        tday = closestTradeDay
        yyyymm = funcs.todayMonth()

        # 다음 로그인을 위한 60초 sleep
        funcs.timeSleepForNextTr()

    # 선물코드는 fucode, 옵션코드는 opcode, 선물옵션코드는 focode로 명명
    # focode는 fucode, opcode 리스트를 서로 합쳐서 만든다.

    # trList 가져옴
    """
    trList = [ "t1485", "t1511", "t1603", "t1662", "t1926", "t1927"
            , "t2201", "t2301", "t2405"
            , "t2804", "t2805", "t2813", "t2832", "t2833", "t2835"
            , "t3202", "t3518", "t8428"
            , "t8409", "t8412", "t8414", "t8415", "t8417", "t8418", "t8429"]
    
    ## 총 23개 tr 
    """
    # 공휴일이 아닌 경우
    if isHoliday is False:
        # 월요일(0)~ 금요일(4), 오후 16시 이후에는 주간데이터, (혹은 에러로 인해 야간에 실행해야하는 경우),
        if (hour > weekday_dayStrtHour and dayOfWeek in weekday_dayList) or (hour < weekday_dayEndHour and dayOfWeek in weekday_nightList):
            trListAll.append(trList_0)
            trListAll.append(trList_1)
            trListAll.append(trList_2)
            trListAll.append(trList_3)
            trListAll.append(trList_4)
            trListAll.append(trList_5)
            trListAll.append(trList_6)
            # 만기인 경우에만 리스트에 아이템이 추가되므로,
            if len(trList_7) > 0:
                trListAll.append(trList_7)

        # 화요일(1)~ 토요일(5), 오전 5시 부터 12시 전까지는 야간데이터
        elif hour in weekday_nightStrtHour and dayOfWeek in weekday_nightList:
            # 야간 EUREX 선물, CME USD 종목코드 데이터를 추가해준다
            addCmeCode = funcs.additionalFutCode('CME')
            addEurexCode = funcs.additionalFutCode('EUREX')

            cmecode = cmecode + addCmeCode
            opcode = opcode + addEurexCode

            trListAll.append(trList_N0)
            trListAll.append(trList_N1)
            trListAll.append(trList_N2)
            trListAll.append(trList_N3)
            if len(trList_N4) > 0:
                trListAll.append(trList_N4)

    # 공휴일인 경우
    # 화요일(1)~ 토요일(5), 오전 5시 부터 12시 전까지, 공휴일인 경우 데이터
    elif isHoliday is True:
        if hour in weekday_nightStrtHour and dayOfWeek in weekday_nightList:
            trListAll.append(trList_H0)

    # trListAll가 0이 아닌 경우에만 실행
    if len(trListAll) != 0:
        for trList in trListAll:
            is_done = False
            def_list = []
            while is_done is not True:
                # trList에 있는 항목대로 함수, 매개변수 리스트 append 해줌
                if len(trList) == 0:
                    is_done = True
                else:
                    for item in trList:
                        oneTr = []
                        oneTr.append(xacom.parseTrFunction(item))
                        oneTr.append(xacom.parseTrArgsList(item))

                        # def_list에 세팅된 tr을 append
                        def_list.append(oneTr)

                    # 멀티프로세스 조인리스트
                    procs = []

                    for index in def_list:
                        # 여기서 프로세스 태우기 전에,
                        # arg를 세팅하여 보내주는 것이 맞는 흐름으로 보인다
                        args = []
                        for arg in index[1]:
                            if arg == "shcode":
                                args.append(shcode)
                            if arg == "fucode":
                                args.append(fucode)
                            if arg == "focode":
                                args.append(focode)
                            if arg == "opcode":
                                args.append(opcode)
                            if arg == "upcode":
                                args.append(upcode)
                            if arg == "cmecode":
                                args.append(cmecode)
                            if arg == "sdate":
                                args.append(sdate)
                            if arg == "edate":
                                args.append(edate)
                            if arg == "yyyymm":
                                args.append(yyyymm)
                            if arg == "tday":
                                args.append(tday)

                        proc = multiprocessing.Process(target=index[0], args=(args))
                        procs.append(proc)
                        proc.start()

                    for proc in range(len(procs)):
                        procs[proc].join()
                        print(procs[proc])
                        is_done = True
                        print('---------------------------------------------------------------------')
                        log.info('trCode: ' + trList[proc] + ' Done')
                        print('---------------------------------------------------------------------')

                        # 다음 로그인을 위한 60초 sleep
                        funcs.timeSleepForNextTr()

    else:
        log.error('trList None')

    log.info('main End: ' + today)

