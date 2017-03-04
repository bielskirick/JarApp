from flask import Flask, render_template, request
import pickle
from random import randint

data = {}
data['name'] = []
data['price'] = []
data['neighborhood'] = []
data['region'] = []
data['reservation'] = []
data['type'] = []
data['time'] = []

app = Flask(__name__)

def logPrint(msg):
    print(msg)
    try:
        with open('log.txt','ab') as f:
            f.writelines(msg + '\n')
    except:
        print('Could not write to log.')
        pass

def initialization():
    global data
    logPrint('Initializing.')

    try:
        with open('dataStore.p','rb') as f:
            data = pickle.load(f)
    except:
        logPrint('Could not find datastore, will create a new file.')
        pass

    logPrint('Initialization Complete')

def saveData():
    global data
    logPrint('Saving Data')

    try:
        with open('dataStore.p','wb') as f:
            pickle.dump(data, f)
    except:
        logPrint('Unable to write datastore, will try again later.')
        pass

    logPrint('Saving Complete')

@app.route('/')
def index():
    global data
    initialization()
    return render_template('index.html')

@app.route('/newLocation')
def newLocation():
    return render_template('newLocation.html')

@app.route('/randomRestuarant')
def randomRestuarant():
    global data
    indices = [i for i, x in enumerate(data['type']) if x.upper() == 'R']
    if len(indices) < 0:
        return "DataStore Empty. Add Some Locations."
    loc = randint(0,len(indices)-1)

    name = str(data['name'][indices[loc]])
    price = str(data['price'][indices[loc]])
    neighborhood = str(data['neighborhood'][indices[loc]])
    region = str(data['region'][indices[loc]])
    res  =  str(data['reservation'][indices[loc]])
    locType = str(data['type'][indices[loc]])
    time = str(data['time'][indices[loc]])

    return render_template('randomLocation.html', name=name, price=price, neighborhood=neighborhood, region=region, res=res, locType=locType, time=time)

@app.route('/randomActivity')
def randomActivity():
    global data
    indices = [i for i, x in enumerate(data['type']) if x.upper() == 'A']
    if len(indices) < 0:
        return "DataStore Empty. Add Some Locations."
    loc = randint(0,len(indices)-1)

    name = str(data['name'][indices[loc]])
    price = str(data['price'][indices[loc]])
    neighborhood = str(data['neighborhood'][indices[loc]])
    region = str(data['region'][indices[loc]])
    res  =  str(data['reservation'][indices[loc]])
    locType = str(data['type'][indices[loc]])
    time = str(data['time'][indices[loc]])

    return render_template('randomLocation.html', name=name, price=price, neighborhood=neighborhood, region=region, res=res, locType=locType, time=time)

@app.route('/insertData', methods = ['POST'])
def insertData():
    global data
    initialization()
    data['name'].append(request.form['name'])
    data['price'].append(request.form['price'])
    data['neighborhood'].append(request.form['neighborhood'])
    data['region'].append(request.form['region'])
    data['reservation'].append(request.form['reservation'])
    data['type'].append(request.form['type'])
    data['time'].append(request.form['time'])
    saveData()
    return render_template('insertData.html')

initialization()
app.run(debug=1, host="0.0.0.0", port=80)
