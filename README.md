Optimize webpage design using eye tracking insights


What is Eye Tracking?
Eye tracking is the process of detecting and analysing eitherthe point of gaze or the motion of an eye relative to the head




'Eye-tracking’ software can give to help design a website.
Identify your site visitors are looking and for how long are theylooking. 
How the size and placement of various page items are affectingtheir attention.
What parts of the user interface do they miss



We are doing the project using two methods, using Python OpenCV and using WebGazer. 

In the first method, we are going to make a library specifically for gaze-tracking using Python.
-The first step is to detect the face of the user, and extract the eye-region from it and subsequently track the pupil movement from that region. The face and eye-region is detected by Haar Cascade classifier files and the pupil is tracked using blob detection algorithm. We create a calibration model to calculate accurate gaze points. This data from the calibration model is then put into a linear regression model to predict the gaze point.

Dataset used:
Haar Cascade Classifiers

In the second method, we create a web application that generates heatmap of the user's attention to a website using libraries WebGazer.js and heatmap.js. We create a calibration model to calculate accuracy of gaze points and we implement heatmaps using data obtained from WebGazer predictions.

Dataset used: 
The Eye Of The Typer Dataset (EOTT) - https://webgazer.cs.brown.edu/data/

Libraries:
https://github.com/pa7/heatmap.js.git

https://github.com/brownhci/WebGazer.git

We have divided our project and is done in different branches. Each person work in different branches.
Kevin Paul K works in jscalib
Lakshmi Harish Kumar works in python-calibration


This project is done by 
                   
| Name | Working Branch |
| ------ | ------ |
| Marvel Varghese 17 | js-heatmaps |
| Kevin Paul K - 9| jscalib |
| Naveen K Biju - 36    | python-pupiltracking|
|Lakshmi Harish Kumar - 14 |python-calibration|

