# RevealingThief

### Description
Arduino project syncing with Python through pyserial, this is a home safety project that captures a photo of invader upon detection of light above certain threshold. 

## Tech Stack
- **Frontend:** 
- **Backend:** C++, Python
- **Database:** 
- **Hardware:** Arduino Uno
- **Other Tools:**  pyserial, cv

## Features
- Light detection sensor (Photoresistor) is used to capture the invasion of thief that uses lights.
- Upon detection of lights, the comptuer opens a camera and takes a photo and saves to cloud directory.
- Shows the taken photo in the monitor to notify the thief that their face is exposed.

### Installation
this command will install python packs
pip install -r requirements.txt

run app.py python file for taking photos

run exposeandshow.py python file for captioning photo and sharing it to cloud onedrive

also change the variable ONEDRIVE_FOLDER to your own onedrive dir

run following file and install it to your arduino
sketch_feb24a
