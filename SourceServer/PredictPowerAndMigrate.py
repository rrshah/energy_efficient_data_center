######## First argument - threshold power

######## Second argument - migration script in quotes like below egs
#/////////////////////////////////////////////////////////////////////////
######## ./sourceScripts/source_graphAnalytics.sh 
#////////////////////////////////////////////////////////////////////////

######## Thrid argument - File to be used to store the values
######## Fourth argument - Number of iterations

import psutil as ps
import numpy as np
import csv
import sys
import time
import paramiko
import datetime as dt
import requests
import shlex
import subprocess
import threading

runTime = []

RNN_predicted_power = 0
class sysParam:
        migrated = False
	threshold_power_arr = [140, 120, 112.86, 107.92, 80]
        rnn_power_values = []
	counter = 0
	write_actual = False
	def __init__(self):
		self.X=[]

	def perfStat(self):
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

	def gatherData(self):
                num_samples=30
		info=[]
		cpu_times=ps.cpu_times()
		cpu_stats=ps.cpu_stats()
        	time_previous = dt.datetime.now()
		global RNN_predicted_power
		time.sleep(2) # comment this 
        	#insert watts up script here

        	#ip = '130.65.159.89'
        	#username = 'sjsu_ra'
        	#password = 'sjsu124'
        	#port = 22
        	#cmd = 'sudo ./wattsup_pyrovski/watts-up/./wattsup ttyUSB0 -c 1 watts'
       		#ssh = paramiko.SSHClient()
        	#ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        	#ssh.connect(ip, port, username, password)

        	#stdin, stdout, stderr = ssh.exec_command(cmd)
        	#outlines = stdout.readlines()
                #resp = ''.join(outlines) 
                #print("Raw response:",resp.strip())

        	#actual = float(resp.strip())
        	#print("ACTUAL POWER : ", actual)

        	cpu_stats_current=ps.cpu_stats()
		cpu_times_current=ps.cpu_times()
        	time_current = dt.datetime.now()
        	time_elapsed = (time_current - time_previous).total_seconds()
		virtual_memory_stats = ps.virtual_memory()
        	swap_memory_stats = ps.swap_memory()

        	info.append(ps.cpu_freq()[0]) #cpu current frequency                                                   PARAMETER 1
		info.append((cpu_times_current[0]-cpu_times[0])/time_elapsed) # time spent for user in 1 sec           PARAMETER 2
	    	info.append(ps.cpu_percent())# cpu percentage                                                          PARAMETER 3		
		info.append((cpu_stats_current[1]-cpu_stats[1])/time_elapsed)#interrupts                               PARAMETER 4
		info.append((cpu_stats_current[2]-cpu_stats[2])/time_elapsed) # sw interrupts                          PARAMETER 5
        	info.append(len(ps.pids())) # number of processes                                                      PARAMTEER 6
		info.append(virtual_memory_stats[2])                            # virtual memory used percentage                PARAMETER 7
		info.append((cpu_stats_current[2]-cpu_stats[2])/time_elapsed)   # number of system calls                        PARAMETER 8
	        #info.append(virtual_memory_stats[9])                            # shared memory used                            PARAMETER 9
	        cacheMap = self.perfStat()
        	info.append(cacheMap['instructions'])                           #Instructions                                   PARAMETER 10
        	info.append(cacheMap['miss-ratio'])                             #Miss Ratio                                     PARAMETER 11
		
		r = requests.post('http://130.65.159.84:5001/api/predict',json = {'param':info})
                print("predicted power:",float(r.json()))
		power_predicted = float(r.json())
	        if (len(self.rnn_power_values) >= num_samples):
			print("Predicting power, len = ",len(self.rnn_power_values))
                        r = requests.post('http://130.65.159.84:5001/api/predict_rnn',json = {'param': self.rnn_power_values})
                        self.rnn_power_values.pop(0)
			print("RNN predicted power = ", float(r.json()))
			rnn_power = float(r.json())
			f = open(sys.argv[3], 'a')
			f.write(time.ctime() + ","+ str(rnn_power) + "\n")
			f.close()
			self.write_actual = True
			RNN_predicted_power = float(r.json())
                        #self.counter = 0
			if (RNN_predicted_power > int(sys.argv[1]) and not self.migrated:
			       print("Migrating application")
                               threading.Thread(target=migrate, args=(sys.argv[2],)).start()
                               self.migrated = True
                               print(self.migrated)
                 
		else:
			if (self.counter == 10):
                		self.rnn_power_values.append(power_predicted)
				self.counter = 0
				print("RNN list len = " , len(self.rnn_power_values))
			else:
				self.counter = self.counter + 1

		f = open(sys.argv[3]+'.csv', 'a')
		f.write(time.ctime()+','+ str(info).strip('[]')+ "," + str(power_predicted) + "," + str(RNN_predicted_power) + "\n")
		f.close()
		
def migrate(script):
        output = subprocess.call(shlex.split(script))
        print(output)
        return

def main():
	f=open(sys.argv[3]+'.csv','a')
	f.write('timeStamp,currentCPUFrequency,userTime1Sec,percentCPU,interrupts,interruptsSoftware,numberOfProcesses,percentVirtualMemory,systemCalls,instructions,missRatio,DNNPredictedPower,RNNPredictedPower\n')
	f.close()

	sysObj = sysParam()
	i = 0 
	while (i < int(sys.argv[4])):
		try:
			sysObj.gatherData()
			i = i + 1
		except Exception as e:
			print("Failed " + str(e))
			pass

if __name__=="__main__":
	main()
