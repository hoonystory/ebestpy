import requests
from src.constant import request
from src.utils.log import log
from config import login


class Login:
    """
    eBest login process
    app_key:
    secret_key:
    access_token:
    """
    response = None
    access_token = None
    expires_in = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):         # Foo 클래스 객체에 _instance 속성이 없다면
            log.debug("__new__ is called\n")
            cls._instance = super().__new__(cls)  # Foo 클래스의 객체를 생성하고 Foo._instance로 바인딩
        return cls._instance                      # Foo._instance를 리턴

    def __init__(self):
        cls = type(self)
        if not hasattr(cls, "_init"):             # Foo 클래스 객체에 _init 속성이 없다면
            log.debug("__init__ is called\n")
            self.app_key = login.app_key
            self.secret_key = login.secret_key
            self.url = request.hostname + request.login
            self.init()
            cls._init = True
        # pass

    def init(self):
        self.response = requests.post(
            url=self.url,
            data={
                'appkey': self.app_key
                , 'appsecretkey': self.secret_key
                , 'grant_type': 'client_credentials'
                , 'scope': 'oob'
            },
            headers={
                'content-type': 'application/x-www-form-urlencoded'
            }
        )
        if self.response.status_code == 200:
            self.access_token = self.response.json().get('access_token')
            self.expires_in = self.response.json().get('expires_in')
        else:
            pass

        log.debug('init login')
        log.info('access_token: ' + self.access_token)
        log.info('expires_in: ' + str(self.expires_in))
