from argparse import ArgumentParser
from scipy import stats
import math
import matplotlib.pyplot as plt


kth=[0,100,125,133]
sth=[0,-0.1,-0.1,-0.14]

ns=[26,19,33,32,32,31,36,26,37 , 26]  #   LOS
nr=[33,32,26,19,23,26,37,32,36 , 31]  #   Test

#ns=[11,10,10  ,33,35,16,19,36 ]  #   NLOS
#nr=[33,35,37 ,11,10,36,36,19]  #   Test


parser = ArgumentParser()
parser.add_argument("-r", "--rate", default=1, type=int,
                    help="having two experiences to try, default={}"
                         .format(1))
args = parser.parse_args()


def test(a, b):  # for skew
    if a < b:
        return 1    # "LOS according to skewness"
    else:
        return 0 #"NLOS according to skewness"


def test_k(a, b):
    if a > b:
        return 1 #"LOS according to k factor"
    else:
        return 0 #"NLOS according to k factor"

def skewness(a):
    b=[]
    for i in range(0,int(len(a)/10)):
        b.append(sum(a[i*10:(i+1)*10])/len(a[i*10:(i+1)*10]))
    return stats.skew(b)

def k_factor(a):
    b=[]
    for i in range(0,int(len(a)/10)):
        b.append(sum(a[i*10:(i+1)*10])/len(a[i*10:(i+1)*10]))
    n21 = [math.pow(10, i / 10) ** 2 for i in b]
    n41 = [math.pow(10, i / 10) ** 4 for i in b]
    n2 = (1 / len(b)) * (sum(n21))
    n4 = (1 / len(b)) * (sum(n41))
    k = (-2 * math.pow(n2, 2) + n4 - n2 * math.sqrt(2 * math.pow(n2, 2) - n4)) / (math.pow(n2, 2) - n4)
    return k
accuracy_s=[]
accuracy_k=[]
packets=range(100,2000,100)
for k in packets:
    test_skew = []
    test_kfactor = []
    for i,j in zip(ns,nr):  
        power_of_antenna0 = []
        power_of_antenna1 = []
        power_of_antenna2 = []
        file = "./trace-freq2412-T1400-r{}-a7-t9-i0.008-S64-N1000/result-{}.txt".format(args.rate,j)
        fin=open(file , "r")
        l =fin.readlines()

        if i<j:
            x=((i-1)*2000)+4
        else:
            x = ((i - 2) * 2000) + 4
        rss=l[x:x+k]   

        for t in rss:  

            power_of_antenna0.append(int(t.split()[2].split(',')[1]))
            power_of_antenna1.append(int(t.split()[2].split(',')[2]))
            power_of_antenna2.append(int(t.split()[2].split(',')[3]))


        test_skew.append(test(skewness(power_of_antenna0),sth[1]))
        test_kfactor.append(test_k(k_factor(power_of_antenna0),kth[1]))

        test_skew.append(test(skewness(power_of_antenna1),sth[2]))
        test_kfactor.append(test_k(k_factor(power_of_antenna1),kth[2]))

        test_skew.append(test(skewness(power_of_antenna2),sth[3]))
        test_kfactor.append(test_k(k_factor(power_of_antenna2),kth[3]))

    accuracy_k.append(sum(test_kfactor)/len(test_kfactor))
    accuracy_s.append(sum(test_skew)/len(test_skew))



plt.plot(packets,accuracy_s,'b-^',label="% skewness")
plt.plot(packets,accuracy_k,'g-^',label="% k-factor")
plt.suptitle("LOS",size=16)
plt.legend()
plt.ylabel("Percentage of accuracy")
plt.xlabel("Number of packets")
#plt.savefig('% LOS.png')
plt.show()
