# Internship
In the context of my internship, my mission was to characterize the anechoic chamber R2lab for the purpose of being able to evaluate wireless protocols inside of it. 
Thus this repository will contain the code to get values of the metric chosen, namely the received signal strength, and the scripts that I made to generate results.
NB: The code to get values of the RSSI is not mine. I nonless put it here because I made various modifications to it and because its result is used by the other scripts.
To take a look at the original code visit: https://github.com/parmentelat/r2lab/tree/public/demos/radiomap 

The generate RSSI folder contains the code that outputs values of RSSI from a ping experiment between the nodes of the lab.
For the results part;
First there is the RSSI characterization folder containing:
-A 2ghz 5ghz transmission bands comparison.
-The interactive heatamp plotted with plotly library to see how the signal behaves depending on the transmiter. 
-The daily change on the RSSI metric with timestamps.
Then there are experiments done:
-Assessing the antennas of nodes
-Describe the effet of calibration of wireless cards on the RSSI.
-Fitting the lab with known propagation models. 
