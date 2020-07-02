#!/bin/bash
docker run --name web_search --net search_network -p 8983:8983 cloudsuite/web-search:server 12g 1
