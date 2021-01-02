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


def getExtraAuth():
    print("extra")
    url = 'https://kauth.kakao.com/oauth/authorize?client_id=a930f0b4697f2c084e1e8d0fc473049a&redirect_uri=http://127.0.0.1:5000/oauth/friend&response_type=code&scope=talk_message,friends'

    isAuth = True

def getFriendList(access_token):
    print('access :  ' + access_token)
    url = "https://kapi.kakao.com/v1/api/talk/friends?limit=100"
    header ={
        'Authorization' : 'Bearer ' + str(access_token)
    }
    response = requests.get(url,headers=header).text
    print(response)
    friendList = response.get("elements")
    print(friendList)
    #friendId = []
    #for i in friendList:
    #    print(i['profile_nickname'])
    render_template('index.html')

if __name__ == '__main__':
    app.run()
