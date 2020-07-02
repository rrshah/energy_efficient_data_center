#!/bin/bash

echo "Killing all scripts"
killall orderExec.sh
killall graph_analytics_loop.sh
killall data_analytics_loop.sh
killall media_streaming.sh
killall webSearch.sh 
killall workload_dnn_rnn.sh

docker rm -f web_search
docker rm -f data-analytics-master
docker rm -f data-analytics-slave01
docker rm -f data-analytics-slave02
docker rm -f data-analytics-slave03
docker rm -f data-analytics-slave04
docker rm -f media_stream
docker rm -f graph-server
docker rm -f workload_dnn_rnn
echo "Done......"
