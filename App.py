import BriefingGenerator as Briefing
from flask import Flask, request
from flask_restx import Api, Resource
import json

profileDict = {}
profileDict[0] = Briefing.BriefingProfile()

briefingTextDict = {}
briefingTextDict[0] = profileDict[0].GenerateBriefingText()
curId = 0

app = Flask(__name__)
api = Api(app)

@api.route('/briefing/<int:profileId>')
class GetBriefingText(Resource):
    def get(self, profileId):
        profileId = max(0,profileId)
        profileId = min(profileId, len(profileDict)-1)
        return {
            "text": briefingTextDict[profileId]
        }

@api.route('/briefing/profile')
class ManageProfile(Resource):
    def get(self):
        allProfileJson = []
        for profile in profileDict.values():
            allProfileJson.append(profile.__dict__)

        return allProfileJson
    def post(self):
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
                "id": curId,
                "profile": profileDict[curId].__dict__
            }
        except Exception as e:
            return {"error": str(e)}
    def put(self):
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
                "id": profileId,
                "profile": newProfile.__dict__
            }
        except Exception as e:
            return {"error": str(e)}

    def delete(self):
        profileId = request.json.get('id')
        del profileDict[profileId]
        return {
            "delete" : "success"
        }
        

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5000)