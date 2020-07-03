# Setting up GPU Server

This Readme is for instructions to setup the GPU server to predict power for Medusa and Kraken

## Usage

```bash
FLASK_APP=PowerPredictionApp.py flask run --host 0.0.0.0 --port 5001
```

The .h5 model files were generated using RNN and DNN model jupyter notebook scripts in their respective folders
