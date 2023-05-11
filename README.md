# Guide of RoboTest

## Directory Structure

- __control__: Folder used to store the operation instruction files sent to the robotic arm
- __image__: Folder used to store files related to image processing
  - __flag__: Folder to store files used to mark the order in which the robotic arm performs operations
  - __input__: Folder used to store the image files captured by the camera and corrected and sharpened
  - __output__: Folder used to store the image files after processing the screen recognition and the image capture
  - __temp__: Folder used to store files of picture control extraction results
- __script__: Folder used to store the instruction control script files of the robotic arm
  - __explore.robo__: Folder used to store the converted script files of the auto exploration script
  - __xxx.robo__: Folder used to store the robotic arm control script file and corresponding screenshot files
- __atom_operation.py__: Used to generate atomic operations to control the robotic arm
- __auto_explore.py__: Used to perform robotic arm automation exploration
- __backend.py__: Used to start the backend of the RoboTest
- __cal_similarity.py__: Used to calculate image similarity
- __clear_environment.py__: Used to clean up temporary files before starting the backend of the robotic arm each time
- __connect_to_autoarm.py__: Used to set the parameters of the connected robot arm
- __notch_check.py__: Used to judge whether there is a special-shaped screen occlusion bug during replay
- __scale_coordinate.py__: Coordinate scaling calculation for cross-device replay
- __scheduling_strategy.py__: Scheduling strategy for performing automatic exploration of robotic arms
- __screen_recognition.py__: Used for screen recognition of the device under test
- __script_replay.py__: Used to perform script replay
- __take_screenshot.py__: Used to take screenshots of the screen of the device under test, and to correct and sharpen
- __transfer_with_autoarm.py__: Used to send and receive files with the robotic arm
- __widget_extraction.py__: Used for control identification and extraction of screenshots
- __widget_matching.py__: Used to match the control where the screen is clicked

## Environment Configuration

### Python Version and Mainly Used Packages

- __Python__: 3.6
- __opencv-contrib-python__: 3.4.2.16
- __opencv-python__: 3.4.2.16
- __Flask__: 2.0.3
- __Flask-Cors__: 3.0.10
- __paramiko__: 2.11.0

### Local Path and Parameter Settings

- __auto_explore.py__: Change _explore.txt_ and _explore.robo_ addresses to local addresses
- __backend.py__: Change _host\_ip_, _username_, _password_ according to the configuration of the robotic arm, change _length_, _width_, _depth_, _phone_size_ according to the information of the device under test, change _image\_input\_path_, _image\_output\_path_, _remote\_path_, _local\_path_, _flag\_path_, _control\_base\_path_, _script\_base\_path_ to the local actual addresses
- __clear\_environment.py__: Change the place where the address is involved in the code to the local actual address
- __connect\_to\_autoarm.py__: Change _host\_ip_, _username_, _password_ according to the configuration of the robotic arm
- __notch\_check.py__: Change _base\_file\_path_ to the local actual address
- __widget\_extraction.py__: Change _temp\_widget\_extraction\_res\_path_ to the local actual address

## How to Start

- __RoboTest back-end__: Take PyCharm to start the backend of RoboTest as an example, open the Run/Debug Configurations window, set the Script path to __backend.py__, and then click the run button.
- __RoboTest front-end__: The startup method of the front end is the same as that of a general Vue project. After installing the npm dependencies, run _npm run dev_ to run.
- __The robotic arm backend__: Execute the _TestRobot.py_ file in the _TestRobot_ directory to start the backend of the robotic arm. The specific code for operating the robotic arm and the backend code of the robotic arm should depend on the specific robotic arm model used.

## How to Use

### Script Recording

__step 0__: Execute _clear_environment.py_ to clear the temporary files left over from the last experiment.
__step 1__: The backend service of RoboTest and the one of the robotic arm have been successfully started.
__step 2__: Select _Start Recording_ in the front-end _Test Recording_, specify a _Script Name_ (we assume it is named _1_), RoboTest will generate a _1.robo_ folder under the _script_ directory, and generate a _1.txt_ in this folder to record the user's instructions to the robotic arm. 
__step 3__: RoboTest will call _take_screenshot.py_ to take a picture of the current device and correct and sharpen it. The processed picture will be stored in the _image/input_ directory in order.
__step 4__: RoboTest calls _screen_recognition.py_ to perform screen recognition on the device picture in _image/input_, and save the screenshot in the _image/output_ directory and in the _1.robo_ directory.
__step 5__: RoboTest displays the recognized screenshot on the front-end interface. Users preform __click__, __double\_click__, __long\_click__, or __slide__ operations on the screenshot, and RoboTest calls _atom\_operation.py_ to perform corresponding robotic arm atomic operations, and generates the control instruction in the _control_ directory. RoboTest writes the control instruction into the _1.txt_ file in the _1.robo_ directory.
__step 6__: Repeat steps from __step 3__ to __step 5__.

### Script Replaying

__step 0__: Execute _clear_environment.py_ to clear the temporary files left over from the last experiment.
__step 1__: The backend service of RoboTest and the one of the robotic arm have been successfully started.
__step 2__: Select _Test Replaying_ on the front-end interface, click _Choose Script_, and select the script file to be replayed(using _1.txt_ int the _1.robo_ directory as an example).
__step 3__: RoboTest will replay step by step based on the control instructions and corresponding screenshots in the _1.robo_ directory. The coordinates or widgets on the new device will be confirmed according to the method provided in _scale\_coordinate.py_ or _widget\_matching.py_. After all replay steps are completed, RoboTest will end the replay.

### Auto Exploration

__step 0__: Execute _clear_environment.py_ to clear the temporary files left over from the last experiment.
__step 1__: The backend service of RoboTest and the one of the robotic arm have been successfully started.
__step 2__: Select _Auto Exploration_ on the front-end interface, click _Create the auto exploration script_ and set _Execute exploration times_, _bottom left coordinates_ and _top right coordinates_. RoboTest will generate the corresponding script file under the _monkey.robo_ directory according to the set parameters, and at the same time, the front-end page will jump to _Test Replaying_.
__step 3__: Click _Choose Script_, and choose _monkey.txt_ in the _monkey.robo_ directory to be replayed. RoboTest performs auto exploration operations by calling _auto\_explore.py_, and the control instructions and screenshots corresponding to each operation step will be stored in the _explore.robo_ directory. The user can modify the call strategy in _auto\_explore.py_, and the call strategies that can be modified are written in _scheduling\_strategy.py_.

### Notch Detection

__step 0__: Execute _clear_environment.py_ to clear the temporary files left over from the last experiment.
__step 1__: The backend service of RoboTest and the one of the robotic arm have been successfully started.
__step 2__: Execute the auto exploration, the corresponding control instructions and screenshots will be stored in the _explore.robo_ directory, suspend the automatic exploration, and perform cross-device script replay on the generated auto exploration script, and detect whether there is a UI occlusion problem with the special-shaped screen by calling _notch_check.py_.
__step 3__: _notch_check.py_ compares the execution results of the same instruction on different devices by calling _cal_similarity.py_. If the image similarity is lower than the threshold, it will be considered that the UI occlusion problem of the special-shaped screen has occurred.
