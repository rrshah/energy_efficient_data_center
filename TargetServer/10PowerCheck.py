import paramiko
import csv
import time
import sys
import psutil as ps
import datetime as dt
import subprocess
import requests
from sklearn.externals import joblib
from tensorflow.keras.models import load_model
import json

ip = '130.65.159.89'
username = 'sjsu_ra'
password = 'sjsu124'
port = 22
cmd = 'sudo ./wattsup_pyrovski/watts-up/./wattsup ttyUSB0 -c 1 watts'
#ssh = paramiko.SSHClient()
#ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#ssh.connect(ip, port, username, password)

def predict_power(param):
    model = load_model('DNN_2layer_10_params.h5')
    scalar_filename = "scaler.save"
    scalar = joblib.load(scalar_filename)
    return model.predict(scalar.transform(param))[0][0]

def perfStat():
	cmd = ['sudo','perf', 'stat', '--time' ,'1000', '-e', 'cache-misses,cache-references,instructions']
	response = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	output = str(response.communicate())
	output = output.split('\n')
	output = output[0].split('\\n')

	cache_misses = int(output[3].split()[0].replace(',',''))
	cache_ref = int(output[4].split()[0].replace(',',''))
	instructions = int(output[5].split()[0].replace(',',''))
	miss_ratio = float(cache_misses)/float(cache_ref) 
	return {'instructions': instructions, 'miss-ratio': miss_ratio}
#Looping Power Output:
print("Predicted and Actual Power Values:")

f=open(sys.argv[1]+'.csv','a')
f.write('timeStamp,currentCPUFrequency,userTime1Sec,percentCPU,interrupts,interruptsSoftware,numberOfProcesses,percentVirtualMemory,systemCalls,instructions,missRatio,PredictedPower\n')

i=0
loopcount = int(sys.argv[2])
while(i<=loopcount):
	try:
		p =[]
		info=[]
		tempInfo = []
		cpu_times=ps.cpu_times()
		cpu_stats=ps.cpu_stats()
		time_previous = dt.datetime.now()

		#stdin, stdout, stderr = ssh.exec_command(cmd)
		#outlines = stdout.readlines()
		#resp = ''.join(outlines)
		#actual = float(resp.strip())

		cpu_stats_current=ps.cpu_stats()
		cpu_times_current=ps.cpu_times()
		time_current = dt.datetime.now()
		time_elapsed = (time_current - time_previous).total_seconds()
		virtual_memory_stats = ps.virtual_memory()
		swap_memory_stats = ps.swap_memory()

		info.append(ps.cpu_freq()[0])                                   # cpu current frequency                         PARAMETER 1
		tempInfo.append(ps.cpu_freq()[0])

		info.append((cpu_times_current[0]-cpu_times[0])/time_elapsed)   # time spent for user in 1 sec                  PARAMETER 2
		tempInfo.append((cpu_times_current[0]-cpu_times[0])/time_elapsed)
		
		info.append(ps.cpu_percent())                                   # cpu percentage                                PARAMETER 3
		tempInfo.append(ps.cpu_percent())

		info.append((cpu_stats_current[1]-cpu_stats[1])/time_elapsed)   # interrupts                                    PARAMETER 4
		tempInfo.append((cpu_stats_current[1]-cpu_stats[1])/time_elapsed)

		info.append((cpu_stats_current[2]-cpu_stats[2])/time_elapsed)   # sw interrupts                                 PARAMETER 5
		tempInfo.append((cpu_stats_current[2]-cpu_stats[2])/time_elapsed)

		info.append(len(ps.pids()))                                     # number of processes                           PARAMTEER 6
		tempInfo.append(len(ps.pids()))
		
		info.append(virtual_memory_stats[2])                            # virtual memory used percentage                PARAMETER 7
		
		info.append((cpu_stats_current[2]-cpu_stats[2])/time_elapsed)   # number of system calls                        PARAMETER 8

		#info.append(virtual_memory_stats[9])                            # shared memory used                            PARAMETER 9

		cacheMap = perfStat()
		info.append(cacheMap['instructions'])                           #Instructions                                   PARAMETER 10
		info.append(cacheMap['miss-ratio'])				#Miss Ratio					PARAMETER 11


		r = requests.post('http://130.65.159.84:5001/api/predict',json = {'param':info})
		print(i, "Predicted power:",float(r.json()))
		info.append(float(r.json()))
		#p.append(info)
		#predicted_power = predict_power(p)
		#info.append(predicted_power)        


		f.write(time.ctime()+','+ str(info).strip('[]')+'\n')

		i+=1
		time.sleep(3)
	except Exception as e:
		print("Failed " +str(e))
		pass
f.close()
