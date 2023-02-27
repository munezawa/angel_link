import time
import json
import requests
import urllib3
import msgpack
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {
  "http": "http://127.0.0.1:7890",
  "https": "http://127.0.0.1:7890",
  "ftp": "ftp://127.0.0.1:7890"
}
headers = {
    'host': r"ancl.jp",
    'accept': r'*/*',
    'accept-encoding': 'gzip, deflate, br',
    'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    # 虽然我浏览器的默认语言是英语
    'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    # 原来`是转义字符的意思
    'sec-ch-ua': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': r'Windows',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'Origin':'https://ancl.jp',
    # 'Referer': r'https://ancl.jp/game/pc/start/1/43451822/HyknBer5NLe7lqnEuqB5tjnNatGGhO716xounMeGH1QepxYt9i476dkTt6g95urL5pxQBSONYyiid7kUM1YMbj5Hxn2Yw8hO/'
}
def post_msgpackstring(msgpackstring, token, count=0):
    url = r'https://ancl.jp/game/api/v1/'
    if(count >= 10):
        raise Exception("post_msgpackstring_fall")
    try:
        time.sleep(0.5)
        headers['Authorization'] = "Bearer "+token
        # Referer 请求头包含了当前请求页面的来源页面的地址，即表示当前页面是通过此来源页面里的链接进入的。
        headers['Content-Type'] = r'application/x-msgpack'
        r = requests.post(url, headers=headers, verify=False, proxies=proxies, data=msgpackstring)
        if(r.status_code == 200):
            body = msgpack.unpackb(r.content, strict_map_key=False)
            # 注意这里返回的是字典
            return body
        elif(r.status_code == 401):
            # badrequst错误 和认证无效错误 立刻停止尝试产生异常
            count = 10
            print('post_msgpackstring error:', end=" ")
            print(r.status_code, url)
            raise Exception("訪問失敗")
        elif(r.status_code == 400):
            # badrequst错误 和认证无效错误 立刻停止尝试产生异常
            count = 10
            print('post_msgpackstring error:', end=" ")
            print(r.status_code, url)
            raise Exception("訪問失敗")
        else:
            print('post_msgpackstring error:', end=" ")
            print(r.status_code, url)
            raise Exception("訪問失敗")
    except Exception:
        time.sleep(3)
        print('post_msgpackstring again:', headers['X-Class'], headers['X-Func'])
        # 除了cookies加不进的错误忽略之外 其他情况下应该都会重新登陆吧
        return post_msgpackstring(msgpackstring, token, count=count+1)


def post_req(X_Class, X_Func, Parameter, token):
    headers['X-Class'] = X_Class
    headers['X-Func'] = X_Func
    msgpackstring = msgpack.packb(Parameter)
    return post_msgpackstring(msgpackstring, token)

# event = 'EVE40'
# headers['X-Class'] = 'BattleEvent'
# headers['X-Func'] = 'getProgress'
# a = {'params': {'event_id': 'EVE46'}}
# b = post_msgpackstring(msgpack.packb(a), 
#                        "M2i1khCVlDBpukqUzBsUiufJ9P1kDyc4cLtKzohsfnBZxF3xkgNzkxBsQwsvTwfsBoYosrmkClgdagVyVPTsnoBvdqvf56mj")
# print(b['error']==None)
# with open('.\info.txt',"w") as f:
#     f.write(str(b))

# mission_info = post_req('Mission', 'getStatusDaily', {'params': {}}, "Gpb7O1tmrLejoWm960QN1REiIWWOwbaPafrY9Yl9Vhly6fiWekoIB964PA2djE6Kf6Zon1myicDuPKpCBAEp3nWgkz4O4pGE")
# cleared_mission_list = []
# for i in mission_info['result']['mission']:
#     if(mission_info['result']['mission'][i]['clear'] == True and mission_info['result']['mission'][i]['receive'] == False):
#         cleared_mission_list.append(i[1:])
# print(cleared_mission_list, "are cleared missions")
# if(len(cleared_mission_list) <= 0):
#     print("no mission cleared")
#     exit(0)
# data = {'params': {'mission': []}}
# data['params']['mission'] = cleared_mission_list
# print(data)
# reward_info = post_req('Mission', 'execClearDaily', data, "Gpb7O1tmrLejoWm960QN1REiIWWOwbaPafrY9Yl9Vhly6fiWekoIB964PA2djE6Kf6Zon1myicDuPKpCBAEp3nWgkz4O4pGE")
# try:
#     print(reward_info['result']['reward'], "mission rewards received")
# except Exception:
#     print("unknow error cause mission reward receive fail")
# exit(0)