import json
from datetime import date, timedelta
from urllib.request import urlopen
from urllib.parse import urlencode, unquote, quote_plus
import urllib

apiURL = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
    
def GetWeatherData(baseDate, time, nx, ny):
    with open('secrets.json') as f:
        jsonData = json.load(f)
        weatherAPIKey = jsonData["weatherAPIKey"]

    params = '?' + urlencode({
        quote_plus("serviceKey"):weatherAPIKey,
        quote_plus("numOfRows"):600,
        quote_plus("pageNo"):1,
        quote_plus("dataType"):"JSON",
        quote_plus("base_date"):baseDate,
        quote_plus("base_time"):time,
        quote_plus("nx"):nx,
        quote_plus("ny"):ny,  
    })
    req = urllib.request.Request(apiURL + unquote(params))
    body = urlopen(req).read()
    jsonData = json.loads(body)
    return jsonData["response"]

def RainTypeToString(type):
    if type == -1:
        return "Error"
    if type == 1:
        return "비가"
    if type == 2:
        return "비나 눈이"
    if type == 3:
        return "눈이"
    if type == 4:
        return "소나기가"
    return "없음"

def GetWeatherBriefing(when, nx = 62, ny = 120): # when = 1 오늘 2 내일
    today = date.today().strftime('%Y%m%d')
    yesterday = (date.today() - timedelta(1)).strftime('%Y%m%d')
    tomorrow = (date.today() + timedelta(1)).strftime('%Y%m%d')

    response = GetWeatherData(today,"0200",nx,ny)
    resultCode = response["header"]["resultCode"]

    if resultCode != "00":
        response = GetWeatherData(yesterday,"2300",nx,ny)

    resultCode = response["header"]["resultCode"]
    if resultCode != "00":
        print("Error")
        exit()

    infoList = response["body"]["items"]["item"]
    todayTMN = todayTMX = tomoTMN = tomoTMX = 0
    todayRainPercent = tomoRainPercent = 0
    todayRainTime = tomoRainTime = ""
    todayRainType = tomoRainType = -1
    for info in infoList:
        category = info["category"]
        fcstDate = info["fcstDate"]
        val = info["fcstValue"]
        if category == "TMN" and fcstDate == today:
            todayTMN = val
        elif category == "TMN" and fcstDate == tomorrow:
            tomoTMN = val
        elif category == "TMX" and fcstDate == today:
            todayTMX = val
        elif category == "TMX" and fcstDate == tomorrow:
            tomoTMX = val
        elif category == "POP" and fcstDate == today:
            if int(val) > todayRainPercent:
                todayRainPercent = int(val)
                todayRainTime = info["fcstTime"]
        elif category == "PTY" and fcstDate == today:
            todayRainType = max(todayRainType,int(val))
        elif category == "POP" and fcstDate == tomorrow:
            if int(val) > tomoRainPercent:
                tomoRainPercent = int(val)
                tomoRainTime = info["fcstTime"]
        elif category == "PTY" and fcstDate == tomorrow:
            tomoRainType = max(tomoRainType,int(val))

    todayRainTypeStr = RainTypeToString(todayRainType)
    tomoRainTypeStr = RainTypeToString(tomoRainType)
    briefing = ''
    if when == 1:
        briefing += f'오늘 최고기온은 {todayTMX} 도, 최저기온은 {todayTMN} 입니다. '
        if todayRainTypeStr != '없음':
            briefing += f'오늘 {todayRainTime[:2]}시 {todayRainTime[2:]}분에 {str(todayRainPercent)}% 확률로 {todayRainTypeStr} 내립니다. '
        else:
            briefing += '오늘은 비나 눈이 내리지 않습니다. '
    else:
        briefing += f'내일 최고기온은 {tomoTMX} 도, 최저기온은 {tomoTMN} 입니다. '
        if tomoRainTypeStr != '없음':
            briefing += f'내일 {tomoRainTime[:2]}시 {tomoRainTime[2:]}분에 {str(tomoRainPercent)}% 확률로 {tomoRainTypeStr} 내립니다. '
        else:
            briefing += '내일은 비나 눈이 내리지 않습니다. '

    
    return briefing
