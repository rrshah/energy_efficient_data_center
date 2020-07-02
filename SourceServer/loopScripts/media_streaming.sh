#!/bin/bash

docker run --name media_stream --volumes-from streaming_dataset --net streaming_network cloudsuite/media-streaming:server
