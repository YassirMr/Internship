#This script gives a grading of the antennas taking as input the node number, and the transmission power, and an argument for general (which stands for a sum of the rssi and deviding by the number: global assessing) or individual which brings what antenna is better for every experiment.

#source of distributions: https://docs.scipy.org/doc/scipy/reference/stats.html  : if i understand, i should look at pdf function, see how 
#many arguments it takes, and generate these arguments when fitting 

from argparse import ArgumentParser
from scipy import stats
from sklearn.metrics import mean_squared_error
import numpy as np
import matplotlib.pyplot as plt 
import operator

Tx = 1400  #transmission power
n = 1  #node number
total_power_ant_all = 0
total_power_ant0 = 0
total_power_ant1 = 0
total_power_ant2 = 0
power_of_antenna_all = []
power_of_antenna0 = []
power_of_antenna1 = []
power_of_antenna2 = []
parser = ArgumentParser()
parser.add_argument("-n", "--node", default=n, type=int,
                    help="specify the (receiver) node number, default={}"
                         .format(n))
parser.add_argument("-Tx", "--power", default=Tx, type=int,
                    help="specify a transmission power, default={}"
                         .format(Tx))
parser.add_argument("-gp", "--type", default='g', choices=['g','p'],
                    help="specify if general or particular comparison of antennas")
parser.add_argument("-d", "--distribution",default='', choices=['norm'], #'rice','rayleigh'
                    help="specify which distribution to fit the histrogram and compute the error")
args = parser.parse_args()

#for t in range(1,37):         parsing all the files
file = "./trace-T{}-r1-a7-t1-i0.008-S64-N100/rssi-{}.txt".format(args.power,args.node)  #the node receiving power from all others
fin=open(file , "r")
l =fin.readlines() 

del l[args.node-1] #remove the node-id line
if args.distribution=='norm':
 boo = True
else:
 boo =False

if args.type=='g':
 #for line in fin:
 for i in l:   #summing to get the total power received
  #l =fin.readline().split()
  total_power_ant_all += float(i.split()[2]) 
  total_power_ant0 += float(i.split()[3])
  total_power_ant1 += float(i.split()[4])
  total_power_ant2 += float(i.split()[5])

 average_power_ant_all = total_power_ant_all/36
 average_power_ant0 = total_power_ant0/36
 average_power_ant1 = total_power_ant1/36
 average_power_ant2 = total_power_ant2/36

 result = {'ant0':average_power_ant0,'ant-all': average_power_ant_all , 'ant2': average_power_ant2, 'ant1' : average_power_ant1 }
 sorted_g = sorted(result.items(), key=operator.itemgetter(1), reverse=True)
 print(sorted_g) #sorting the power and showing in general which antenna in a better receiver
elif args.type=='p':
 for i in l:
  result = ({'ant0':float(i.split()[3]),'ant-all': float(i.split()[2]) , 'ant2': float(i.split()[5]), 'ant1' : float(i.split()[4]) })
  sorted_p = sorted(result.items(), key=operator.itemgetter(1), reverse=True)
  print (sorted_p) #showing for each experiment which antenna was better 
  power_of_antenna_all.append(float(i.split()[2]))
  power_of_antenna0.append(float(i.split()[3]))
  power_of_antenna1.append(float(i.split()[4]))
  power_of_antenna2.append(float(i.split()[5]))
#ploting the histogram for each antenna:
 plt.subplot(221)
 n, bins, patches = plt.hist(power_of_antenna_all, 10, facecolor='blue',normed=boo)
 plt.title('Histogram of all antennas')
 plt.xticks(np.arange(-80, -25, 5))
 if args.distribution == 'norm':
  m, s = stats.norm.fit(power_of_antenna_all)
  pdf = stats.norm.pdf(np.arange(-80, -25, 5), m, s)
  plt.plot(np.arange(-80, -25, 5), pdf, label="normal distribution fitting")
  generated = stats.norm.rvs(m,s,len(power_of_antenna_all))
  print("Generated values by the {} distribution".format(args.distribution))
  print(generated)
  print("Mean square error of the fitting")
  print (mean_squared_error(power_of_antenna_all, generated)) 

 plt.subplot(222)
 n, bins, patches = plt.hist(power_of_antenna0, 10, facecolor='blue')
 plt.title('Histogram of antenna0')
 plt.xticks(np.arange(-80, -25, 5))

 plt.subplot(223)
 n, bins, patches = plt.hist(power_of_antenna1, 10, facecolor='blue')
 plt.title('Histogram of antenna1')
 plt.xticks(np.arange(-80, -25, 5))

 plt.subplot(224)
 n, bins, patches = plt.hist(power_of_antenna2, 10, facecolor='blue')
 plt.title('Histogram of antenna2')
 plt.xticks(np.arange(-80, -25, 5))

 #plt.savefig('Histogramms.png')
 plt.show()


'''
 elif args.distribution == 'rice':
  a,b,c = stats.rice.fit(power_of_antenna_all)
  pdf = stats.norm.pdf(np.arange(-80, -25, 5), a, b, c)
  plt.plot(np.arange(-80, -25, 5), pdf, label="Rice distribution fitting")
  generated = stats.norm.rvs(a,b,c,len(power_of_antenna_all))
  print("Generated values by the {} distribution".format(args.distribution))
  print(generated)
  print (mean_squared_error(power_of_antenna_all, generated))
'''
