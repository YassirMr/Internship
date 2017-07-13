import matplotlib.pyplot as plt
from argparse import ArgumentParser
import numpy as np
parser = ArgumentParser()


parser.add_argument("-e", "--exp", default=3, type=int,
                    help="specify which experience ")
args = parser.parse_args()
node_r=2
node_s=3
if args.exp==1: # spaces
 my_xticks = []
 timestamps=["3:12:50"] 
 timestamps.append("{}:{}:{}".format(3,12,55))

 for i in range(13,60):
  for j in [0,5,10,15,20,25,30,35,40,45,50,55]:
   timestamps.append("{}:{}:{}".format(3,i,j))

 for i in range(0,12):
  for j in [0,5,10,15,20,25,30,35,40,45,50,55]:
   timestamps.append("{}:{}:{}".format(4,i,j))
 for j in [0,5,10,15,20,25,30,35,40,45]:
  timestamps.append("{}:{}:{}".format(4,12,j))
 print(len(timestamps))
 
 filename= "./trace-freq2412-T1400-r6-a7-t1-i0.008-S64-N100-{}/result-{}.txt".format(args.exp,node_r)
 received_power=[]

 f = open(filename, 'r') 


 lines=f.readlines()


 for i in range(0,720):
  tmp=lines[i*100:i*100+100]
  tmp2=[]
  for j in tmp:
   tmp2.append(float(j.split()[2].split(',')[0]))
  received_power.append(sum(tmp2)/len(tmp2))

 b=range(1,len(received_power)+1)
 plt.plot(b,received_power , 'r',linewidth=2.0)
 for i in timestamps:
  my_xticks.append(i)
 plt.xticks(b[0::60], my_xticks[0::60],fontsize= 8)


 plt.xlabel('Time format H:MM:SS')
 plt.ylabel('Received power (dBm)')
 plt.title('Node {} => Node {} '.format(node_s,node_r))
 print("timestamps:")
 print(timestamps)
 print("received_power:")
 print(received_power)
 plt.savefig("figure1.png")
 #plt.show()

elif args.exp==2:
 timestamps=[]
 for i in range(30,51):
  for j in np.arange(0, 59.95, 0.05):
   timestamps.append("{}:{}".format(i,j))
 
 
 filename= "./trace-freq2412-T1400-r6-a7-t1205-i0.05-S64-N240000-{}/result-{}.txt".format(args.exp,node_r)
 received_power=[]
 timestamps=timestamps[0:len(received_power)+1]
 my_xticks=[]
 f = open(filename, 'r') 
 lines=f.readlines()
 for l in lines:
  received_power.append(l.split()[2].split(',')[0])
 b=range(1,len(received_power)+1)
 plt.plot(b,received_power , 'r',linewidth=2.0)
 for i in timestamps[0:len(received_power)+1]:
  my_xticks.append(i)
 plt.xticks(b[0::2000], my_xticks[0::2000],fontsize= 8)
 plt.xlabel('Time format MM:SS')
 plt.ylabel('Received power (dBm)')
 plt.title('Node {} => Node {} '.format(node_s,node_r))
 #plt.savefig("figure2.png")
 plt.show()
 
 

elif args.exp==3:
 my_xticks = []
 timestamps=[] #start "12:32:00"

 for i in range(32,60):
  for j in [0,5,10,15,20,25,30,35,40,45,50,55]:
   timestamps.append("{}:{}:{}".format(12,i,j))

 for i in range(0,60):
  for j in [0,5,10,15,20,25,30,35,40,45,50,55]:
   timestamps.append("{}:{}:{}".format(13,i,j))
 for i in range(0,42):
  for j in [0,5,10,15,20,25,30,35,40,45,50,55]:
   timestamps.append("{}:{}:{}".format(14,i,j))
 
 #timestamps.append("{}:{}:{}".format(14,32,0))
 timestamps=timestamps[0:1440]
 
 filename= "./trace-freq2412-T1400-r6-a7-t1-i0.008-S64-N100-{}/result-{}.txt".format(args.exp,node_r)
 received_power=[]

 f = open(filename, 'r') 


 lines=f.readlines()


 for i in range(0,2*720):
  tmp=lines[i*100:i*100+100]
  tmp2=[]
  for j in tmp:
   tmp2.append(float(j.split()[2].split(',')[0]))
  received_power.append(sum(tmp2)/len(tmp2))
 b=range(1,len(received_power)+1)


 filename= "./trace-freq2412-T1400-r6-a7-t1-i0.008-S64-N100-{}/noise{}.txt".format(args.exp,node_r)
 received_noise=[]

 f = open(filename, 'r') 
 lines=f.readlines()
 for l in lines:
  received_noise.append(l.split()[1])
 received_noise=received_noise[0:1440]
 print(len(timestamps))
 print(len(received_noise))
 print(len(received_power))

 plt.figure(1)
 plt.subplot(211)
 plt.plot(b,received_power , 'g',linewidth=2.0)
 plt.xlabel('Time format H:MM:SS')
 plt.title('Node {} => Node {} '.format(node_s,node_r))
 plt.ylabel('Received power (dBm)')
 for i in timestamps:
  my_xticks.append(i)
 plt.xticks(b[0::120], my_xticks[0::120],fontsize= 8)

 plt.subplot(212)
 plt.plot(b,received_noise , 'r',linewidth=2.0)
 plt.ylabel('Noise level (dBm)')
 plt.xlabel('Time format H:MM:SS')
 for i in timestamps:
  my_xticks.append(i)
 plt.xticks(b[0::120], my_xticks[0::120],fontsize= 8)
 plt.savefig("figure3.png")
 plt.show()
