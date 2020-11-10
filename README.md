Optimize webpage design using eye tracking insights


What is Eye Tracking?
Eye tracking is the process of detecting and analysing eitherthe point of gaze or the motion of an eye relative to the head




'Eye-tracking’ software can give to help design a website.
Identify your site visitors are looking and for how long are theylooking. 
How the size and placement of various page items are affectingtheir attention.
What parts of the user interface do they miss



We are doing the project using two methods, using Python OpenCV and using WebGazer. 

In the first method, we are going to make a library specifically for gaze-tracking using Python.
-The first step is to detect the face of the user, and extract the eye-region from it and subsequently track the pupil movement . Then calibrated using this data and prediting the position where the person looks in the screen using linear regression.

In the second method, we create a web application that generates heatmap of the user's attention to a website using libraries WebGazer.js and heatmap.js. We create a calibration model to calculate accuracy of gaze points and we implement heatmaps using data obtained from WebGazer predictions.

Dataset used: 
The Eye Of The Typer Dataset (EOTT) - https://webgazer.cs.brown.edu/data/

Libraries:
https://github.com/pa7/heatmap.js.git

https://github.com/brownhci/WebGazer.git

https://github.com/antoinelame/GazeTracking

Video description of each member of this project is given in the given link:
https://drive.google.com/drive/folders/1BjcpvfFuSkkQNc7doHi6KpGm0T0C59ii?usp=sharing

We have divided our project and created seperate branches for each person and also additional branches to make them merge at the end of project.

javascript and python braches for merging our project done in python as well as javascript.

This project is done by 
                   
| Name | Working Branch |
| ------ | ------ |
| Marvel Varghese 17 | js-heatmaps |
| Kevin Paul K - 9| jscalib |
| Naveen K Biju - 36    | python|
|Lakshmi Harish Kumar - 14 |predictions|

