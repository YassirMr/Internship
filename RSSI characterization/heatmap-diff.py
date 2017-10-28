# In order to easly look at The difference between heatmaps, this script is directly called by the heatmap.py script 
#and will display a heatmap difference of values.

from argparse import ArgumentParser
import plotly
import plotly.graph_objs as go
from plotly import tools

parser = ArgumentParser()
parser.add_argument("-i2", "--rss2", type=str)
parser.add_argument("-i1", "--rss1", type=str)
args = parser.parse_args()

rss2=(args.rss2).split('[')[1].split(']')[0]
rss1=(args.rss1).split('[')[1].split(']')[0]

lines=[]
for (j,i) in zip (rss2.split(','),rss1.split(',')):
 lines.append('{:02f}'.format(float(j)-float(i)))

trace = go.Scatter(  #displaying text (values), each couple (x,y) has a corresponding text value (x1,y1,text1) ainsi de suite
x = [0,1,2,3,4,5,6,7,8,0,1,2,3,4,5,6,7,8,0,1,2,3,4,5,6,7,8,0,1,2,3,4,5,6,7,8,0,1,2,3,4,5,6,7,8],
y = [0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4],
mode= 'text',
text = ["{}".format(lines[4]), "{}".format(lines[9]),"{}".format(lines[14]),"","","","{}".format(lines[29]),"{}".format(lines[34]),"{}".format(lines  [36]), "{}".format(lines[3]),"{}".format(lines[8]),"{}".format(lines[13]),"{}".format(lines[17]),"{}".format(lines[21]),"{}".format	(lines[24]),"{}".format(lines[28]),"{}".format(lines[33]),"{}".format(lines[35]),
"{}".format(lines[2]),"{}".format(lines[7]),"{}".format(lines[12]),"{}".format(lines[16]),"{}".format(lines[20]),"{}".format(lines[23]),"{}".format(lines[27]),"{}".format(lines[32]),"",
"{}".format(lines[1]),"{}".format(lines[6]),"{}".format(lines[11]),"","{}".format(lines[19]),"","{}".format(lines[26]),"{}".format(lines[31]),"",
"{}".format(lines[0]),"{}".format(lines[5]),"{}".format(lines[10]),"{}".format(lines[15]),"{}".format(lines[18]),"{}".format(lines[22]),"{}".format(lines[25]),"{}".format(lines[30]),""]
)
fig = tools.make_subplots(rows=1 , cols=1)
fig.append_trace(trace, 1, 1)
plotly.offline.plot(fig, filename="Diff")
