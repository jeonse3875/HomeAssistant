import WeatherManager as WeatherMgr
import CampusManager as CampusMgr
import NewsManager as NewsMgr
import CalendarManager as CalendarMgr
import json

class BriefingProfile:
    def __init__(self, briefingTime = '0900', contentList = ['Weather','Campus','News','Calendar'], campusDay = 3,
    newsKeywordList = ['코로나','경제'], newsCount = 3, scheduleCount = 5) -> None:
        self.briefingTime = briefingTime
        self.contentList = contentList
        self.campusDay = campusDay
        self.newsKeywordList = newsKeywordList
        self.newsCount = newsCount
        self.scheduleCount = scheduleCount

    def GenerateBriefingText(self):
        if self.briefingTime is None:
            self.briefingTime = '0900'
        elif self.contentList is None:
            self.contentList = ['Weather','Campus','News','Calendar']
        elif self.campusDay is None:
            self.campusDay = 3
        elif self.newsKeywordList is None:
            self.newsKeywordList = ['코로나','경제']
        elif self.newsCount is None:
            self.newsCount = 3
        elif self.scheduleCount is None:
            self.scheduleCount = 5

        briefingText = ''

        for content in self.contentList:
            if content == 'Weather':
                briefingText += '날씨 정보입니다. '
                if self.briefingTime >= '1800':
                    briefingText += WeatherMgr.GetWeatherBriefing(2)
                else:
                    briefingText += WeatherMgr.GetWeatherBriefing(1)
            elif content == 'Campus':
                briefingText += '과제 및 공지사항 정보입니다. '
                assignments = CampusMgr.GetAssignmentList(self.campusDay)
                for assignment in assignments:
                    briefingText += assignment
            elif content == 'News':
                briefingText += '뉴스 정보입니다. '
                for keyword in self.newsKeywordList:
                    newsList = NewsMgr.SearchNews(keyword,self.newsCount)
                    for news in newsList:
                        briefingText += news + '. '
            elif content == 'Calendar':
                briefingText += '일정 정보입니다. '
                scheduleList = CalendarMgr.GetSchedule(self.scheduleCount)
                for sch in scheduleList:
                    briefingText += sch + ' '

        return briefingText

def GetWeatherToday():
    return WeatherMgr.GetWeatherBriefing(1)

def GetWeatherTomorrow():
    return WeatherMgr.GetWeatherBriefing(2)

def GetCampus():
    tempText = ''
    assignments = CampusMgr.GetAssignmentList(4)
    for assignment in assignments:
        tempText += assignment
    return tempText

def GetNews(keyword):
    tempText = ''
    newsList = NewsMgr.SearchNews(keyword,5)
    for news in newsList:
        tempText += news + '. '
    return tempText

def GetCalendar():
    tempText = ''
    scheduleList = CalendarMgr.GetSchedule(5)
    for sch in scheduleList:
        tempText += sch + ' '
    return tempText