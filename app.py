import numpy as np
from flask import Flask, request, jsonify, render_template,url_for
import pickle

import pandas as pd
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
model = pickle.load(open('tune_rf.pkl', 'rb'))




@app.route('/')
def home():
    return render_template('index.html')



@app.route('/pred',methods=['GET','POST'])

def pred():

    if request.method == "POST":
        departure_date = request.form["Departure_date"]
        dep = pd.to_datetime(departure_date)
        dep_date = dep.day
        dep_hour = dep.hour
        dep_min = dep.minute


        arrival_date = request.form["Arrival_date"]
        arv = pd.to_datetime(arrival_date)
        arv_date = arv.day
        arv_hour = arv.hour
        arv_min = arv.minute

        dur_hour = abs(arv_hour - dep_hour)
        dur_min = abs(arv_min - dep_min)

        duration= dur_hour * 60 + dur_min

        Source = request.form["source"]
        print(Source)
        sd= {'Banglore': 0,'Kolkata':3,'Delhi':2,'Chennai':1,'Mumbai':4}
        a= pd.Series(Source)
        sou = a.map(sd).values[0]

        des = request.form["Destination"]
        dest_dict = {'Banglore':0,'Cochin':1,'Delhi':2,'Kolkata': 3,'Hyderabad':4,'New Delhi':5}
        b= pd.Series(des)
        dest = b.map(dest_dict).values[0]

        Stoppage = int(request.form["stoppage"])

        airline = request.form["Airline"]
        airline_dict = {"Jet Airways": 5,'IndiGo':4,'Air India':2,'Air Asia':1,'Multiple carriers':7,'SpiceJet':9,'Vistara':11,
        'GoAir':3,'Multiple carriers Premium economy':8,'Jet Airways Business':6,'Vistara Premium economy':12,'Trujet':10}

        c= pd.Series(airline)
        air = c.map(airline_dict).values[0]


        pred= model.predict([[dep_date,dep_hour,dep_min,arv_date,arv_min,arv_hour,duration,sou,dest,Stoppage,air]])
        res=round(pred[0],3)
        return render_template('index.html',prediction_text="The price of flight is Rs. {}".format(res))


    return render_template("index.html")





if __name__ == "__main__":
    app.run(debug=True)