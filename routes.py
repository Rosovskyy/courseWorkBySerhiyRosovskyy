from flask import Flask, render_template, flash, request, url_for, redirect, session
from pymongo import MongoClient
import regionsMap


app = Flask(__name__)
app.secret_key = "IT'SASECRETKEY"
db = MongoClient().datab

@app.route('/')
def main():
    return render_template('main.html')


@app.route('/regOrLog', methods=['GET'])
def regOrLog():
    return render_template('regOrLog.html')


@app.route('/choose', methods=['GET', 'POST'])
def choose():
    if request.method == 'POST':
        if request.form['submit'] == 'Log':
            return redirect('login')
        elif request.form['submit'] == 'Reg':
            return redirect('reg'   )

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        users = db.users
        login_user = users.find_one({'name': request.form['log']})
        if login_user and request.form['password'] == login_user['password']:
            session['name'] = login_user['name']
            return redirect('form')

    return redirect('login')



@app.route('/reg', methods=['GET', 'POST'])
def reg():
    if request.method == 'GET':
        return render_template('secondSignUp.html')
    if request.method == 'POST':
        d = request.form.to_dict()
        d['admin'] = False
        db.users.insert_one(d)
        return redirect('login')

@app.route('/form', methods=["GET", "POST"])
def form():
    if request.method == 'GET':
        if db.users.find_one({'name':session['name']})['admin']:
            return redirect('superuser')
        elif session['name'] == None:
            return redirect('login')
        return render_template('form.html')
    if request.method == 'POST':
        d = request.form.to_dict()
        db.coordinates.insert_one(d)
        if request.form['submit'] == 'MAP':
            return redirect('map')

@app.route('/superuser', methods=['GET'])
def superuser():
    if request.method == 'GET':
        sendData()
        delete('templates/my_map.html')
        return render_template('my_map.html')


@app.route('/map', methods=['GET', 'POST'])
def map():
    if request.method == 'GET':
        return render_template('map.html')
    if request.method == 'POST':
        body = request.form.to_dict(flat=False)
        lat = float(body['lat'][0])
        lon = float(body['lon'][0])
        m = list(db.coordinates.find({}))[-1]['_id']
        db.coordinates.update({'_id': m}, {'$set': {'lat': lat, 'lon': lon}})
        return "OK"

@app.route('/data', methods=['GET'])
def data():
    if request.method == 'GET':
        db.coordinates.insert({'name': request.args['name'], 'street': request.args['street']})
        return redirect('map')

def sendData():
    regionsMap.main()
    all = list(db.coordinates.find({}))
    for i in all:
        name = i['name']
        street = i['street']
        regionsMap.putMarker((i['lat'], i['lon']), 'yellow')
    regionsMap.draw()

@app.route('/bye', methods=['GET'])
def bye():
    if request.method == 'GET':
        return render_template('thanks.html')


def delete(path):
    f = open(path, 'r')
    lines = f.readlines()
    f.close()
    f = open(path, 'w')
    for line in lines:
        if ("var img = new google.maps.MarkerImage") in line:
            line = line.replace("/usr/local/lib/python3.6/site-packages/gmplot/markers/", "https://raw.githubusercontent.com/vgm64/gmplot/master/gmplot/markers/")
            print(line)
        f.write(line)
    f.close()





if __name__ == '__main__':
    app.run(debug=True)