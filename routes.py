from flask import Flask, render_template, flash, request, url_for, redirect, session
from pymongo import MongoClient
from spampkg import regionsMap


app = Flask(__name__)
app.secret_key = "IT'SASECRETKEY"
db = MongoClient().datab

@app.route('/')
def main():
    """
    Return the main page of the project
    """
    return render_template('main.html')


@app.route('/regOrLog', methods=['GET'])
def regOrLog():
    """
    Return the page, in which the user will have
    a choice to sign up or to sign in
    """
    return render_template('regOrLog.html')


@app.route('/choose', methods=['GET', 'POST'])
def choose():
    """
    The function finds out which button was pressed
    and as a result, returns the appropriate another
    function
    """
    if request.method == 'POST':
        if request.form['submit'] == 'Log':
            return redirect('login')
        elif request.form['submit'] == 'Reg':
            return redirect('reg')

@app.route('/login', methods=["GET", "POST"])
def login():
    """
    The function has two possible options:
    to open the page, which will represent the login
    of the user or if the page has been already
    opened, it takes data from it and check whether
    it is a user with these data in the database
    """
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
    """
    The function has two possible options:
    to open the page, which will represent the
    registration of the newcoming user or if
    the page has been already opened, it takes
    data from it and send them to the database
    """
    if request.method == 'GET':
        return render_template('secondSignUp.html')
    if request.method == 'POST':
        d = request.form.to_dict()
        d['admin'] = False
        db.users.insert_one(d)
        return redirect('login')

@app.route('/form', methods=["GET", "POST"])
def form():
    """
    The function has a few possible options:
    to open different pages for the superuser and
    a usual one or open the login page if the data
    was not correct. If the page has been alreay
    opened, it takes data from it and send them to
    the database
    """
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
    """
    The function returns the map, which will
    show the needed data. But before it, the map
    will be created.
    """
    if request.method == 'GET':
        sendData()
        delete('templates/my_map.html')
        return render_template('my_map.html')


@app.route('/map', methods=['GET', 'POST'])
def map():
    """
    The function has two possible options:
    to open the page of the map, where the user
    can put the marker, where the idle lamp is
    located or if he has already done it he can
    press the "CONFIRM" button to send all data
    to the database
    """
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
    """
    The functions gets all data from
    the input forms of the "form" page and
    send them to the database
    """
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
    """
    The function returns the final page
    """
    if request.method == 'GET':
        return render_template('thanks.html')


def delete(path):
    """
    (str) -> Nonetype
    The function goes through the *.js
    file and change some lines of the
    code, because that file was created
    automatically
    """
    f = open(path, 'r')
    lines = f.readlines()
    f.close()
    f = open(path, 'w')
    for line in lines:
        if ("var img = new google.maps.MarkerImage") in line:
            line = line.replace("/usr/local/lib/python3.6/site-packages/gmplot/markers/", "https://raw.githubusercontent.com/vgm64/gmplot/master/gmplot/markers/")
        f.write(line)
    f.close()





if __name__ == '__main__':
    app.run(debug=True)