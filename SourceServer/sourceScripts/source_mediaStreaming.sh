#!/bin/bash
now=$(date +"%T")
echo "Current time : $now"
containername="$1"

echo "Initiating Migration of Media Streaming to Kraken..."
echo "Commit current image state..."
sudo docker commit $containername ${containername}_image

echo "Stopping and Removing current running image..."
sudo docker stop $containername
sudo docker rm $containername

echo "Saving current image..."
sudo docker save ${containername}_image > /home/sjsu_ra/migration_img/${containername}_image.tar

echo "Removing current image"
sudo docker image rm ${containername}_image

echo "Transferring image to Kraken..."
scp /home/sjsu_ra/migration_img/${containername}_image.tar sjsu_ra@130.65.159.89:/home/sjsu_ra/migration_img/

echo "Connecting to Kraken..."
ssh sjsu_ra@130.65.159.89 bash "/home/sjsu_ra/migration_new/targetScripts/target_mediaStreaming.sh $containername"
