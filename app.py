import json

import requests
from flask import Flask, request,jsonify,render_template, redirect

app = Flask(__name__)

cliend_id = 'a930f0b4697f2c084e1e8d0fc473049a'
globalAccessToken = ''
@app.route('/')
@app.route('/index.html')
def index():
    title='좀되라18'


    return render_template('index.html',htmltitle = title)
@app.route('/oauth')
def outh():
    #code = str(request.args.get('code'))
    #print(code)
    #getExtraAuth()
    return render_template('index.html')

@app.route('/oauth/friend')
def friendOuth():
    #global sign_success
    code = str(request.args.get('code'))
    print("outh : " + code)
    getToken(code)
    return redirect("http://127.0.0.1:5000/")
'''
    if(sign_success == False):
        sign_success = True
        getToken(code)
        redirect("http://127.0.0.1:5000/")

    else:
        print(sign_success)
        origin(code)
'''


def getToken(code):
    global globalAccessToken
    url = 'https://kauth.kakao.com/oauth/token'
    payload2 = {
        'grant_type' : 'authorization_code',
        'client_id' : cliend_id,
        'redirect_uri' : 'http://127.0.0.1:5000/oauth/friend',
        'code' : str(code)
    }
    payload = "grant_type=authorization_code&client_id=" + cliend_id + "&redirect_uri=http://127.0.0.1:5000/oauth/friend"+'&code='+str(code)
    print('gettokencode :' + str(code))
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cache-Control': 'no-cache',
    }
    response = requests.request("POST", url,data=payload2, headers=headers)
    print("getToken : " + str((response.text).encode('utf-8')))
    access_token = json.loads(((response.text).encode('utf-8')))['access_token']
    globalAccessToken = access_token
    return access_token

def getLogin(access_token):

    url = "https://kapi.kakao.com/v2/user/me"
    header = {
        'Authorization': 'Bearer ' + str(access_token)
    }
    response = requests.get(url, headers=header).text
    print('getLogin')
def getExtraAuth():
    print("extra")
    url = 'https://kauth.kakao.com/oauth/authorize?client_id=' + cliend_id + '&redirect_uri=http://127.0.0.1:5000/oauth/friend&response_type=code&scope=talk_message,friends'

    isAuth = True


@app.route('/oauth/friend')
def origin(code):
    print('origin')

@app.route('/service.html')
def getFriendList():
    url = "https://kapi.kakao.com/v1/api/talk/friends"
    header ={
        'Authorization' : 'Bearer ' + str(globalAccessToken)
    }
    response = json.loads(requests.get(url,headers=header).text)['elements']
    friendId = []
    for i in response:
        print(i['profile_nickname'])
        friendId.append(i['profile_nickname'])

    
    friendId.append("dfgdf")
    friendId.append("fgjfghjkfjh")
    print(type(response))
    return render_template('service.html', friend_html = response)
    #uuid = response[0]['uuid']
    #print("uuid" + uuid)
    #makeMessage(uuid, access_token)

    #render_template('index.html')
@app.route("/function_route", methods=["GET", "POST"])
def makeMessage(uuid,access_token):
    if request.method == 'POST':
        data = {}
        data['message'] = request.json['mesesage']
        data['uuids'] = request.json['uuids']
        print(data)

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

#    data = {'template_object': json.dumps(post)}
#    uuidsData.update(data)
#    print(type(uuidsData))
#    response = requests.post(url, headers=headers, data=uuidsData)
#    print(response)
if __name__ == '__main__':
    app.run()
