from flask import Flask, render_template, url_for, request
import numpy as np
import pandas as pd
from sklearn.preprocessing import RobustScaler
import pickle
import jsonify

model = pickle.load(open('random_forest_model.pkl', 'rb'))
app = Flask(__name__)

@app.route('/', methods= ['GET'])
def home():
    return render_template('home.html')


scalar = RobustScaler()
@app.route('/predict', methods= ['POST'])
def predict():
    Levy= 0
    Mileage= 0
    if request.method == 'POST':
        Year = int(request.form['Year'])
        Levy = int(request.form['Levy'])
        Mileage = int(request.form['Mileage'])
        Cylinders = int(request.form['Cylinders'])
        Airbags = int(request.form['Airbags'])
        Hatchback = str(request.form['Hatchback'])
        if(Hatchback == 'Hatchback'):
            Hatchback= 1
            Jeep= 0
            Minivan= 0
            Sedan= 0
        elif(Hatchback == 'Jeep'):
            Hatchback= 0
            Jeep= 1
            Minivan= 0
            Sedan= 0
        elif(Hatchback == 'Minivan'):
            Hatchback= 0
            Jeep= 0
            Minivan= 1
            Sedan= 0
        elif(Hatchback == 'Sedan'):
            Hatchback= 0
            Jeep= 0
            Minivan= 0
            Sedan= 1
        else:
            Hatchback= 0
            Jeep= 0
            Minivan= 0
            Sedan= 0
        Leather_Yes = str(request.form['Leather_Yes'])
        if(Leather_Yes == 'Yes'):
            Leather_Yes= 1
        else:
            Leather_Yes= 0
        Diesel = str(request.form['Diesel'])
        if(Diesel == 'Diesel'):
            Diesel= 1
            Hybrid= 0
            LPG= 0
            Petrol= 0
        elif(Diesel == 'Petrol'):
            Diesel= 0
            Hybrid= 0
            LPG= 0
            Petrol= 1
        elif(Diesel == 'Hybrid'):
            Diesel= 0
            Hybrid= 1
            LPG= 0
            Petrol= 0
        elif(Diesel == 'LPG'):
            Diesel= 0
            Hybrid= 0
            LPG= 1
            Petrol= 0
        else:
            Diesel= 0
            Hybrid= 0
            LPG= 0
            Petrol= 0
        Turbo = str(request.form['Turbo'])
        if(Turbo == 'Turbo'):
            Turbo= 1
        else:
            Turbo= 0
        Gear_Manual = str(request.form['Gear_Manual'])
        if(Gear_Manual == 'Manual'):
            Gear_Manual= 1
            Gear_Tiptronic = 0
            Gear_Variator= 0
        elif(Gear_Manual == 'Tiptronic'):
            Gear_Manual= 0
            Gear_Tiptronic= 1
            Gear_Variator= 0
        elif(Gear_Manual == 'Variator'):
            Gear_Manual= 0
            Gear_Tiptronic= 0
            Gear_Variator= 1
        else:
            Gear_Manual= 0
            Gear_Tiptronic= 0
            Gear_Variator= 0
        Front_Wheel = str(request.form['Front_Wheel'])
        if(Front_Wheel == 'Front'):
            Front_Wheel= 1
            Rear_Wheel = 0
        elif(Front_Wheel == 'Rear'):
            Front_Wheel= 0
            Rear_Wheel= 1
        else:
            Front_Wheel= 0
            Rear_Wheel= 0
        RightHand_Drive =  str(request.form['RightHand_Drive'])
        if(RightHand_Drive == 'RightHand'):
            RightHand_Drive= 1
        else:
            RightHand_Drive= 0

        scalar.fit_transform([[Levy, Mileage, Cylinders, Airbags]])
        prediction = model.predict([[Year, Hatchback, Jeep, Minivan, Sedan, Leather_Yes, Diesel, Hybrid, LPG, Petrol, Turbo, Gear_Manual,
         Gear_Tiptronic, Gear_Variator, Front_Wheel, Rear_Wheel, RightHand_Drive, Levy, Mileage, Cylinders, Airbags]])
        output=round(np.exp(prediction[0]),2)


        if output<0:
            return render_template('home.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('home.html',prediction_text="You Can Sell The Car at {}".format(output))
    else:
        return render_template('home.html')



if __name__ == '__main__':
    app.run(host= '127.0.0.1', port= 200, debug = True) 