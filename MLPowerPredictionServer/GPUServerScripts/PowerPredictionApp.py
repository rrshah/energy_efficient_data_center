#!/usr/lib/python3

import json
from flask import Flask, request
from sklearn.externals import joblib
from tensorflow.keras.models import load_model

app = Flask(__name__)


@app.route('/api/predict', methods=['POST'])
def predict_api():
    data = request.data
    data_dict = json.loads(data)
    print(data_dict)
    power = predict_power([data_dict['param']])
    return json.dumps(str(power[0][0]))

@app.route('/api/predict_rnn', methods=['POST'])
def predict_rnn_api():
    data = request.data
    data_dict = json.loads(data)
    print(data_dict)
    power = predict_power_rnn([data_dict['param']])
    print(power)
    return json.dumps(str(power[0][0]))


def predict_power_rnn(param):
    import numpy as np
    model = load_model('RNNPowerPredictionModel.h5')
    scalar_filename = "scaler_RNN.save"
    scalar = joblib.load(scalar_filename)
    param = scalar.transform(param)
    param = np.array(param)
    param = np.reshape(param, (param.shape[0], param.shape[1], 1))
    predicted_power = model.predict(param)
    predicted_power = scalar.inverse_transform(predicted_power)
    return predicted_power

def predict_power(param):
    model = load_model('DNNPowerPredictionModel.h5')
    scalar_filename = "scaler.save"
    scalar = joblib.load(scalar_filename)
    return model.predict(scalar.transform(param))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5001)
