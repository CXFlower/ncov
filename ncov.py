import json
import os
import time
from json import JSONDecodeError

import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_overall_informaiton():
    session = requests.session()
    session.keep_alive = False

    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
    }
    session.headers.update(headers)

    try:
        r = session.get(url='https://ncov.dxy.cn/ncovh5/view/pneumonia')
    except (requests.exceptions.ChunkedEncodingError, requests.exceptions.ProxyError) as err:
        print(err.__str__())
        return None
    soup = BeautifulSoup(r.content, "html.parser")

    # overall_information = re.search(r'\{("id".*?)\}', str(soup.find('script', attrs={'id': 'getStatisticsService'})))
    overall_information = str(soup.find('script', attrs={'id': 'getStatisticsService'}))
    if overall_information != "":
        start_idx = overall_information.find('{"id":')
        end_idx = overall_information.rfind('}catch(e){}')
        if start_idx != -1 and end_idx != -1:
            overall_information = overall_information[start_idx:end_idx]
            return overall_information
        else:
            return None
    return None


def overall_parser(overall_information):
    if overall_information is None:
        return None
    try:
        overall_information = json.loads(overall_information)
        overall_information['updateTime'] = overall_information['modifyTime']
        overall_information['countRemark'] = overall_information['countRemark'].replace(' 疑似', '，疑似').replace(' 治愈', '，治愈').replace(' 死亡', '，死亡').replace(' ', '')
        overall_information['recordTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        new_information = {"infectSource": overall_information["infectSource"],
                           "passWay": overall_information["passWay"], "dailyPic": overall_information["dailyPic"],
                           "summary": overall_information["summary"], "countRemark": overall_information["countRemark"],
                           "confirmedCount": overall_information["confirmedCount"],
                           "suspectedCount": overall_information["suspectedCount"],
                           "curedCount": overall_information["curedCount"],
                           "deadCount": overall_information["deadCount"], "virus": overall_information["virus"],
                           "remark1": overall_information["remark1"], "remark2": overall_information["remark2"],
                           "remark3": overall_information["remark3"], "remark4": overall_information["remark4"],
                           "remark5": overall_information["remark5"],
                           "generalRemark": overall_information["generalRemark"],
                           "abroadRemark": overall_information["abroadRemark"],
                           "updateTime": overall_information["updateTime"],
                           "recordTime": overall_information["recordTime"]}
        return new_information
    except JSONDecodeError as jerr:
        print("获取到错误数据！")
        print("错误数据为：", end="")
        print(type(overall_information))
        print(overall_information)
        print(jerr.__str__())
        return None


if __name__ == '__main__':
    print("疫情实时数据采集器启动，半小时进行采集一次！")
    header = True
    sum = 0
    while True:
        now_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        if now_time_str.find(":30:00") != -1 or now_time_str.find(":00:00") != -1:
        # if True:
            overall_information = get_overall_informaiton()
            overall_information = overall_parser(overall_information)
            if overall_information is None:
                continue
            df = pd.DataFrame.from_dict(overall_information, orient='index', dtype=None, columns=None)
            df = df.transpose()
            file_path = 'DXYOverall.csv'
            if os.path.exists(file_path):
                header = False
            else:
                header = True
            df.to_csv(
                path_or_buf=file_path,
                header=header,
                index=False, encoding='utf_8_sig',
                mode="a"
            )
            sum = sum + 1
            print(now_time_str + " 完成一次采集！数据量：" + str(sum))
        time.sleep(0.9)
print()

