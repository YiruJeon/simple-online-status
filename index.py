import json
from flask import Flask, request, render_template, redirect, make_response, url_for
import datetime
import pytz

app = Flask(__name__)

status = {}


@app.route("/join", methods=["POST"])
def join():
    if 'id' not in request.cookies:
        return redirect(url_for('index'))
    if request.method == "POST":
        id = request.cookies['id']
        playnote = request.form['playnote']
        now = datetime.datetime.now().astimezone(pytz.timezone('Asia/Seoul')).time().strftime("%H:%M:%S")
        try:
            end_time = int(request.form['end_time'])
        except Exception as allException:
            end_time = 0
        status[id] = (playnote, now, end_time)
    else:
        return "ERROR, 개발자에게 문의하세요"

    return redirect(url_for('index'))

@app.route("/exit", methods=["POST"])
def exit():
    if 'id' not in request.cookies:
        return redirect(url_for('index'))
    if request.method == "POST":
        id = request.cookies['id']
        if id not in status:
            return "ERROR, 쿠키 멋대로 바꾸셨나요? 개발자에게 문의하세요"
        del(status[id])
    else:
        return "ERROR, 개발자에게 문의하세요"

    return redirect(url_for('index'))


@app.route("/setcookie", methods=["POST"])
def setcookie():
    id = request.form['id']
    resp = make_response(redirect(url_for('index')))
    # id 길이가 0 인건 제외해버림
    if len(id) > 0:
      resp.set_cookie('id', id)
    return resp


@app.route("/")
def index():
    if 'id' in request.cookies:
        return render_template('index.html', status=status, id=request.cookies['id'])
    else:
        return render_template('request_id.html')



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)