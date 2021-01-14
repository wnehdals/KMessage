import json

import requests
from flask import Flask, request,jsonify,render_template, redirect

app = Flask(__name__)

cliend_id = ''
globalAccessToken = ''
@app.route('/')
@app.route('/index.html')
def index():
    title='제발쫌되라'


    return render_template('index.html',htmltitle = title)
@app.route('/oauth')
def outh():
    return render_template('index.html')

#카카오 outh코드를 받아오는 함수
@app.route('/oauth/friend')
def friendOuth():
    code = str(request.args.get('code'))
    getToken(code)
    return redirect("http://127.0.0.1:5000/")

#카카오 액세스 토큰을 얻어오는 함수
def getToken(code):
    global globalAccessToken
    url = 'https://kauth.kakao.com/oauth/token'
    payload2 = {
        'grant_type' : 'authorization_code',
        'client_id' : cliend_id,
        'redirect_uri' : 'http://127.0.0.1:5000/oauth/friend',
        'code' : str(code)
    }
    print('gettokencode :' + str(code))
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cache-Control': 'no-cache',
    }
    response = requests.request("POST", url,data=payload2, headers=headers)
    access_token = json.loads(((response.text).encode('utf-8')))['access_token']
    globalAccessToken = access_token
    return access_token


#친구 목록을 불러오는 함수
@app.route('/service.html', methods=["GET","POST"])
def getFriendList():
    data = None
    if request.method == 'POST':
        data = request.get_json()
        idList = data['uuids']
        message = data['message']
        for i in idList:
            sendFriend(i,message)

    url = "https://kapi.kakao.com/v1/api/talk/friends"
    header ={
        'Authorization' : 'Bearer ' + str(globalAccessToken)
    }
    response = json.loads(requests.get(url,headers=header).text)['elements']
    friendId = []
    for i in response:
        print(i['profile_nickname'])
        friendId.append(i['profile_nickname'])

    return render_template('service.html', friend_html = response)

#메시지를 보내는 함수
def sendFriend(_uuid, message):
    headers = {
        'Authorization': "Bearer " + str(globalAccessToken),
    }
    url = "https://kapi.kakao.com/v1/api/talk/friends/message/default/send"  ##친구에게 메시지 보내기
    uuid = '["' + _uuid + '"]'
    print(uuid)
    uuidsData = {'receiver_uuids': uuid}

    post = {
        "object_type": "text",
        "text": message,
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
