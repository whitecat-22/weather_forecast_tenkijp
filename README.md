# weather_forecast_tenkijp

### tenki.jpの天気予報（東京都港区）をLINE Messaging APIによりLine botとして通知する

AWS Lambda で定期実行するように対応　（JST:6時15分に実行）  
トリガーは、EventBridge (CloudWatch Events)で設定  
ログは、Amazon SNS により、Cloud Trail Logs へ送信  

　
 
![https://github.com/whitecat-22/weather_forecast_tenkijp/blob/main/weather_forecast_tenkijp.PNG](https://github.com/whitecat-22/weather_forecast_tenkijp/blob/main/weather_forecast_tenkijp.PNG)
