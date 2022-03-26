import requests
from flask import *
import weatherkey
import pickle
import numpy as np


app = Flask(__name__)

model = 'rfnew1.pkl'
model = pickle.load(open(model,'rb'))


@app.route('/login', methods=['POST'])
def login():
    print(request.get_json())
    value = {
        "Nitrogen": request.get_json().get('Nitrogen'),
        "Phosphorus": request.get_json().get('Phosphorus'),
        "Potassium": request.get_json().get('Potassium'),
        "Soil Type" : request.get_json().get('Soil Type'),
        "Crop Type": request.get_json().get('Crop Type'),
        "Moisture": request.get_json().get('Moisture'),
        # "Temperature": request.get_json().get('Temperature'),
        # "Humidity": request.get_json().get('Humidity'),
        "State": request.get_json().get('State'),
        "City" : request.get_json().get('City')

    }

    Nitrogen = request.get_json().get('Nitrogen')
    Phosphorus = request.get_json().get('Phosphorus')
    Potassium = request.get_json().get('Potassium')
    # Ph = request.get_json().get('Ph')
    SoilType = request.get_json().get('SoilType')
    CropType = request.get_json().get('CropType')
    State = request.get_json().get('State')
    City = request.get_json().get('City')
    Moisture = request.get_json().get('Moisture')
    # Temperature = request.get_json().get('Temperature')
    # Humidity= request.get_json().get('Humidity')
    print(fetch(City))
    if fetch(City) != None:
        temperature, humidity = fetch(City)

        data = np.array([[temperature, humidity, Moisture, SoilType, CropType, Nitrogen, Potassium, Phosphorus]])
        print(data)
        my_prediction = model.predict(data)
        print("CAlled SUccess")
        final_prediction = my_prediction[0]
        print(final_prediction)
        return jsonify({"result" : final_prediction})


    # my_prediction = model.predict(data)
    #
    # fertilizer_Name = my_prediction[0]
    # print(fertilizer_Name)

   # return jsonify({"result": final_prediction})

    # Dictionary to JSON Object using dumps() method
    # Return JSON Object
    return json.dumps(value)


#   return request["nm"];



def fetch(City):

    api_key  = weatherkey.weather_api_key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + City

    response = requests.get(complete_url)
    a = response.json()

    if a["cod"] != "404":
        b = a["main"]

        temperature = round((b["temp"] - 273.15), 2)
        humidity = b["humidity"]

        return temperature, humidity
    else:
        return None



# @app.route("/pre" , methods = ['POST'])
# def prediction():
#     if request.method =='POST':
#         val = login.value
#         N = val["N"]
#         P =val["P"]
#         K = val["K"]
#         Ph = val["Ph"]
#         Rain = val["Rain"]
#         State = val["State"]
#         City = val["City"]
#
#         if fetch(City) != None:
#
#             temperature, humidity = fetch(City)
#             data = np.array([[N, P, K, temperature, humidity, Ph, Rain]])
#             my_prediction = model.predict(data)
#             final_prediction = my_prediction[0]
#             print(final_prediction)
#             return jsonify(final_prediction)
#






if __name__ == '__main__':
    app.run(debug=True)