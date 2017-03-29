#This script gives a grading of the antennas taking as input the node number, and the transmission power, and 
#an argument for general (which stands for a sum of the rssi and deviding by the number: global assessing) or
#individual which brings what antenna is better for every experiment.

from argparse import ArgumentParser
import operator

Tx = 1400  #transmission power
n = 1  #node number
total_power_ant_all = 0
total_power_ant0 = 0
total_power_ant1 = 0
total_power_ant2 = 0

parser = ArgumentParser()
parser.add_argument("-n", "--node", default=n, type=int,
                    help="specify the node number, default={}"
                         .format(n))
parser.add_argument("-Tx", "--power", default=Tx, type=int,
                    help="specify a transmission power, default={}"
                         .format(Tx))
parser.add_argument("-gp", "--type", default='g', choices=['g','p'],
                    help="specify if general or particular comparaison")
args = parser.parse_args()

#for t in range(1,37):         parsing all the files
file = "./trace-T{}-r1-a7-t1-i0.008-S64-N100/rssi-{}.txt".format(args.power,args.node)  #the node receiving power from all others
fin=open(file , "r")
l =fin.readlines() 

del l[args.node-1] #remove the node-id line


if args.type=='g':
 for i in l:   #summing to get the total power received
  total_power_ant_all += float(i[20:26]) 
  total_power_ant0 += float(i[27:33])
  total_power_ant1 += float(i[34:40])
  total_power_ant2 += float(i[41:47])

 average_power_ant_all = total_power_ant_all/36
 average_power_ant0 = total_power_ant0/36
 average_power_ant1 = total_power_ant1/36
 average_power_ant2 = total_power_ant2/36

 result = {'ant0':average_power_ant0,'ant-all': average_power_ant_all , 'ant2': average_power_ant2, 'ant1' : average_power_ant1 }
 sorted_g = sorted(result.items(), key=operator.itemgetter(1), reverse=True)
 print(sorted_g) #sorting the power and showing in general which antenna in a better receiver
elif args.type=='p':
 for i in l:
  result = ({'ant0':float(i[27:33]),'ant-all': float(i[20:26]) , 'ant2': float(i[41:47]), 'ant1' : float(i[34:40]) })
  sorted_p = sorted(result.items(), key=operator.itemgetter(1), reverse=True)
  print (sorted_p) #showing for each experiment which antenna was better 



