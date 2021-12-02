import WeatherManager as WeatherMgr
import CampusManager as CampusMgr
import NewsManager as NewsMgr
import CalendarManager as CalendarMgr

print(WeatherMgr.GetWeatherBriefing(1))
print(WeatherMgr.GetWeatherBriefing(2))
print(CampusMgr.GetAssignmentList(3))
print(NewsMgr.SearchNews('코로나',5))
print(CalendarMgr.GetSchedule(10))