# Internship
In the context of my internship, my mission was to characterize the anechoic chamber R2lab for the purpose of being able to evaluate wireless protocols inside of it. 
Thus this repository will contain the code to get values of the metric chosen, namely the received signal strength, and the scripts that I made to generate results.
NB: The code to get values of the RSSI is not mine. It can be accessed following this link: https://github.com/parmentelat/r2lab/tree/public/demos/radiomap 


First there is the RSSI characterization folder containing:
-A 2ghz 5ghz transmission bands comparison.
-The interactive heatamp plotted with plotly library to see how the signal behaves depending on the transmiter, the frquency, the receiver antenna. 
-The daily change on the RSSI metric with timestamps.
Then there are experiments done:
-Assessing the antennas of nodes
-Describe the effet of calibration of wireless cards on the RSSI.
-Fitting the lab with known propagation models. 
