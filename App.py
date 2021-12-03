import BriefingGenerator as Briefing
from flask import Flask, request
from flask_restx import Api, Resource, reqparse, Namespace,fields

profileDict = {}
profileDict[0] = Briefing.BriefingProfile()

briefingTextDict = {}
briefingTextDict[0] = profileDict[0].GenerateBriefingText()

curId = 0

app = Flask(__name__)
api = Api(
    app,
    version='0.1',
    title="HomeAssistant API Server",
    description="HomeAssistant API Server",
    base_url="3.91.196.2:5000/",
)

profileParser = reqparse.RequestParser()
profileFields = api.model('BrefingProfile', {
    'briefingTime':fields.String(description='자동 브리핑 시간', required=True, example='0900'),
    'contentList':fields.List(fields.String(example="Weather")),
    'campusDay':fields.Integer(description='며칠 이내의 과제 정보를 가져올 것인지 설정', required=True, example=3),
    'newsKeywordList':fields.List(fields.String(example="코로나")),
    'newsCount':fields.Integer(description='한 키워드당 몇 개의 뉴스를 검색할지', required=True, example=3),
    'scheduleCount':fields.Integer(description='몇 개의 일정을 가져올지', required=True, example=5)
})
profileIdFields = api.model('ProfileId', {
    'id':fields.Integer(description='프로필 id', required=True, example=0),
})

@api.route('/briefing/<int:profileId>')
class GetBriefingText(Resource):
    def get(self, profileId):
        """profileId에 해당하는 브리핑 문자열을 가져옵니다."""
        profileId = max(0,profileId)
        profileId = min(profileId, len(profileDict)-1)
        return {
            "text": briefingTextDict[profileId]
        }

@api.route('/briefing/profile')
class ManageProfile(Resource):
    def get(self):
        """모든 브리핑 프로필 정보를 가져옵니다."""
        allProfileJson = []
        for profile in profileDict.values():
            allProfileJson.append(profile.__dict__)

        return allProfileJson
    @api.expect(profileFields)
    @api.response(201, 'Success', profileIdFields)
    def post(self):
        """새로운 브리핑 프로필을 등록합니다. *contentList = ['Weather','Campus','News','Calendar']* """
        try:
            newProfile = Briefing.BriefingProfile(
                request.json.get('briefingTime'),
                request.json.get('contentList'),
                request.json.get('campusDay'),
                request.json.get('newsKeywordList'),
                request.json.get('newsCount'),
                request.json.get('scheduleCount'),
            )
            global curId
            curId += 1
            profileDict[curId] = newProfile
            briefingTextDict[curId] = profileDict[curId].GenerateBriefingText()
            return {
                "id": curId
            }
        except Exception as e:
            return {"error": str(e)}
    @api.expect(profileFields)
    @api.response(200, 'Success', profileIdFields)
    def put(self):
        """기존 브리핑 프로필을 수정합니다."""
        try:
            profileId = request.json.get('id')
            if profileId not in profileDict:
                return {"error": f"Profile {profileId} doesn't exist"}
            newProfile = Briefing.BriefingProfile(
                request.json.get('briefingTime'),
                request.json.get('contentList'),
                request.json.get('campusDay'),
                request.json.get('newsKeywordList'),
                request.json.get('newsCount'),
                request.json.get('scheduleCount'),
            )
            profileDict[profileId] = newProfile
            briefingTextDict[profileId] = profileDict[profileId].GenerateBriefingText()
            return {
                "id": profileId
            }
        except Exception as e:
            return {"error": str(e)}

    @api.expect(profileIdFields)
    def delete(self):
        """기존 브리핑 프로필을 삭제합니다."""
        profileId = request.json.get('id')
        del profileDict[profileId]
        return {
            "delete" : "success"
        }
    
@api.route('/briefing/weathertoday')
class GetWeatherTodayText(Resource):
    def get(self):
        """오늘 날씨정보 브리핑 문자열을 가져옵니다."""
        returnText = Briefing.GetWeatherToday()
        return {
            "text": returnText
        }

@api.route('/briefing/weathertomorrow')
class GetWeatherTomorrowText(Resource):
    def get(self):
        """내일 날씨정보 브리핑 문자열을 가져옵니다."""
        returnText = Briefing.GetWeatherTomorrow()
        return {
            "text": returnText
        }

@api.route('/briefing/campus')
class GetCampusText(Resource):
    def get(self):
        """과제 및 공지사항 브리핑 문자열을 가져옵니다."""
        returnText = Briefing.GetCampus()
        return {
            "text": returnText
        }

@api.route('/briefing/news/<string:keyword>')
class GetNewsText(Resource):
    def get(self, keyword):
        """뉴스 브리핑 문자열을 가져옵니다."""
        returnText = Briefing.GetNews(keyword)
        return {
            "text": returnText
        }

@api.route('/briefing/calendar')
class GetCalendarText(Resource):
    def get(self):
        """일정 브리핑 문자열을 가져옵니다."""
        returnText = Briefing.GetCalendar()
        return {
            "text": returnText
        }
        

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5000)