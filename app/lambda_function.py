"""
lambda_function.py
"""
# postリクエストをline notify APIに送るためにrequestsのimport
import os
import time
from datetime import datetime, timezone
import pytz
import re
import requests
from bs4 import BeautifulSoup
import json

url = "https://tenki.jp/forecast/3/16/4410/13103/"  # 東京都港区

# line notify APIのトークン
line_notify_token = os.getenv("LINE_NOTIFY_TOKEN")
# line notify APIのエンドポイントの設定
line_notify_api = 'https://notify-api.line.me/api/notify'


def lambda_handler(event, context):
    """
    lambda_handler
    """
    print('event: {}'.format(event))
    print('context: {}'.format(context))

    # 現在時刻
    now = datetime.now(tz=timezone.utc)
    tokyo = pytz.timezone('Asia/Tokyo')
    # 東京のローカル時間に変換
    jst_now = tokyo.normalize(now.astimezone(tokyo))
    content0 = jst_now.strftime("%m月%d日 %H:%M現在")

    # bs4でパース
    r = requests.get(url)
    html = r.text.encode(r.encoding)
    soup = BeautifulSoup(html, 'html.parser')

    dict = {}

    # lineに通知するメッセージを組み立て
    content_text = []

    # 予測地点
    l_pattern = r"(.+)の今日明日の天気"
    l_src = soup.title.text
    dict['location'] = re.findall(l_pattern, l_src)[0]
    content00 = "●" + dict['location'] + "の天気"
    print(content00)
    content_text.append(content00)

    soup_tdy = soup.select('.today-weather')[0]

    soup_tmr = soup.select('.tomorrow-weather')[0]


    # 今日の天気
    dict["today"] = forecast2dict(soup_tdy)

    info = dict["today"]["forecasts"]

    content1 = "=====" + dict["today"]["date"] + "=====" + "\n" + "天    気： " + info["weather"] + "\n" + "最高気温： " + info["high_temp"] + info["high_temp_diff"] + "\n" + "最低気温： " + info["low_temp"] + info["low_temp_diff"] + "\n" + "降水確率: " + "\n" + "[00-06]： " + info["rain_probability"]['00-06'] + \
        "\n" + "[06-12]： " + info["rain_probability"]['06-12'] + "\n" + "[12-18]： " + info["rain_probability"]['12-18'] + \
        "\n" + "[18-24]： " + info["rain_probability"]['18-24'] + \
        "\n" + "風    向： " + info["wind_wave"]

    print(content1)
    content_text.append(content1)

    # 明日の天気
    dict["tomorrow"] = forecast2dict(soup_tmr)

    info = dict["tomorrow"]["forecasts"]

    content2 = "=====" + dict["tomorrow"]["date"] + "=====" + "\n" + "天    気： " + info["weather"] + "\n" + "最高気温： " + info["high_temp"] + info["high_temp_diff"] + "\n" + "最低気温： " + info["low_temp"] + info["low_temp_diff"] + "\n" + "降水確率: " + "\n" + "[00-06]： " + info["rain_probability"]['00-06'] + \
        "\n" + "[06-12]： " + info["rain_probability"]['06-12'] + "\n" + "[12-18]： " + info["rain_probability"]['12-18'] + \
        "\n" + "[18-24]： " + info["rain_probability"]['18-24'] + \
        "\n" + "風    向： " + info["wind_wave"]

    print(content2)
    content_text.append(content2)

    notification_message = content0 + "\n" + "\n\n".join(content_text)

    # ヘッダーの指定
    headers = {'Authorization': f'Bearer {line_notify_token}'}
    # 送信するデータの指定
    data = {'message': f'{notification_message}'}
    # line notify apiにpostリクエストを送る
    requests.post(line_notify_api, headers=headers, data=data)

    return {
        'status_code': 200
    }


def forecast2dict(soup):
    data = {}

    # 日付処理
    d_pattern = r"(\d+)月(\d+)日\(([土日月火水木金])+\)"
    d_src = soup.select('.left-style')
    date = re.findall(d_pattern, d_src[0].text)[0]
    data["date"] = "%s/%s(%s)" % (date[0], date[1], date[2])
    #print("=====" + data["date"] + "=====")

    # ## 取得
    weather = soup.select('.weather-telop')[0]
    high_temp = soup.select("[class='high-temp temp']")[0]
    high_temp_diff = soup.select("[class='high-temp tempdiff']")[0]
    low_temp = soup.select("[class='low-temp temp']")[0]
    low_temp_diff = soup.select("[class='low-temp tempdiff']")[0]
    rain_probability = soup.select('.rain-probability > td')
    wind_wave = soup.select('.wind-wave > td')[0]

    # ## 格納
    forecast = {}
    forecast["weather"] = weather.text.strip()
    forecast["high_temp"] = high_temp.text.strip()
    forecast["high_temp_diff"] = high_temp_diff.text.strip()
    forecast["low_temp"] = low_temp.text.strip()
    forecast["low_temp_diff"] = low_temp_diff.text.strip()
    every_6h = {}
    for i in range(4):
        time_from = 0+6*i
        time_to = 6+6*i
        itr = '{:02}-{:02}'.format(time_from, time_to)
        every_6h[itr] = rain_probability[i].text.strip()
    forecast["rain_probability"] = every_6h
    forecast["wind_wave"] = wind_wave.text.strip()

    data["forecasts"] = forecast

    return data

if __name__ == "__main__":
    print(lambda_handler(event=None, context=None))
