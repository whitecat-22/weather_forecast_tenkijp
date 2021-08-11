# weather_forecast_tenkijp

### tenki.jpの天気予報（東京都港区）をLINE Messaging APIによりLine botとして通知する

AWS Lambda で定期実行するように対応　（JST:6時15分に実行）  
トリガーは、EventBridge (CloudWatch Events)で設定  
ログは、Amazon SNS により、Cloud Trail Logs へ送信  

### 執筆記事：AWS Lambdaで天気予報を毎朝LINEへ通知してみた【Python】

<a href="https://qiita.com/_whitecat_22/items/479659e59af0a3bc731c">
 <img src="">
</a>

　
 
![https://github.com/whitecat-22/weather_forecast_tenkijp/blob/main/weather_forecast_tenkijp.PNG](https://github.com/whitecat-22/weather_forecast_tenkijp/blob/main/weather_forecast_tenkijp.PNG)
