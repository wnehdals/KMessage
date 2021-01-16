import json
import requests
from flask import Flask, request,jsonify,render_template, redirect, url_for
import sys
import pyautogui
import time
import pyperclip
import os
import win32con
import win32api
import win32gui

app = Flask(__name__)
img_file_name = "{filename}.png"
fail_name = [] #보내기 실패한 이름들
@app.route('/')
@app.route('/index.html')
def index():
    title='제발쫌되라'
    #return redirect(url_for('getComplete'))
    return render_template('index.html',htmltitle = title)

@app.route('/complete.html')
def getComplete():
    return render_template('complete.html', fail_name_html=fail_name)
#친구 목록을 불러오는 함수
@app.route('/service.html', methods=["GET","POST"])
def getFriendList():

    data = None
    if request.method == 'POST':

        data = request.get_json()
        flag = False
        print(data)
        friendName = data['friendName'].split(' ')
        message = data['message']
        filePath = data['filePath']


        for i in friendName:
            step1 = open_chatroom(i)
            if(step1 == True):
                if(filePath == ""):
                    kakao_send_init(i,message)
                else:
                    kakao_send_init(i, message,filePath)
        return jsonify(result = "success", redir = fail_name)


    return render_template('service.html')



def click_img(imagePath):
    location = pyautogui.locateCenterOnScreen(imagePath, confidence = conf)
    x, y = location
    pyautogui.click(x, y)


def click_img_plus_x(imagePath, pixel):
    location = pyautogui.locateCenterOnScreen(imagePath, confidence = conf)
    x, y = location
    pyautogui.click(x + pixel, y)


def doubleClickImg (imagePath):
    location = pyautogui.locateCenterOnScreen(imagePath, confidence = conf)
    x, y = location
    pyautogui.click(x, y, clicks=2)


def set_delay():
    delay_time = input("몇 초 후에 프로그램을 실행하시겠습니까? : ")
    print(delay_time + "초 후에 프로그램을 실행합니다.")
    for remaining in range(int(delay_time), 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write("{:2d} seconds remaining.".format(remaining))
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\r프로그램 실행!\n")


def logout():
    try:
        click_img(img_path + 'menu.png')
    except Exception as e:
        print('e ', e)
    try:
        click_img(img_path + 'logout.png')
    except Exception as e:
        print('e ', e)


def bye_msg():
    input('프로그램이 종료되었습니다.')


def set_import_msg():
    with open("send_for_text.txt", "r", encoding='UTF-8') as f:
        text = f.read()
        print('======== 아래는 전송할 텍스트입니다. ========\n', text)
        return text



def SendReturn(hwnd):
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
    time.sleep(0.01)
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)


# # 채팅방 열기
def open_chatroom(chatroom_name):
    # # 친구목록 검색하는 Edit (채팅방이 열려있지 않아도 전송 가능하기 위하여)
    hwndkakao = win32gui.FindWindow(None, "카카오톡")
    hwndkakao_edit1 = win32gui.FindWindowEx(hwndkakao, None, "EVA_ChildWindow", None)
    hwndkakao_edit2_1 = win32gui.FindWindowEx(hwndkakao_edit1, None, "EVA_Window", None)
    hwndkakao_edit3 = win32gui.FindWindowEx(hwndkakao_edit2_1, None, "Edit", None)

    # # Edit에 검색 _ 입력되어있는 텍스트가 있어도 덮어쓰기됨
    win32api.SendMessage(hwndkakao_edit3, win32con.WM_SETTEXT, 0, chatroom_name)
    time.sleep(1)   # 안정성 위해 필요
    SendReturn(hwndkakao_edit3)
    #pyautogui.typewrite('\n', interval=0.1)
    time.sleep(1)

    try:
        imagePath = img_path + 'arrow.png'
        location = pyautogui.locateCenterOnScreen(imagePath, confidence=conf)
        x, y = location
        return True
    except TypeError:
        fail_name.append(chatroom_name)
        return False

# config
img_path = os.path.dirname(os.path.realpath(__file__)) + '/img/'
conf = 0.90
pyautogui.PAUSE = 0.5

# # 채팅방 전송 준비
def kakao_send_init(chatroom_name, text, img=None):
    # # 핸들 _ 채팅방
    hwndMain = win32gui.FindWindow( None, chatroom_name)
    hwndEdit = win32gui.FindWindowEx( hwndMain, None, "RichEdit20W", None)
    # hwndListControl = win32gui.FindWindowEx( hwndMain, None, "EVA_VH_ListControl_Dblclk", None)
    kakao_sendtext(text)
    if(img != None):
        kakao_sendimg(img)

    pyautogui.keyDown('esc')


    #win32api.SendMessage(hwndEdit, win32con.WM_SETTEXT, 0, text)
# 채팅방에 test입력
def kakao_sendtext(text):
    pyperclip.copy(text)
    pyautogui.hotkey("ctrl", "v")
    pyautogui.typewrite('\n', interval=0.1)


# 채팅방에 사진입력
def kakao_sendimg(img_file_name):
    click_img(img_path + 'light_gray_clip1.png')
    pyperclip.copy(img_file_name)
    pyautogui.hotkey("ctrl", "v")
    pyautogui.typewrite('\n', interval=0.1)




if __name__ == '__main__':
    app.run()
