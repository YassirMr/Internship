#This script will plot heatmaps of 2ghz and 5ghz depending on the database data set.

from argparse import ArgumentParser
from plotly import tools
import sqlite3
import plotly
import plotly.graph_objs as go
import operator
import subprocess

F = [2412,5180]
T=14
'''
In order to delete raws from the database
cursor.execute('DELETE FROM input WHERE day="14/5:20" and frequency={}'.format(args.freq))
'''
n = 1
r=6
in_for_diff=[]
parser = ArgumentParser()
parser.add_argument("-n", "--node", default=n, type=int,
                    help="specify the node number, default={}"
                         .format(n))
parser.add_argument("-T", "--power", default=T, type=int,
                    help="specify the transmission power, default={}"
                         .format(T))
parser.add_argument("-r", "--rate", default=r, type=int,
                    help="specify the transmission power, default={}"
                         .format(r))
parser.add_argument("-a", "--ant", default=-1, type=int,
                    help="specify the antenna, default={}"
                         .format(-1))
args = parser.parse_args()
def list_sort(a):
 b=[]
 for i in a:
  b.append((int(i.split(":")[0].split("/")[0]),int(i.split(":")[0].split("/")[1]),int(i.split(":")[1].split("-")[0]),int(i.split(":")[1].split("-")[1])))
 b.sort(key=operator.itemgetter(1,0,2,3))
 del a[:]
 for t in b:
  a.append("{}/{}:{}-{}".format(t[0],t[1],t[2],t[3]))

if args.ant==0:
    rss_chosen="Rss_ant0"
elif args.ant==1:
    rss_chosen = "Rss_ant1"
elif args.ant==2:
    rss_chosen = "Rss_ant2"
else:
     rss_chosen = "Rss_mrc"
conn = sqlite3.connect('my_database.db')
cursor = conn.cursor()
input_1=input("Select 1 if you want a heatmap comparaison between 2ghz and 5ghz \n       2 if you want heatmaps of the same frequency in two consecutive days: ")
if int(input_1)==2:
 days = []
 rss = []
 input_2=input("Available frequencies are: {} . Please select one: ".format(F))
 cursor.execute("SELECT day FROM input WHERE frequency={} and transmission_power={}  and rate={}".format(int(input_2),args.power,args.rate))
 outcome = cursor.fetchall()
 for d in outcome:
  days.append(d[0])
 a=list(set(days))
 list_sort(a)

 print("Available days :")
 print(a)
 input_var = input("Enter the day number format d1,d2 : ")
 for i in [a[int(input_var.split(',')[0])-1],a[int(input_var.split(',')[1])-1]]:
  raw = []
  cursor.execute("SELECT {} FROM input WHERE day='{}' and node_sender={} and frequency={} and transmission_power={} and rate={}".format(rss_chosen,i,args.node,int(input_2),args.power,args.rate))
  raw.append(cursor.fetchall())
  for j in raw:
   for k in j:
    rss.append(k[0])

 fig = tools.make_subplots(rows=1 , cols=2, subplot_titles=('D/M:H {}	   T {}	    freq {}'.format(a[int(input_var.split(',')[0])-1],args.power,int(input_2)),'D/M:H {}	   T {}     	freq {}'.format(a[int(input_var.split(',')[1])-1],args.power,int(input_2))))
 t = 1
 for day in range(0,2):
  lines=rss[day*37:day*37+37]
 #Here goes the plotting of the heatmap offline with a subplot
  lines[args.node-1] = "Sender"
  data = go.Heatmap(  #making a heatmap using plotly library (values are put in rows)
z= [
["{}".format(lines[4]), "{}".format(lines[9]),"{}".format(lines[14]),"","","","{}".format(lines[29]),"{}".format(lines[34]),"{}".format(lines  [36])], ["{}".format(lines[3]),"{}".format(lines[8]),"{}".format(lines[13]),"{}".format(lines[17]),"{}".format(lines[21]),"{}".format(lines[24]),"{}".format(lines[28]),"{}".format(lines[33]),"{}".format(lines[35])],
["{}".format(lines[2]),"{}".format(lines[7]),"{}".format(lines[12]),"{}".format(lines[16]),"{}".format(lines[20]),"{}".format(lines[23]),"{}".format(lines[27]),"{}".format(lines[32]),""],
["{}".format(lines[1]),"{}".format(lines[6]),"{}".format(lines[11]),"","{}".format(lines[19]),"","{}".format(lines[26]),"{}".format(lines[31]),""],
["{}".format(lines[0]),"{}".format(lines[5]),"{}".format(lines[10]),"{}".format(lines[15]),"{}".format(lines[18]),"{}".format(lines[22]),"{}".format(lines[25]),"{}".format(lines[30]),""]
],
zmin=-100,
zmax=0
)

  trace = go.Scatter(  #displaying text (values), each couple (x,y) has a corresponding text value (x1,y1,text1) ainsi de suite
x = [0,1,2,3,4,5,6,7,8,0,1,2,3,4,5,6,7,8,0,1,2,3,4,5,6,7,8,0,1,2,3,4,5,6,7,8,0,1,2,3,4,5,6,7,8],
y = [0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4],
mode= 'text',
text = ["{}".format(lines[4]), "{}".format(lines[9]),"{}".format(lines[14]),"","","","{}".format(lines[29]),"{}".format(lines[34]),"{}".format(lines  [36]), "{}".format(lines[3]),"{}".format(lines[8]),"{}".format(lines[13]),"{}".format(lines[17]),"{}".format(lines[21]),"{}".format	(lines[24]),"{}".format(lines[28]),"{}".format(lines[33]),"{}".format(lines[35]),
"{}".format(lines[2]),"{}".format(lines[7]),"{}".format(lines[12]),"{}".format(lines[16]),"{}".format(lines[20]),"{}".format(lines[23]),"{}".format(lines[27]),"{}".format(lines[32]),"",
"{}".format(lines[1]),"{}".format(lines[6]),"{}".format(lines[11]),"","{}".format(lines[19]),"","{}".format(lines[26]),"{}".format(lines[31]),"",
"{}".format(lines[0]),"{}".format(lines[5]),"{}".format(lines[10]),"{}".format(lines[15]),"{}".format(lines[18]),"{}".format(lines[22]),"{}".format(lines[25]),"{}".format(lines[30]),""]
)

  lines[args.node-1] = 0
  in_for_diff.append(lines)
  fig.append_trace(data, 1, t)
  fig.append_trace(trace, 1, t)
  t+=1

 conn.close()
 subprocess.run('python3 heatmap-diff.py -i2 "{}" -i1 "{}"'.format(in_for_diff[1],in_for_diff[0]),shell=True, check=True)
 subprocess.run('python3 noise-heatmap.py -r "{}" -T "{}" -f "{}" -d "{}" -n "{}"'.format(args.rate, args.power, input_2,a[int(input_var.split(',')[0])-1]+","+a[int(input_var.split(',')[1])-1],args.node), shell=True,
                check=True)
 plotly.offline.plot(fig, filename="freq {} n {} sender, ant=all, T={} dBm.html".format(input_2,args.node,args.power))

elif int(input_1)==1:
 t=1
 days = []
 days5 = []
 cursor.execute("SELECT day FROM input WHERE frequency={} and transmission_power={} and rate={}".format(F[0],int(args.power),args.rate))
 outcome1 = cursor.fetchall()
 cursor.execute("SELECT day FROM input WHERE frequency={} and transmission_power={} and rate={}".format(F[1],int(args.power),args.rate))
 outcome2 = cursor.fetchall()
 for d in outcome1:
  days.append(d[0])
 a = list(set(days))
 list_sort(a)
 for d in outcome2:
  days5.append(d[0])
 b = list(set(days5))
 list_sort(b)
 input_days = input("Choose a day number for 2ghz among {}".format(a))
 input_days5 = input("And a day for 5ghz {}".format(b))

 fig = tools.make_subplots(rows=1 , cols=2, subplot_titles=('D/M:H {}	    freq 2412	   T {}'.format(a[int(input_days)-1],args.power),'D/M:H {}     	freq 5180	    T {}'.format(a[int(input_days5)-1],args.power)))
 for f in F:
  raw = []
  rss = []
  if int(f)<3000:
    cursor.execute("SELECT {} FROM input WHERE day='{}' and node_sender={} and frequency={} and transmission_power={} and rate={}".format(rss_chosen,a[int(input_days)-1],args.node,f,args.power,args.rate))
  else:
      cursor.execute(
          "SELECT {} FROM input WHERE day='{}' and node_sender={} and frequency={} and transmission_power={} and rate={}".format(
              rss_chosen, b[int(input_days5) - 1], args.node, f, args.power,args.rate))
  raw.append(cursor.fetchall())
  for j in raw:
    for k in j:
     rss.append(k[0])

  lines = rss
  lines[args.node-1] = "Sender"

  data = go.Heatmap(  #making a heatmap using plotly library (values are put in rows)
z= [
["{}".format(lines[4]), "{}".format(lines[9]),"{}".format(lines[14]),"","","","{}".format(lines[29]),"{}".format(lines[34]),"{}".format(lines  [36])], ["{}".format(lines[3]),"{}".format(lines[8]),"{}".format(lines[13]),"{}".format(lines[17]),"{}".format(lines[21]),"{}".format(lines[24]),"{}".format(lines[28]),"{}".format(lines[33]),"{}".format(lines[35])],
["{}".format(lines[2]),"{}".format(lines[7]),"{}".format(lines[12]),"{}".format(lines[16]),"{}".format(lines[20]),"{}".format(lines[23]),"{}".format(lines[27]),"{}".format(lines[32]),""],
["{}".format(lines[1]),"{}".format(lines[6]),"{}".format(lines[11]),"","{}".format(lines[19]),"","{}".format(lines[26]),"{}".format(lines[31]),""],
["{}".format(lines[0]),"{}".format(lines[5]),"{}".format(lines[10]),"{}".format(lines[15]),"{}".format(lines[18]),"{}".format(lines[22]),"{}".format(lines[25]),"{}".format(lines[30]),""]
],
zmin=-100,
zmax=0
)

  trace = go.Scatter(  #displaying text (values), each couple (x,y) has a corresponding text value (x1,y1,text1) ainsi de suite
x = [0,1,2,3,4,5,6,7,8,0,1,2,3,4,5,6,7,8,0,1,2,3,4,5,6,7,8,0,1,2,3,4,5,6,7,8,0,1,2,3,4,5,6,7,8],
y = [0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4],
mode= 'text',
text = ["{}".format(lines[4]), "{}".format(lines[9]),"{}".format(lines[14]),"","","","{}".format(lines[29]),"{}".format(lines[34]),"{}".format(lines  [36]), "{}".format(lines[3]),"{}".format(lines[8]),"{}".format(lines[13]),"{}".format(lines[17]),"{}".format(lines[21]),"{}".format	(lines[24]),"{}".format(lines[28]),"{}".format(lines[33]),"{}".format(lines[35]),
"{}".format(lines[2]),"{}".format(lines[7]),"{}".format(lines[12]),"{}".format(lines[16]),"{}".format(lines[20]),"{}".format(lines[23]),"{}".format(lines[27]),"{}".format(lines[32]),"",
"{}".format(lines[1]),"{}".format(lines[6]),"{}".format(lines[11]),"","{}".format(lines[19]),"","{}".format(lines[26]),"{}".format(lines[31]),"",
"{}".format(lines[0]),"{}".format(lines[5]),"{}".format(lines[10]),"{}".format(lines[15]),"{}".format(lines[18]),"{}".format(lines[22]),"{}".format(lines[25]),"{}".format(lines[30]),""]
)
  lines[args.node-1] = 0
  in_for_diff.append(lines)
  fig.append_trace(data, 1, t)
  fig.append_trace(trace, 1, t)
  t+=1
  
 conn.close()
 subprocess.run('python3 heatmap-diff.py -i2 "{}" -i1 "{}"'.format(in_for_diff[1],in_for_diff[0]),shell=True, check=True)
 subprocess.run('python3 noise-heatmap.py -r "{}" -T "{}" -e "{}" -d "{}" -n "{}"'.format(args.rate,args.power,2,a[int(input_days) - 1]+","+b[int(input_days5) - 1],args.node), shell=True,
                check=True)
 plotly.offline.plot(fig, filename="freq {} n {} sender, ant=all, T={} dBm.html".format(F,args.node,args.power))
