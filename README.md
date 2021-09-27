# weather_forecast_tenkijp

### 指定した都市につき、tenki.jpの天気予報をLINE Messaging APIによりLine botとして通知する

- AWS Lambda で定期実行するように対応　（毎日 JST:6時10分に実行）  
- トリガーは、EventBridge (CloudWatch Events)で設定  
- ログは、Amazon SNS により、Cloud Trail Logs へ送信  

※※本来はスクレイピングではなく、APIが存在すればAPIを利用すべきです※※
　

### 使用技術：
- Python 3.8
- AWS
  - Lambda
  - EventBridge
  - SNS
  - CloudTrailLogs

　

### 執筆記事：AWS Lambdaで天気予報を毎朝LINEへ通知してみた【Python】

<a href="https://qiita.com/_whitecat_22/items/479659e59af0a3bc731c">
 <img src="https://github.com/whitecat-22/weather_forecast_tenkijp/blob/main/qiita.png">
</a>

　
 
- LINEへの通知結果

![https://github.com/whitecat-22/weather_forecast_tenkijp/blob/main/weather_forecast_tenkijp.PNG](https://github.com/whitecat-22/weather_forecast_tenkijp/blob/main/weather_forecast_tenkijp.PNG)
