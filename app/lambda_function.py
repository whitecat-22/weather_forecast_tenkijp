"""
lambda_function.py
"""
# postリクエストをline notify APIに送るためにrequestsのimport
import os
import time
import requests
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime, timezone
import pytz

url = "https://tenki.jp/forecast/3/16/4410/13103/"  # 東京都港区

# line notify APIのトークン
line_notify_token = os.getenv("LINE_NOTIFY_TOKEN")
# line notify APIのエンドポイントの設定
line_notify_api = 'https://notify-api.line.me/api/notify'


def move_bin(
    fname: str, src_dir: str = "/var/task/bin", dest_dir: str = "/tmp/bin"
) -> None:
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    dest_file = os.path.join(dest_dir, fname)
    shutil.copy2(os.path.join(src_dir, fname), dest_file)
    os.chmod(dest_file, 0o775)


def create_driver(
    options: webdriver.chrome.options.Options,
) -> webdriver.chrome.webdriver:
    driver = webdriver.Chrome(
        executable_path="/tmp/bin/chromedriver", chrome_options=options
    )
    return driver


def lambda_handler(event, context):
    """
    lambda_handler
    """
    print('event: {}'.format(event))
    print('context: {}'.format(context))

    move_bin("headless-chromium")
    move_bin("chromedriver")

    #headless_chromium = os.getenv('HEADLESS_CHROMIUM', '')
    #chromedriver = os.getenv('CHROMEDRIVER', '')
    # webdriverの設定
    options = Options()
    #options.binary_location = headless_chromium
    options.binary_location = "/tmp/bin/headless-chromium"
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--single-process')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280x1696")
    options.add_argument("--disable-application-cache")
    options.add_argument("--disable-infobars")
    options.add_argument("--hide-scrollbars")
    options.add_argument("--enable-logging")
    options.add_argument("--log-level=0")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--homedir=/tmp")

    driver = create_driver(options)
    # driver = webdriver.Chrome(executable_path=chromedriver, options=options)

    # 現在時刻
    now = datetime.now(tz=timezone.utc)
    tokyo = pytz.timezone('Asia/Tokyo')
    # 東京のローカル時間に変換
    jst_now = tokyo.normalize(now.astimezone(tokyo))
    content0 = jst_now.strftime("%m月%d日 %H:%M現在")

    content = []
    driver.get(url)
    time.sleep(1)
    content1 = driver.find_element_by_xpath("//section/h2")
    content2 = driver.find_element_by_css_selector(
        "#main-column > section > div.forecast-days-wrap.clearfix > section.today-weather > div.weather-wrap.clearfix > div.weather-icon > p")
    content3 = driver.find_element_by_css_selector(
        "#main-column > section > div.forecast-days-wrap.clearfix > section.today-weather > div.weather-wrap.clearfix > div.date-value-wrap > dl > dd.high-temp.temp > span.value")
    content4 = driver.find_element_by_css_selector(
        "#main-column > section > div.forecast-days-wrap.clearfix > section.today-weather > div.weather-wrap.clearfix > div.date-value-wrap > dl > dd.low-temp.temp > span.value")

    # lineに通知するメッセージを組み立て
    content_text = []
    content_text.append("●" + content1.text + '\n' + "今日の天気は" + content2.text +
                                  "、最高気温は{}℃".format(content3.text) + "、最低気温は{}℃です。".format(content4.text))

    notification_message = content0 + '\n' + '\n\n'.join(content_text)

    driver.close()
    driver.quit()

    # ヘッダーの指定
    headers = {'Authorization': f'Bearer {line_notify_token}'}
    # 送信するデータの指定
    data = {'message': f'{notification_message}'}
    # line notify apiにpostリクエストを送る
    requests.post(line_notify_api, headers=headers, data=data)

    return {
        'status_code': 200
    }


if __name__ == "__main__":
    print(lambda_handler(event=None, context=None))
