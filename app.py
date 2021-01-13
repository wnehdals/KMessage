import json

import requests
from flask import Flask, request,jsonify,render_template

app = Flask(__name__)


@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')
@app.route('/oauth')
def outh():
    code = str(request.args.get('code'))
    print(code)
    getExtraAuth()

@app.route('/oauth/friend')
def friendOuth():
    code = str(request.args.get('code'))
    print("friend : " + code)
    getToken(code)

def getToken(code):
    url = 'https://kauth.kakao.com/oauth/token'

    payload = "grant_type=authorization_code&client_id=a930f0b4697f2c084e1e8d0fc473049a&redirect_uri=http://127.0.0.1:5000/oauth/friend&code="+str(code)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cache-Control': 'no-cache',
    }
    response = requests.request("POST", url,data=payload, headers=headers)
    access_token = json.loads(((response.text).encode('utf-8')))['access_token']
    getFriendList(access_token)
def getLogin(access_token):

    url = "https://kapi.kakao.com/v2/user/me"
    header = {
        'Authorization': 'Bearer ' + str(access_token)
    }
    response = requests.get(url, headers=header).text
    print(response)
def getExtraAuth():
    print("extra")
    url = 'https://kauth.kakao.com/oauth/authorize?client_id=a930f0b4697f2c084e1e8d0fc473049a&redirect_uri=http://127.0.0.1:5000/oauth/friend&response_type=code&scope=talk_message,friends'

    isAuth = True

def getFriendList(access_token):
    url = "https://kapi.kakao.com/v1/api/talk/friends"
    header ={
        'Authorization' : 'Bearer ' + str(access_token)
    }
    friend = {}
    response = json.loads(requests.get(url,headers=header).text)['elements']
    #friendId = []
    #for i in response:
    #    friend['']
    #    print(i['profile_nickname'])
    uuid = response[0]['uuid']
    print("uuid" + uuid)
    makeMessage(uuid, access_token)

    #render_template('index.html')
def makeMessage(uuid,access_token):
    headers = {
        'Authorization': "Bearer " + str(access_token),
    }
    url = "https://kapi.kakao.com/v1/api/talk/friends/message/default/send"  ##친구에게 메시지 보내기
    uuid = '["'+ uuid+'"]'
    print(uuid)
    uuidsData = {'receiver_uuids': uuid}

    post = {
        "object_type": "text",
        "text": "test입니다",
        "link": {
            "web_url": "https://developers.kakao.com",
        },
    }

    data = {'template_object': json.dumps(post)}
    uuidsData.update(data)
    print(type(uuidsData))
    response = requests.post(url, headers=headers, data=uuidsData)
    print(response)
if __name__ == '__main__':
    app.run()
