# Mobile\_Capstone
Pupil Player             |  Facial Recognition
:-------------------------:|:-------------------------:
![](http://pupil-labs.com/media/img/dev_front_crop.jpeg)  |  ![](http://www.rineypackard.com/images/facerecognition.png)
##Overview
This project is meant to help teacher's identify student's names in a classroom. It uses a pupil eye-tracker and facial detection/recognition algorithms to identify a potential student whose image/images already preloaded. 


##Launch Instructions
* Follow the instructions by [Pupil Lab's](https://github.com/pupil-labs/pupil/wiki/Setup#run-from-source) to set up pupil player software
* OpenCV/OpenBR are difficult to set up but are not needed if you are running the main.py on master
* cd gui
* ./gui.py to run with pupil (NOTE-Autofocus the pupil eye capture software before using it)
* ./gui.py [IMAGE] to run with sample image

##Running Instructions
* The first time you plugin the pupil, autofocus the eye. This window is automatically minimized on start up.
* In the gui, click on file, and choose class to choose what class you want to look in(class pictures must be in facial\_comparison directory. Each subdirectory should be the name of the person and contain photos that are numbered starting with 1
* In the gui, press enter to take a snapshot with the current class

##Face++ Instructions
* In the Face++ folder a file called train\_groups.py can be used to add classes, delete classes, and update classes. 
* NOTE-If there are issues with a class, you should delete the group using train\_groups.py(run python train\_groups.py to get usage information) 
* results.py contains a a file called results.py, run python results.py [CLASS\_NAME to get results about how accurately pictures are classified. Pictures are classified assuming that there is a directory called {CLASS\_NAME}\_test that contains test images for each person contained in the CLASS\_NAME directory


##Technologies
* Pupil Lab's open source pupil(hardware/software)
* FACE++ Facial Detection/Recognition
* OpenBR Facial Recognition
* OpenCV Facial Detection/Recognition
* TkInter Python GUI

##Repo Organization
* face\_comparison-Contains facial comparison code(OpenBR/OpenCV)
* face\_detection-Contains facial detection code(OpenCV)
* facepp-Contains Face++ Detection/Recognition/Training
* gui-contains the main program and the code to run the gui
* pupil-Contains are modified version of the pupil catpure software

Window

![gui](https://raw.github.com/DanielNoteboom/Mobile_Capstone/gui.png)







