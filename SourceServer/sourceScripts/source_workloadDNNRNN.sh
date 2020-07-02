#!/bin/bash
now=$(date +"%T")
echo "Starting DNN+RNN Workload Migration..."
echo "Current time : $now"
containername="$1"

echo "Committing current image state..."
sudo docker commit $containername ${containername}_image

echo "Stopping container..."
sudo docker stop $containername

echo "Removing container..."
sudo docker rm $containername

echo "Saving container..."
sudo docker save ${containername}_image > /home/sjsu_ra/migration_img/${containername}_image.tar

#echo "Removing container image..."
#sudo docker image rm ${containername}_image

echo "Transferring container image to Kraken..."
scp /home/sjsu_ra/migration_img/${containername}_image.tar sjsu_ra@130.65.159.89:/home/sjsu_ra/migration_img/

echo "Connecting to Kraken"
ssh sjsu_ra@130.65.159.89 bash "/home/sjsu_ra/migration_new/targetScripts/target_workloadDNNRNN.sh $containername"
