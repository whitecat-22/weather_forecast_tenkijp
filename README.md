# weather_forecast_tenkijp

### 指定した都市につき、[tenki.jp](https://tenki.jp/)の天気予報をLine botとして通知する


### ◆処理内容：
- AWS Lambda で定期実行するように対応　（毎日 JST:6時10分に実行、6時00分時点の予報を通知）  
- トリガーは、EventBridge (CloudWatch Events)で設定  
- [LINE Messaging API](https://developers.line.biz/ja/services/messaging-api/)により、LINEへ通知  
- ログは、Amazon SNS により、Cloud Trail Logs へ送信  

**※※本来はスクレイピングではなく、APIが存在すればAPIを利用すべきです※※**

　

### ◆使用技術：
- [Python](https://www.python.org/) 3.8
- AWS
  - [Lambda](https://aws.amazon.com/jp/lambda/?nc2=h_ql_prod_serv_lbd)
  - [EventBridge](https://aws.amazon.com/jp/eventbridge/?nc2=h_ql_prod_serv_eb)
  - [SNS](https://aws.amazon.com/jp/sns/?nc2=h_ql_prod_serv_sns&whats-new-cards.sort-by=item.additionalFields.postDateTime&whats-new-cards.sort-order=desc)
  - [CloudTrailLogs](https://aws.amazon.com/jp/cloudtrail/?nc2=h_ql_prod_mg_ct)

　

### ◆執筆記事：[AWS Lambdaで天気予報を毎朝LINEへ通知してみた【Python】](https://qiita.com/_whitecat_22/items/479659e59af0a3bc731c)

<a href="https://qiita.com/_whitecat_22/items/479659e59af0a3bc731c">
 <img src="https://github.com/whitecat-22/weather_forecast_tenkijp/blob/main/qiita.png">
</a>

　
 
- LINEへの通知結果

![https://github.com/whitecat-22/weather_forecast_tenkijp/blob/main/weather_forecast_tenkijp.PNG](https://github.com/whitecat-22/weather_forecast_tenkijp/blob/main/weather_forecast_tenkijp.PNG)
