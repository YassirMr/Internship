from argparse import ArgumentParser
from scipy import stats
import statistics
import math

kth=[0,100,125,133]
sth=[0,-0.1,-0.1,-0.14]
]

ns=[26,19,23,19,11]  #   LOS
nr=[33,32,32,23,23]  #   Test

ns=[6,12,10,5]  #   NLOS
nr=[27,33,30,37]  #   Test

power_of_antenna_all = []
power_of_antenna0 = []
power_of_antenna1 = []
power_of_antenna2 = []
parser = ArgumentParser()
parser.add_argument("-nr", "--node_r", default=12, type=int,
                    help="specify the (receiver) node number, default={}"
                         .format(12))
parser.add_argument("-ns", "--node_s", default=11, type=int,
                    help="specify the (receiver) node number, default={}"
                         .format(11))
parser.add_argument("-r", "--rate", default=1, type=int,
                    help="having two experiences to try, default={}"
                         .format(1))
parser.add_argument("-nu", "--number", default=1900, type=int,
                    help="number of samples, default={}"
                         .format(1900))
args = parser.parse_args()

file = "./trace-freq2412-T1400-r{}-a7-t9-i0.008-S64-N1000/result-{}.txt".format(args.rate,args.node_r)  #the node receiving power from all others
fin=open(file , "r")
l =fin.readlines()



if args.node_s<args.node_r:
    x=((args.node_s-1)*2000)+4
else:
    x = ((args.node_s - 2) * 2000) + 4
rss=l[x:x+args.number]


for t in range(0,int(args.number/10)):
 tmp1 = []
 tmp2 = []
 tmp3 = []
 tmp4 = []
 for i in rss[t*10:(t+1)* 10]:
  tmp1.append(int(i.split()[2].split(',')[0]))
  tmp2.append(int(i.split()[2].split(',')[1]))
  tmp3.append(int(i.split()[2].split(',')[2]))
  tmp4.append(int(i.split()[2].split(',')[3]))
 power_of_antenna_all.append(float(sum(tmp1)/len(tmp1)))
 power_of_antenna0.append(float(sum(tmp2)/len(tmp2)))
 power_of_antenna1.append(float(sum(tmp3)/len(tmp3)))
 power_of_antenna2.append(float(sum(tmp4)/len(tmp4)))

def test(a,b): #for skew
    if a<b:
        return "LOS according to skewness"
    else:
        return "NLOS according to skewness"
def test_k(a,b):
    if a>b:
        return "LOS according to k factor"
    else:
        return "NLOS according to k factor"
def k_factor(a):
    n21=[math.pow(10,i/10)**2 for i in a]
    n41 = [math.pow(10,i/10) ** 4 for i in a]
    n2=(1/len(a))*(sum(n21))
    n4=(1/len(a))*(sum(n41))
    k=(-2*math.pow(n2,2)+n4-n2*math.sqrt(2*math.pow(n2,2)-n4))/(math.pow(n2,2)-n4)

    return k

print("Rss_ant0: ")        
print("Skewness")
print(stats.skew(power_of_antenna0))
print(test(stats.skew(power_of_antenna0),sth[1]))
print("K factor")
print(k_factor(power_of_antenna0))
print(test_k(k_factor(power_of_antenna0),kth[1]))
print('')
print("Rss_ant1: ")        
print("Skewness")
print(stats.skew(power_of_antenna1))
print(test(stats.skew(power_of_antenna1),sth[2]))
print("K factor")
print(k_factor(power_of_antenna1))
print(test_k(k_factor(power_of_antenna1),kth[2]))
print('')
print("Rss_ant2: ")        
print("Skewness")
print(stats.skew(power_of_antenna2))
print(test(stats.skew(power_of_antenna2),sth[3]))
print("K factor")
print(k_factor(power_of_antenna2))
print(test_k(k_factor(power_of_antenna2),kth[3]))


