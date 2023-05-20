
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