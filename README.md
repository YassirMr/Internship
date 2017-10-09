In the context of my internship, my mission was to characterize the anechoic chamber R2lab for the purpose of being able
to evaluate wireless protocols inside of this wireless environment. Thus this repository will contain the code to get values of 
the chosen metric, 
namely the Received Signal Strength and the scripts that I made to generate results.
#### NB: The code to get values of the RSSI is in the generate RSSI folder, it is the modified version of the code that was initially present in the team. The original version can be accessed following this link: https://github.com/parmentelat/r2lab/tree/public/demos/radiomap
#### My modified version to make runs simultaneous optimizing the execution time and space the output is taking is in the report annex. 
### For the results first there is the RSSI characterization folder containing: 
* A 2ghz 5ghz transmission bands comparison.
* The interactive heatamp plotted with plotly library to see how the signal behaves depending on the transmiter, 
the frquency and the receiver antenna. 
* The daily change on the RSSI metric with timestamps. 
### Then each experiments condacted has a dedicated folder:
* Assessing the antennas of nodes 
* Describing the effet of calibration of wireless cards on the RSSI. 
* Fitting the lab with known propagation models.
* LOS identification. 
