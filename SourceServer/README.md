# Predict Power and Migrate Application from Source Server
PredictPowerAndMigrate script queries the system for the 10 parameters like CPU utilization, number of processes, missRatio, etc.
MLPowerPredictionServer predicts the current power of the system when these system parameters are sent to it by using the DNN model.
30 such current power values passed as inputs to the MLPowerPredictonServer predicts the future power of the system using the RNN Model.

## Usage
```
PredictPowerAndMigrate.py <threshold_power> <script to be used to migrate application> <file nam> <number of iterations>

threshold_power - RNN power at which migration is to be triggered

script to be used to migrate application - All these scripts are inside sourceScripts folder. For eg, to migrate graph use
"./sourceScripts/source_graphAnalytics.sh" in quotes

file name - file to capture system parameters and power
```
