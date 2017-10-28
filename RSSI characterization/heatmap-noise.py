#This script is directly called by the heatmap.py script and will draw heatmaps of noise.

from argparse import ArgumentParser
from plotly import tools
import plotly
import plotly.graph_objs as go
import sqlite3
F = [2412,5180]
T=14
r=6

parser = ArgumentParser()
parser.add_argument("-n", "--node", default=1, type=str,   #It is here only to get the position of noise in the list. position 0 is when 
                    help="specify the frequency, default={}"# node 1 was pinging etc..
                         .format(1))
parser.add_argument("-f", "--freq", default=2412, type=str,
                    help="specify the frequency, default={}"
                         .format(F))
parser.add_argument("-T", "--power", default=T, type=str,
                    help="specify the transmission power, default={}"
                         .format(T))
parser.add_argument("-r", "--rate", default=r, type=str,
                    help="specify the rate, default={}"
                         .format(r))
parser.add_argument("-d", "--day", type=str,
                    help="specify the day" )
parser.add_argument("-e", "--extra",default="-1")
args = parser.parse_args()

conn = sqlite3.connect('my_database.db')
cursor = conn.cursor()
if int(args.extra)>0:
    t=1
    fig = tools.make_subplots(rows=1, cols=2,
                              subplot_titles=('Noise f={}   T={}'.format(F[0], T), 'Noise f={}   T={}'.format(F[1], T)))
    for f in F:
        raw =[]
        lines=[]
        cursor.execute(
            "SELECT noise FROM input WHERE day='{}' and node_sender={} and frequency={} and transmission_power={} and rate={}".format(
                args.day.split(',')[t-1], int(args.node), f, int(args.power), int(args.rate)))
        raw.append(cursor.fetchall())
        for j in raw:
            for k in j:
                lines.append(k[0])
        data = go.Heatmap(
            z=[
                ["{}".format(lines[4]), "{}".format(lines[9]), "{}".format(lines[14]), "", "", "",
                 "{}".format(lines[29]), "{}".format(lines[34]), "{}".format(lines[36])],
                ["{}".format(lines[3]), "{}".format(lines[8]), "{}".format(lines[13]), "{}".format(lines[17]),
                 "{}".format(lines[21]), "{}".format(lines[24]), "{}".format(lines[28]), "{}".format(lines[33]),
                 "{}".format(lines[35])],
                ["{}".format(lines[2]), "{}".format(lines[7]), "{}".format(lines[12]), "{}".format(lines[16]),
                 "{}".format(lines[20]), "{}".format(lines[23]), "{}".format(lines[27]), "{}".format(lines[32]), ""],
                ["{}".format(lines[1]), "{}".format(lines[6]), "{}".format(lines[11]), "", "{}".format(lines[19]), "",
                 "{}".format(lines[26]), "{}".format(lines[31]), ""],
                ["{}".format(lines[0]), "{}".format(lines[5]), "{}".format(lines[10]), "{}".format(lines[15]),
                 "{}".format(lines[18]), "{}".format(lines[22]), "{}".format(lines[25]), "{}".format(lines[30]), ""]
            ],
            zmin=-100,
            zmax=-84
        )
        trace = go.Scatter(
            # displaying text (values), each couple (x,y) has a corresponding text value (x1,y1,text1) ainsi de suite
            x=[0, 1, 2, 3, 4, 5, 6, 7, 8, 0, 1, 2, 3, 4, 5, 6, 7, 8, 0, 1, 2, 3, 4, 5, 6, 7, 8, 0, 1, 2, 3, 4, 5, 6, 7,
               8, 0, 1, 2, 3, 4, 5, 6, 7, 8],
            y=[0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3,
               3, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            mode='text',
            text=["{}".format(lines[4]), "{}".format(lines[9]), "{}".format(lines[14]), "", "", "",
                  "{}".format(lines[29]), "{}".format(lines[34]), "{}".format(lines[36]), "{}".format(lines[3]),
                  "{}".format(lines[8]), "{}".format(lines[13]), "{}".format(lines[17]), "{}".format(lines[21]),
                  "{}".format(lines[24]), "{}".format(lines[28]), "{}".format(lines[33]), "{}".format(lines[35]),
                  "{}".format(lines[2]), "{}".format(lines[7]), "{}".format(lines[12]), "{}".format(lines[16]),
                  "{}".format(lines[20]), "{}".format(lines[23]), "{}".format(lines[27]), "{}".format(lines[32]), "",
                  "{}".format(lines[1]), "{}".format(lines[6]), "{}".format(lines[11]), "", "{}".format(lines[19]), "",
                  "{}".format(lines[26]), "{}".format(lines[31]), "",
                  "{}".format(lines[0]), "{}".format(lines[5]), "{}".format(lines[10]), "{}".format(lines[15]),
                  "{}".format(lines[18]), "{}".format(lines[22]), "{}".format(lines[25]), "{}".format(lines[30]), ""]
        )
        fig.append_trace(data, 1, t)
        fig.append_trace(trace, 1, t)
        t += 1
    plotly.offline.plot(fig, filename="noise.html")


else:
    freq=args.freq
    t = 1
    fig = tools.make_subplots(rows=1, cols=2,
                              subplot_titles=('Noise f={}   T={}'.format(freq, T), 'Noise f={}   T={}'.format(freq, T)))
    for d in [args.day.split(',')[0],args.day.split(',')[1]]:
        raw = []
        lines = []
        cursor.execute(
            "SELECT noise FROM input WHERE day='{}' and node_sender={} and frequency={} and transmission_power={} and rate={}".format(
                d, int(args.node), freq, int(args.power), int(args.rate)))
        raw.append(cursor.fetchall())
        for j in raw:
            for k in j:
                lines.append(k[0])
        data = go.Heatmap(
            z=[
                ["{}".format(lines[4]), "{}".format(lines[9]), "{}".format(lines[14]), "", "", "",
                 "{}".format(lines[29]), "{}".format(lines[34]), "{}".format(lines[36])],
                ["{}".format(lines[3]), "{}".format(lines[8]), "{}".format(lines[13]), "{}".format(lines[17]),
                 "{}".format(lines[21]), "{}".format(lines[24]), "{}".format(lines[28]), "{}".format(lines[33]),
                 "{}".format(lines[35])],
                ["{}".format(lines[2]), "{}".format(lines[7]), "{}".format(lines[12]), "{}".format(lines[16]),
                 "{}".format(lines[20]), "{}".format(lines[23]), "{}".format(lines[27]), "{}".format(lines[32]), ""],
                ["{}".format(lines[1]), "{}".format(lines[6]), "{}".format(lines[11]), "", "{}".format(lines[19]), "",
                 "{}".format(lines[26]), "{}".format(lines[31]), ""],
                ["{}".format(lines[0]), "{}".format(lines[5]), "{}".format(lines[10]), "{}".format(lines[15]),
                 "{}".format(lines[18]), "{}".format(lines[22]), "{}".format(lines[25]), "{}".format(lines[30]), ""]
            ],
            zmin=-100,
            zmax=-84
        )
        trace = go.Scatter(
            # displaying text (values), each couple (x,y) has a corresponding text value (x1,y1,text1) ainsi de suite
            x=[0, 1, 2, 3, 4, 5, 6, 7, 8, 0, 1, 2, 3, 4, 5, 6, 7, 8, 0, 1, 2, 3, 4, 5, 6, 7, 8, 0, 1, 2, 3, 4, 5, 6, 7,
               8, 0, 1, 2, 3, 4, 5, 6, 7, 8],
            y=[0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3,
               3, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            mode='text',
            text=["{}".format(lines[4]), "{}".format(lines[9]), "{}".format(lines[14]), "", "", "",
                  "{}".format(lines[29]), "{}".format(lines[34]), "{}".format(lines[36]), "{}".format(lines[3]),
                  "{}".format(lines[8]), "{}".format(lines[13]), "{}".format(lines[17]), "{}".format(lines[21]),
                  "{}".format(lines[24]), "{}".format(lines[28]), "{}".format(lines[33]), "{}".format(lines[35]),
                  "{}".format(lines[2]), "{}".format(lines[7]), "{}".format(lines[12]), "{}".format(lines[16]),
                  "{}".format(lines[20]), "{}".format(lines[23]), "{}".format(lines[27]), "{}".format(lines[32]), "",
                  "{}".format(lines[1]), "{}".format(lines[6]), "{}".format(lines[11]), "", "{}".format(lines[19]), "",
                  "{}".format(lines[26]), "{}".format(lines[31]), "",
                  "{}".format(lines[0]), "{}".format(lines[5]), "{}".format(lines[10]), "{}".format(lines[15]),
                  "{}".format(lines[18]), "{}".format(lines[22]), "{}".format(lines[25]), "{}".format(lines[30]), ""]
        )
        fig.append_trace(data, 1, t)
        fig.append_trace(trace, 1, t)
        t += 1
    plotly.offline.plot(fig, filename="noise.html")






