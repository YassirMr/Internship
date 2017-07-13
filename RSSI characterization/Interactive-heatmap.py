#This script will draw an interactive heatmap and give insight about the propagation inside R2lab.
# Execute it inside jupyter notebook

import plotly.plotly as py
from plotly.grid_objs import Grid, Column
import sqlite3
import time
import numpy as np
import operator

f=2412
T=14
conn = sqlite3.connect('my_database.db')
cursor = conn.cursor()
def list_sort(a):
 b=[]
 for i in a:
  b.append((int(i.split(":")[0].split("/")[0]),int(i.split(":")[0].split("/")[1]),int(i.split(":")[1])))
 b.sort(key=operator.itemgetter(1,0,2))
 del a[:]
 for t in b:
  a.append("{}/{}:{}".format(t[0],t[1],t[2]))

cursor.execute("SELECT day FROM input WHERE frequency={} and transmission_power={}".format(f,T))
outcome = cursor.fetchall()
days=[]
for d in outcome:
  days.append(d[0])
a=list(set(days))
list_sort(a)
x=np.arange(0,8,1)
y=np.arange(0,4,1)
my_columns=[Column(x, 'x'), Column(y, 'y')]
for i in range(1,38):
  raw=[]
  lines=[]
  cursor.execute("SELECT Rss_mrc FROM input WHERE day='{}' and node_sender={} and frequency={} and transmission_power={}".format(a[-1],i,f,T))
  raw.append(cursor.fetchall())
  for j in raw:
   for k in j:
    lines.append(k[0])
  z= [
["{}".format(lines[4]), "{}".format(lines[9]),"{}".format(lines[14]),"","","","{}".format(lines[29]),"{}".format(lines[34]),"{}".format(lines  [36])], ["{}".format(lines[3]),"{}".format(lines[8]),"{}".format(lines[13]),"{}".format(lines[17]),"{}".format(lines[21]),"{}".format(lines[24]),"{}".format(lines[28]),"{}".format(lines[33]),"{}".format(lines[35])],
["{}".format(lines[2]),"{}".format(lines[7]),"{}".format(lines[12]),"{}".format(lines[16]),"{}".format(lines[20]),"{}".format(lines[23]),"{}".format(lines[27]),"{}".format(lines[32]),""],
["{}".format(lines[1]),"{}".format(lines[6]),"{}".format(lines[11]),"","{}".format(lines[19]),"","{}".format(lines[26]),"{}".format(lines[31]),""],
["{}".format(lines[0]),"{}".format(lines[5]),"{}".format(lines[10]),"{}".format(lines[15]),"{}".format(lines[18]),"{}".format(lines[22]),"{}".format(lines[25]),"{}".format(lines[30]),""]
]
  my_columns.append(Column(z, 'z{}'.format(i)))
conn.close()
grid = Grid(my_columns)
py.grid_ops.upload(grid, 'values'+str(time.time()), auto_open=False)

data=[dict(type='heatmap',  #Create one heatmap here 
           xsrc=grid.get_column_reference('x'),
           ysrc=grid.get_column_reference('y'), 
           zsrc=grid.get_column_reference('z1'),
           zmin=-90,
           zmax=-20,
           zsmooth='best', 
           #colorscale=colorscale, 
           colorbar=dict(thickness=20, ticklen=4))]

title='Intractive heatmap'

layout = dict(title=title,
              autosize=False,
              height=600,
              width=600,
              hovermode='closest',
              xaxis=dict(range=[0, 8], autorange=False),
              yaxis=dict(range=[0, 4], autorange=False),
              showlegend=False,
              updatemenus=[dict(type='buttons', showactive=False,
                                y=1, x=-0.05, xanchor='right',
                                yanchor='top', pad=dict(t=0, r=10),
                                buttons=[dict(label='Play',
                                              method='animate',
                                              args=[None,
                                                    dict(frame=dict(duration=1000, 
                                                                    redraw=True),
                                                    transition=dict(duration=0),
                                                    fromcurrent=True,
                                                    mode='immediate')])])])

frames=[dict(data=[dict(zsrc=grid.get_column_reference('z{}'.format(k)),  #add the others here 
                        zmax=-20)],
                        traces=[0],
                        name='frame{}'.format(k),
                        ) for k in range(2,38)]
          
fig=dict(data=data, layout=layout, frames=frames)  
py.icreate_animations(fig, filename='animheatmap'+str(time.time()))
