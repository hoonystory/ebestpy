import requests
from config import url
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

    def __init__(self):
        self.app_key = login.app_key
        self.secret_key = login.secret_key
        self.url = url.ebest.get('common') + url.ebest.get('login')
        # pass

    def init(self):
        self.response = self.get_access_token_by_request()
        if self.response.status_code == 200:
            self.access_token = self.response.json().get('access_token')
            self.expires_in = self.response.json().get('expires_in')

        print('access_token:', self.access_token)
        print('expires_in:', self.expires_in)
        # print(r)
        # print(r.status_code)
        # print(r.request)
        # print(r.raise_for_status())
        # print(r.json())
        # pass

    def get_access_token_by_request(self):
        params = {
            'appkey': self.app_key
            , 'appsecretkey': self.secret_key
            , 'grant_type': 'client_credentials'
            , 'scope': 'oob'
        }
        headers = {
            'content-type': 'application/x-www-form-urlencoded'
        }
        return requests.post(url=self.url, data=params, headers=headers)
