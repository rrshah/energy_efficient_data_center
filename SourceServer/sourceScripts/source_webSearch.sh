#!/bin/bash
now=$(date +"%T")
echo "Current time : $now"
containername="$1"

echo "Initiating Migration of Web Search to Kraken..."
echo "Commit current image state..."
#sudo docker commit $containername myregistry.com:5000/${containername}_image
sudo docker commit $containername ${containername}_image

echo "Stopping and Removing current running image..."
sudo docker stop $containername
sudo docker rm $containername

echo "Saving current image..."
#sudo docker push myregistry.com:5000/${containername}_image
sudo docker save ${containername}_image > /home/sjsu_ra/migration_img/${containername}_image.tar

echo "Removing current image"
#sudo docker image rm myregistry.com:5000/${containername}_image
sudo docker image rm ${containername}_image

echo "Transferring image to Kraken..."
#ssh sjsu_ra@130.65.159.89 bash "/home/sjsu_ra/migration/gatherpower/client_web_search_new.sh $containername"
scp /home/sjsu_ra/migration_img/${containername}_image.tar sjsu_ra@130.65.159.89:/home/sjsu_ra/migration_img/

echo "Connecting to Kraken..."
ssh sjsu_ra@130.65.159.89 bash "/home/sjsu_ra/migration_new/targetScripts/target_webSearch.sh $containername"
