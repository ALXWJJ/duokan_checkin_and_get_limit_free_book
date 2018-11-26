import time
from pprint import pprint

import requests


class DuoKan:
    URL = 'https://www.duokan.com'

    device_id = '这里是你的 Device_id'
    headers = {
        'Accept-Encoding': 'gzip,deflate',
        'Cookie': '这里是你的 Cookie',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1; MX5 Build/LMY47I)',
    }

    def __init__(self):
        self.session = requests.Session()

    def get_csrf_params(self):
        time_sec = int(time.time())
        list_of_str = list(self.device_id+'&'+str(time_sec))
        i = 0
        csrf_code = 0
        while i < len(list_of_str):
            csrf_code = (csrf_code * 131 + ord(list_of_str[i])) % 65536
            i += 1
        param = {'_t': time_sec, '_c': csrf_code}
        return param

    def check_in(self):
        r = self.session.post(
            self.URL + "/checkin/v0/checkin", data=self.get_csrf_params(), headers=self.headers)
        print(r.json()['msg'])

    def get_free(self):
        r = self.session.get(
            self.URL+'/hs/v4/channel/query/403', headers=self.headers)
        bookid = r.json()["items"][0]["data"]["data"][0]["data"]["book_id"]

        param = {
            'payment_name': 'BC',
            'ch': 'VSZUVB',
            'book_id': bookid,
            'price': 0,
            'allow_discount': 1
        }
        param.update(self.get_csrf_params())

        r = self.session.post(
            self.URL+'/store/v0/payment/book/create', data=param, headers=self.headers)
        print(r.json()['book']['title']+'    '+r.json()['msg'])

    def test(self):
        r = self.session.get(
            self.URL+'/hs/v4/channel/query/403', headers=self.headers)
        pprint(r.json()["items"][0]["data"]["data"][0]["data"]["book_id"])


if __name__ == "__main__":
    my_duokan = DuoKan()
    # my_duokan.test()
    my_duokan.check_in()  # 签到
    my_duokan.get_free()  # 获得每日限免书
