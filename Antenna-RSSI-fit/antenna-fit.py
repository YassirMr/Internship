#source of distributions: https://docs.scipy.org/doc/scipy/reference/stats.html 

from argparse import ArgumentParser
from scipy import stats
from sklearn.metrics import mean_squared_error
import numpy as np
import matplotlib.pyplot as plt 
import operator
import statistics



power_of_antenna_all = []
power_of_antenna0 = []
power_of_antenna1 = []
power_of_antenna2 = []
parser = ArgumentParser()
parser.add_argument("-n", "--node_s", default=5, type=int,
                    help="specify the (receiver) node number, default={}"
                         .format(9))
parser.add_argument("-d", "--distribution",default='norm', choices=['norm','rice','rayleigh'],
                    help="specify which distribution to fit the histrogram and compute the error")
args = parser.parse_args()


file = "./result-30.txt"  #the node receiving power from all others
fin=open(file , "r")
l =fin.readlines()

if args.node_s < 3:
    x=((args.node_s-1)*2000)+4
else:
    x = ((args.node_s - 2) * 2000) + 4
rss=l[x:x+1900]

for t in range(0,190):
 tmp1 = []
 tmp2 = []
 tmp3 = []
 tmp4 = []
 for i in rss[t*10:(t+1)*10]:
  tmp1.append(int(i.split()[2].split(',')[0]))
  tmp2.append(int(i.split()[2].split(',')[1]))
  tmp3.append(int(i.split()[2].split(',')[2]))
  tmp4.append(int(i.split()[2].split(',')[3]))

 power_of_antenna_all.append(float(sum(tmp1)/len(tmp1)))
 power_of_antenna0.append(float(sum(tmp2)/len(tmp2)))
 power_of_antenna1.append(float(sum(tmp3)/len(tmp3)))
 power_of_antenna2.append(float(sum(tmp4)/len(tmp4)))



#ploting the histogram for each antenna:
plt.subplot(221)
print("Mean value for ant=all is :{}".format(statistics.mean(power_of_antenna_all)))
print("Standard deviation for ant=all is :{}".format(statistics.stdev(power_of_antenna_all)))
n, bins, patches = plt.hist(power_of_antenna_all, 15, facecolor='blue',normed=True)
plt.title('Histogram of all antennas')
#x=np.arange(-78, -68, 2)
x=np.arange(sorted(power_of_antenna_all)[0], sorted(power_of_antenna_all)[-1], (sorted(power_of_antenna_all)[-1]-sorted(power_of_antenna_all)[0])/20)
plt.xticks(np.arange(sorted(power_of_antenna_all)[0], sorted(power_of_antenna_all)[-1],0.2)[0::2],np.arange(sorted(power_of_antenna_all)[0], sorted(power_of_antenna_all)[-1],0.2)[0::2])

if args.distribution=='norm':
 m, s = stats.norm.fit(power_of_antenna_all)
 pdf = stats.norm.pdf(x, m, s)
 plt.plot(x, pdf,'r-', label="normal distribution fitting")
 generated = stats.norm.rvs(m,s,len(power_of_antenna_all))
 #print("Generated values by the {} distribution".format(args.distribution))
 #print(generated)
 print("Mean square error of the fitting")
 print (mean_squared_error(power_of_antenna_all, generated))
 print(stats.kstest(power_of_antenna_all, 'norm',args=(m,s)))
 print("-------")
elif args.distribution == 'rice':
 a,b,c = stats.rice.fit(power_of_antenna_all)
 pdf = stats.rice.pdf(x, a, b, c)
 plt.plot(x, pdf, label="Rice distribution fitting")
 generated = stats.rice.rvs(a,b,c,len(power_of_antenna_all))
 #print("Generated values by the {} distribution".format(args.distribution))
 #print(generated)
 print("Mean square error of fitting:")
 print (mean_squared_error(power_of_antenna_all, generated))
 print(stats.kstest(power_of_antenna_all, 'rice', args=(a, b,c)))
 print("-------")
elif args.distribution == 'rayleigh':
 a,b= stats.rayleigh.fit(power_of_antenna_all)
 pdf = stats.rayleigh.pdf(x, a, b)
 plt.plot(x, pdf, label="Rayleigh distribution fitting")
 generated = stats.rayleigh.rvs(a,b,len(power_of_antenna_all))
 #print("Generated values by the {} distribution".format(args.distribution))
 #print(generated)
 print("Mean square error of fitting:")
 print (mean_squared_error(power_of_antenna_all, generated))
 print(stats.kstest(power_of_antenna_all, 'rayleigh', args=(a, b)))
 print("-------")

plt.subplot(222)
print("Mean value for ant=0 is :{}".format(statistics.mean(power_of_antenna0)))
print("Standard deviation for ant=0 is :{}".format(statistics.stdev(power_of_antenna0)))
n, bins, patches = plt.hist(power_of_antenna0, 15, facecolor='blue',normed=True)
plt.title('Histogram of antenna0')
#x=np.arange(-85, -79, 2)
x=np.arange(sorted(power_of_antenna0)[0], sorted(power_of_antenna0)[-1], (sorted(power_of_antenna0)[-1]-sorted(power_of_antenna0)[0])/20)
plt.xticks(np.arange(sorted(power_of_antenna0)[0], sorted(power_of_antenna0)[-1], 0.2)[0::2],np.arange(sorted(power_of_antenna0)[0], sorted(power_of_antenna0)[-1], 0.2)[0::2])


if args.distribution=='norm':
 m, s = stats.norm.fit(power_of_antenna0)
 pdf = stats.norm.pdf(x, m, s)
 plt.plot(x, pdf,'r-', label="normal distribution fitting")
 generated = stats.norm.rvs(m,s,len(power_of_antenna0))
 #print("Generated values by the {} distribution".format(args.distribution))
 #print(generated)
 print("Mean square error of the fitting")
 print (mean_squared_error(power_of_antenna0, generated))
 print(stats.kstest(power_of_antenna0, 'norm',args=(m,s)))
 print("-------")
elif args.distribution == 'rice':
 a,b,c = stats.rice.fit(power_of_antenna0)
 pdf = stats.rice.pdf(x, a, b, c)
 plt.plot(x, pdf, label="Rice distribution fitting")
 generated = stats.rice.rvs(a,b,c,len(power_of_antenna0))
 #print("Generated values by the {} distribution".format(args.distribution))
 #print(generated)
 print("Mean square error of fitting:")
 print (mean_squared_error(power_of_antenna0, generated))
 print(stats.kstest(power_of_antenna0, 'rice', args=(a, b, c)))
 print("-------")
elif args.distribution == 'rayleigh':
 a,b= stats.rayleigh.fit(power_of_antenna0)
 pdf = stats.rayleigh.pdf(x, a, b)
 plt.plot(x, pdf, label="Rayleigh distribution fitting")
 generated = stats.rayleigh.rvs(a,b,len(power_of_antenna0))
 #print("Generated values by the {} distribution".format(args.distribution))
 #print(generated)
 print("Mean square error of fitting:")
 print (mean_squared_error(power_of_antenna0, generated))
 print(stats.kstest(power_of_antenna0, 'rayleigh', args=(a, b)))
 print("-------")

plt.subplot(223)
print("Mean value for ant=1 is :{}".format(statistics.mean(power_of_antenna1)))
print("Standard deviation for ant=1 is :{}".format(statistics.stdev(power_of_antenna1)))
n, bins, patches = plt.hist(power_of_antenna1, 15, facecolor='blue',normed=True)
plt.title('Histogram of antenna1')
#x=np.arange(-80, -72, 2)
x=np.arange(sorted(power_of_antenna1)[0], sorted(power_of_antenna1)[-1], (sorted(power_of_antenna1)[-1]-sorted(power_of_antenna1)[0])/20)
plt.xticks(np.arange(sorted(power_of_antenna1)[0], sorted(power_of_antenna1)[-1], 0.2)[0::2],np.arange(sorted(power_of_antenna1)[0], sorted(power_of_antenna1)[-1], 0.2)[0::2])

if args.distribution=='norm':
 m, s = stats.norm.fit(power_of_antenna1)
 pdf = stats.norm.pdf(x, m, s)
 plt.plot(x, pdf,'r-', label="normal distribution fitting")
 generated = stats.norm.rvs(m,s,len(power_of_antenna1))
 #print("Generated values by the {} distribution".format(args.distribution))
 #print(generated)
 print("Mean square error of the fitting")
 print (mean_squared_error(power_of_antenna1, generated))
 print(stats.kstest(power_of_antenna1, 'norm', args=(m, s)))
 print("-------")
elif args.distribution == 'rice':
 a,b,c = stats.rice.fit(power_of_antenna1)
 pdf = stats.rice.pdf(x, a, b, c)
 plt.plot(x, pdf, label="Rice distribution fitting")
 generated = stats.rice.rvs(a,b,c,len(power_of_antenna1))
 #print("Generated values by the {} distribution".format(args.distribution))
 #print(generated)
 print("Mean square error of fitting:")
 print (mean_squared_error(power_of_antenna1, generated))
 print(stats.kstest(power_of_antenna1, 'rice', args=(a, b, c)))
 print("-------")
elif args.distribution == 'rayleigh':
 a,b= stats.rayleigh.fit(power_of_antenna1)
 pdf = stats.rayleigh.pdf(x, a, b)
 plt.plot(x, pdf, label="Rayleigh distribution fitting")
 generated = stats.rayleigh.rvs(a,b,len(power_of_antenna1))
 #print("Generated values by the {} distribution".format(args.distribution))
 #print(generated)
 print("Mean square error of fitting:")
 print (mean_squared_error(power_of_antenna1, generated))
 print(stats.kstest(power_of_antenna1, 'rayleigh', args=(a, b)))
 print("-------")

plt.subplot(224)
print("Mean value for ant=2 is :{}".format(statistics.mean(power_of_antenna2)))
print("Standard deviation for ant=2 is :{}".format(statistics.stdev(power_of_antenna2)))
n, bins, patches = plt.hist(power_of_antenna2, 15, facecolor='blue',normed=True)
plt.title('Histogram of antenna2')
#x=np.arange(-86, -80, 2)
x=np.arange(sorted(power_of_antenna2)[0], sorted(power_of_antenna2)[-1], (sorted(power_of_antenna2)[-1]-sorted(power_of_antenna2)[0])/20)
plt.xticks(np.arange(sorted(power_of_antenna2)[0], sorted(power_of_antenna2)[-1], 0.2)[0::2],np.arange(sorted(power_of_antenna2)[0], sorted(power_of_antenna2)[-1], 0.2)[0::2])

if args.distribution=='norm':
 m, s = stats.norm.fit(power_of_antenna2)
 pdf = stats.norm.pdf(x, m, s)
 plt.plot(x, pdf,'r-', label="normal distribution fitting")
 generated = stats.norm.rvs(m,s,len(power_of_antenna2))
 #print("Generated values by the {} distribution".format(args.distribution))
 #print(generated)
 print("Mean square error of the fitting")
 print (mean_squared_error(power_of_antenna2, generated))
 print(stats.kstest(power_of_antenna2, 'norm', args=(m, s)))
 print("-------")
elif args.distribution == 'rice':
 a,b,c = stats.rice.fit(power_of_antenna2)
 pdf = stats.rice.pdf(x, a, b, c)
 plt.plot(x, pdf, label="Rice distribution fitting")
 generated = stats.rice.rvs(a,b,c,len(power_of_antenna2))
 #print("Generated values by the {} distribution".format(args.distribution))
 #print(generated)
 print("Mean square error of fitting:")
 print (mean_squared_error(power_of_antenna2, generated))
 print(stats.kstest(power_of_antenna2, 'rice', args=(a, b, c)))
 print("-------")
elif args.distribution == 'rayleigh':
 a,b= stats.rayleigh.fit(power_of_antenna2)
 pdf = stats.rayleigh.pdf(x, a, b)
 plt.plot(x, pdf, label="Rayleigh distribution fitting")
 generated = stats.rayleigh.rvs(a,b,len(power_of_antenna2))
 #print("Generated values by the {} distribution".format(args.distribution))
 #print(generated)
 print("Mean square error of fitting:")
 print (mean_squared_error(power_of_antenna2, generated))
 print(stats.kstest(power_of_antenna2, 'rayleigh', args=(a, b)))
 print("-------")

plt.legend(bbox_to_anchor=(0.096, 2.2), loc=2, borderaxespad=0.)
plt.suptitle("{} > 30".format(args.node_s),size=16)
#plt.savefig('{} > 30 {}.png'.format(args.node_s,args.distribution))
plt.show()

