# Source Scripts

Use the scripts in this folder to start any application on loop on the target server.
## Usage

You can use these commands to run each of the applications individually:

```bash
./webSearch.sh
./media_streaming.sh
./data_analytics_loop.sh
./graph_analytics_loop.sh
./workload_dnn_rnn.sh
```
Use the following script to run each application in a pre-specified sequence. The time gap between the start of each application can also be specified here.
```bash
./orderExec.sh
```
Edit this file to change the order in which each of the application is started.
```bash
vi orderExec.sh
```
## Stop All Applications
Use the following script to kill all running applications and their respective Docker images.

```bash
./close_all_docker_apps.sh
```
