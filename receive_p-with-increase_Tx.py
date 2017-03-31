#This script is about parsing the files of experiment result of rssi and get the value of rssi while the power is increased
#we want to display how rss value changes with the increase of power. (power : 5dbm..14dbm) with increment of 1
import numpy as np
import matplotlib.pyplot as plt
from argparse import ArgumentParser

n_s = 2  #sender node
n_r = 1  #receiver node
ant = 'all' #antenna taken
dict = {'all' : 2, 'ant0' : 3, 'ant1': 4, 'ant2': 5 }
Tx = np.arange(500,1500,100)
parser = ArgumentParser()
parser.add_argument("-nr", "--node_r", default=n_r, type=int,
                    help="specify the receiver node, default={}"
                         .format(n_r))
parser.add_argument("-ns", "--node_s", default=n_s, type=int,
                    help="specify the sender node, default={}"
                         .format(n_s))
parser.add_argument("-a", "--antenna", default=ant, choices=['all','ant0','ant1','ant2'],
                    help="specify which antenna, default={}".format(ant))
args = parser.parse_args()

received_power = []
for i in Tx:
 file = "./trace-T{}-r1-a7-t1-i0.008-S64-N100/rssi-{}.txt".format(i,args.node_r)
 fin = open(file , "r")
 lines = fin.readlines()
 received_power.append(lines[args.node_s-1].split()[dict[args.antenna]])

T = range(5,15)
plt.plot(T, received_power, 'ro')
plt.title('Node {} => Node {} using antenna {}'.format(args.node_s,args.node_r,args.antenna))
plt.xlabel('Tranmission power (dBm)')
plt.ylabel('Received power (dBm)')
plt.show()
#plt.savefig('n{} to n{}.png'.format(n_s,n_r))
