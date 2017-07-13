from argparse import ArgumentParser
from scipy import stats
from sklearn.metrics import mean_squared_error
import numpy as np
import matplotlib.pyplot as plt 
import operator
import statistics

F = 2412
Tx = 900
nr=4
total_power_ant_all = 0
total_power_ant0 = 0
total_power_ant1 = 0
total_power_ant2 = 0
power_of_antenna_all = []
power_of_antenna0 = []
power_of_antenna1 = []
power_of_antenna2 = []




file = "./3>{}/trace-freq2412-T900-r1-a1-t1-i0.008-S64-N100/result-{}.txt".format(nr,nr) 
fin=open(file , "r")

lines =fin.readlines() 

for i in range(0,99):
  tmp=lines[i*100:i*100+100]
  tmp2=[]
  tmp3=[]
  tmp4=[]
  tmp5=[]
  for j in tmp:
   tmp2.append(float(j.split()[2].split(',')[0]))
   tmp3.append(float(j.split()[2].split(',')[1]))
   tmp4.append(float(j.split()[2].split(',')[2]))
   tmp5.append(float(j.split()[2].split(',')[3]))
  power_of_antenna_all.append(sum(tmp2)/len(tmp2))
  power_of_antenna0.append(sum(tmp3)/len(tmp3))
  power_of_antenna1.append(sum(tmp4)/len(tmp4))
  power_of_antenna2.append(sum(tmp5)/len(tmp5))

#ploting the histogram for each antenna:
plt.subplot(221)
print("Mean value for ant=all is :{}".format(statistics.mean(power_of_antenna_all)))
print("Standard deviation for ant=all is :{}".format(statistics.stdev(power_of_antenna_all)))
n, bins, patches = plt.hist(power_of_antenna_all, 10, facecolor='blue')
plt.title('Histogram of all antennas')
#plt.xticks(np.arange(-64, -50, 5))
plt.xticks(np.arange(-80.3, -36.3, 5))


plt.subplot(222)
print("Mean value for ant=0 is :{}".format(statistics.mean(power_of_antenna0)))
print("Standard deviation for ant=0 is :{}".format(statistics.stdev(power_of_antenna0)))
n, bins, patches = plt.hist(power_of_antenna0, 10, facecolor='blue')
plt.title('Histogram of antenna0')
plt.xticks(np.arange(-80.3, -36.3, 5))

plt.subplot(223)
print("Mean value for ant=1 is :{}".format(statistics.mean(power_of_antenna1)))
print("Standard deviation for ant=1 is :{}".format(statistics.stdev(power_of_antenna1)))
n, bins, patches = plt.hist(power_of_antenna1, 10, facecolor='blue')
plt.title('Histogram of antenna1')
plt.xticks(np.arange(-80.3, -36.3, 5))

plt.subplot(224)
print("Mean value for ant=2 is :{}".format(statistics.mean(power_of_antenna2)))
print("Standard deviation for ant=2 is :{}".format(statistics.stdev(power_of_antenna2)))
n, bins, patches = plt.hist(power_of_antenna2, 10, facecolor='blue')
plt.title('Histogram of antenna2')
plt.xticks(np.arange(-80.3, -36.3, 5))

plt.savefig('Histogramms3>{}.png'.format(nr))
plt.show()

