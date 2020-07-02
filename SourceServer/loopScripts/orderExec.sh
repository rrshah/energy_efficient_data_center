#!/bin/bash

echo "Starting Ordered Execution"

echo "Waiting 45 minutes..."
sleep 45m
echo "Starting App 1..."
#nohup ./webSearch.sh &> searchLog.out &
nohup ./media_streaming.sh &> mediaLog.out &

echo "Waiting 15 minutes..."
sleep 15m
echo "Starting App 2..."
#nohup ./graph_analytics_loop.sh &> graphLog.out &
#nohup ./media_streaming.sh &> mediaLog.out &
nohup ./workload_dnn_rnn.sh &> dnnrnnLog.out &

echo "Waiting 15 minutes..."
sleep 15m
echo "Starting App 3..."
#nohup ./workload_dnn_rnn.sh &> dnnrnnLog.out &
#nohup ./webSearch.sh &> searchLog.out &
nohup ./graph_analytics_loop.sh &> graphLog.out &

#echo "Wating 15 minutes..."
#sleep 15m
#echo "Starting App 3..."
#nohup ./data_analytics_loop.sh &> dataLog.out &

echo "Byeee"
