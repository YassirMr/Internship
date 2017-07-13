#This script is about plotting how the rssi decreases with the distance, we will do it for the lab with real distances and display other power decrease models along, then see which model best suits the lab. 
#Models considered: log distance model , two-ray model, telecom equation model , hata model
'''links to wikipedia page to find the mathematical formulas
https://fr.wikipedia.org/wiki/%C3%89quation_des_t%C3%A9l%C3%A9communications
https://en.wikipedia.org/wiki/Two-ray_ground-reflection_model
https://en.wikipedia.org/wiki/Log-distance_path_loss_model
'''

#plotting the signal decrease, n4 sender and the others in the same row receivers.
from argparse import ArgumentParser
import matplotlib.pyplot as plt 
import numpy as np
import scipy as sp
import scipy.stats
from math import *
from sklearn.metrics import mean_squared_error

ant = 'all' #antenna taken
Tx = 1400
F = 2412
row_nodes = [9,14,18,22,25,29,34,36]   # I took this row because it is the longest without any obstacle

row2_distance = np.arange(1.36,10.88,1.36)
row_distance = [log10(i) for i in row2_distance]
dict = {'all' : 2, 'ant0' : 3, 'ant1': 4, 'ant2': 5 }
gaindict = {'all' : 9, 'ant0' : 3, 'ant1': 3, 'ant2': 3 } #the value is gain antenna=5  cable loss= 2 
R_Tequation = []
R_logdistance = []
R_2ray = []
dicto = {2412:1 , 5180:6 }
parser = ArgumentParser()
parser.add_argument("-f", "--freq", default=F, type=int,
                    help="specify the frequency, default={}"
                         .format(F))
parser.add_argument("-Tx", "--power", default=Tx, type=int,
                    help="specify a transmission power, default={}"
                         .format(Tx))
parser.add_argument("-a", "--antenna", default=ant, choices=['all','ant0','ant1','ant2'],
                    help="specify which antenna, default={}".format(ant))
args = parser.parse_args()
received_power = []

for d in row_nodes:
 file = "./trace-freq{}-T{}-r{}-a7-t1-i0.008-S64-N100/rssi-{}.txt".format(args.freq,args.power,dicto[args.freq],d)  #local path
 fin = open(file , "r")
 wanted = fin.readlines()
 received_power.append(float(wanted[3].split()[dict[args.antenna]])) #4th row in each file 


plt.plot(row_distance, received_power, 'ro', label="r2lab")
plt.title('Node sender: 4 freq={} Tx={} dBm'.format(args.freq,int(args.power/100)))
plt.xlabel('Distance : log(meters)')
plt.ylabel('Received power (dBm)')

#ploting the two ray model (gain taken 5dBi for each antenna) (he=hr=1m)
for i in row2_distance: 
 R_2ray.append(int(args.power/100)-40*log10(i)+10*log10(gaindict[args.antenna]))

plt.plot(row_distance, R_2ray, 'yo',label="2ray")

#ploting the log distance path loss model, (gamma=2 , Xg=0)

for i in row2_distance:
 R_logdistance.append(int(args.power/100)-10*2*log10(i/1.36)+(float(received_power[0])-float(args.power/100)))
 
plt.plot(row_distance, R_logdistance, 'b^',label="log distance")
print('Mean square error r2lab/log: {}'.format(mean_squared_error(received_power,R_logdistance)))


#ploting the telecom equation model
for i in row2_distance:
 R_Tequation.append(int(args.power/100)+gaindict[args.antenna]+gaindict[args.antenna]-(35.45+20*log10(args.freq)+20*log10(i/1000)))
plt.plot(row_distance, R_Tequation, 'g^',label="Telecom equ")


plt.legend(bbox_to_anchor=(0.8, 1), loc=2, borderaxespad=0.) #1.05
#Here the confidence bounds are computed
#def mean_confidence_interval(data, confidence=0.95):
confidence=0.95
a = 1.0*np.array(received_power)
n = len(a)
m, se = np.mean(a), scipy.stats.sem(a)
h = se * sp.stats.t._ppf((1+confidence)/2., n-1)
plt.plot([row_distance[0],row_distance[-1]],[m-h,m-h],'r')
plt.text(row_distance[-1], m-h, 'lower confidence bound',fontsize=8)
plt.plot([row_distance[0],row_distance[-1]],[m+h,m+h],'r')
plt.text(row_distance[-1], m+h, 'higher confidence bound',fontsize=8)
plt.show()
