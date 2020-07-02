#!/bin/bash
echo 'Running webSearch on client'
containername="$1"

echo 'Stopping container if running'
sudo docker stop $containername

echo 'Removing container.'
sudo docker rm $containername

echo 'Removing container image.'
#sudo docker image rm myregistry.com:5000/${containername}_image
sudo docker image rm ${containername}_image

echo 'Loading previously saved container.'
#sudo docker pull myregistry.com:5000/${containername}_image
sudo docker load < /home/sjsu_ra/migration_img/${containername}_image.tar

echo 'Running loaded container.'
sudo docker run --name server --net search_network -p 8983:8983 cloudsuite/web-search:server 12g 1

now=$(date +"%T")
echo "End time : $now"

