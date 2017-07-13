#This script is all about showing daily changes in the values of rssi between two nodes.

import sqlite3
import matplotlib.pyplot as plt
from argparse import ArgumentParser
import operator
conn = sqlite3.connect('my_database.db')
cursor = conn.cursor()
days = []
days2 = []
rss = [[] for i in range(1,5)]
rss2= [[] for i in range(1,5)]
T=14
r=6
parser = ArgumentParser()
parser.add_argument("-nr", "--node_r", default=2, type=int,
                    help="specify the receiver node, default={}"
                         .format(2))
parser.add_argument("-ns", "--node_s", default=1, type=int,
                    help="specify the sender node, default={}"
                         .format(1))
parser.add_argument("-T", "--power", default=T, type=int,
                    help="specify the transmission power, default={}"
                         .format(T))
parser.add_argument("-r", "--rate", default=r, type=int,
                    help="specify the transmission power, default={}"
                         .format(r))
args = parser.parse_args()
def list_sort(a):
 b=[]
 for i in a:
  b.append((int(i.split(":")[0].split("/")[0]),int(i.split(":")[0].split("/")[1]),int(i.split(":")[1].split("-")[0]),int(i.split(":")[1].split("-")[1])))
 b.sort(key=operator.itemgetter(1,0,2,3))
 del a[:]
 for t in b:
  a.append("{}/{}:{}-{}".format(t[0],t[1],t[2],t[3]))

cursor.execute("SELECT day FROM input WHERE frequency=2412 and transmission_power={} and rate={}".format(args.power,args.rate))

outcome = cursor.fetchall()

for d in outcome:
 days.append(d[0])
a=list(set(days))
list_sort(a)
a=a[-10:]

for i in a:
 cursor.execute("SELECT Rss_mrc,Rss_ant0,Rss_ant1,Rss_ant2  FROM input WHERE day='{}' and node_sender={} and node_receiver={} and frequency=2412 and transmission_power={} and rate={}".format(i,args.node_s,args.node_r,args.power,args.rate))
 tmp=cursor.fetchone()
 rss[0].append(tmp[0])
 rss[1].append(tmp[1])
 rss[2].append(tmp[2])
 rss[3].append(tmp[3])
#print("Rssi received in 2ghz")
#print(rss)


plt.figure(1)
plt.subplot(211)
my_xticks = []
b=range(1,len(a)+1)
for i in a:
 my_xticks.append(i)
plt.xticks(b, my_xticks,fontsize= 8)
plt.plot(b, rss[0], 'ro',linewidth=2.0, label="mrc")
plt.plot(b, rss[1], 'bo',linewidth=2.0, label="ant0")
plt.plot(b, rss[2], 'go',linewidth=2.0, label="ant1")
plt.plot(b, rss[3], 'mo',linewidth=2.0, label="ant2")
plt.legend()
plt.title('Node {} => Node {} in 2ghz'.format(args.node_s,args.node_r))
plt.ylabel('Received power (dBm)')

cursor.execute("SELECT day FROM input WHERE frequency=5180 and transmission_power={} and rate={}".format(args.power,args.rate))
outcome = cursor.fetchall()
for d in outcome:
 days2.append(d[0])
a=list(set(days2))
list_sort(a)
a=a[-10:]
b=range(1,len(a)+1)
#a.sort()
for i in a:
 cursor.execute("SELECT Rss_mrc,Rss_ant0,Rss_ant1,Rss_ant2 FROM input WHERE day='{}' and node_sender={} and node_receiver={} and frequency=5180 and transmission_power={} and rate={}".format(i,args.node_s,args.node_r,args.power,args.rate))
 tmp = cursor.fetchone()
 rss2[0].append(tmp[0])
 rss2[1].append(tmp[1])
 rss2[2].append(tmp[2])
 rss2[3].append(tmp[3])
#print("Rssi received in 5ghz")
#print(rss2)
conn.close()

plt.subplot(212)
my_xticks = []
for i in a:
 my_xticks.append(i)
plt.xticks(b, my_xticks,fontsize= 8)
plt.plot(b, rss2[0], 'ro',linewidth=2.0, label="mrc")
plt.plot(b, rss2[1], 'bo',linewidth=2.0, label="ant0")
plt.plot(b, rss2[2], 'go',linewidth=2.0, label="ant1")
plt.plot(b, rss2[3], 'mo',linewidth=2.0, label="ant2")
plt.legend()#bbox_to_anchor=(0.805, 1), loc=2, borderaxespad=0.)
plt.ylabel('Received power (dBm)')
plt.title('5ghz')
plt.xlabel('Time format D/M:H-M')
plt.show()
