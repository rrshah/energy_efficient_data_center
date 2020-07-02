#!/bin/bash
echo 'Running Media Streaming on Kraken.'
containername="$1"

echo 'Stopping container if running'
sudo docker stop $containername

echo 'Removing container.'
sudo docker rm $containername

echo 'Removing container image.'
sudo docker image rm ${containername}_image

echo 'Loading previously saved container.'
sudo docker load < /home/sjsu_ra/migration_img/${containername}_image.tar

echo 'Running loaded container.'
#sudo docker run --name=$containername -d --volumes-from streaming_dataset --net streaming_network ${containername}_image
docker run -d --name media_stream --volumes-from streaming_dataset --net streaming_network cloudsuite/media-streaming:server
now=$(date +"%T")

echo "End time : $now"
