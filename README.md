The following is the repository containing code, data and tests collected throughout the project.

It has been used to store data continuously, and is generally unstructured. However, here's a rough overview of the different branches with meaningful content:
* test-11-23
This branch became the de facto "main" branch of most of the circuitpython code, including the code attached in the zip file in the report. 
It has been used for conducting various tests, usually assigned a folder for each dataset, including raw output data and in some cases the code and boot files.
It also contains test files for various smaller tests, such as testing tilt switch sensor configurations, or the RTC.
* measure-amps
This branch contains the majority of code used for performing the power consumption analysis, and consists of various test files written for the different configurations. 
The main test lies in the experiment 20-10 folder.
* electron-app-2
This branch contains the visualization tool, and is identical to the one attached for this project.
* data-processing
This branch contains python scripts used for generating most of the data in the data processing chapter, including the final classifiers. This would be used in conjunction with the Observable notebooks linked in the zip file readme.
* datagenerators
This branch contains earlier work in the data processing aspects, including some tests.
It contains the majority of mock data generators used in the visualization chapter. These are in large parts constructed with the help of ChatGPT, as mentioned in the thesis.

The other branches mostly contains ad hoc files used for one-time tests, and older work.
