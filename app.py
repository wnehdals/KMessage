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


#친구 목록을 불러오는 함수
@app.route('/service.html', methods=["GET","POST"])
def getFriendList():

    data = None
    if request.method == 'POST':
        data = request.get_json()
        friendName = data['friendName'].split(' ')
        message = data['message']
        for i in friendName:
            print(i)
            


    return render_template('service.html')






if __name__ == '__main__':
    app.run()
