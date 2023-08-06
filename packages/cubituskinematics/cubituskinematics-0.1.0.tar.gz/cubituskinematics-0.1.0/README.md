# Cubitus Kinematics Package

This is the custom made package for Cubitus Robotic Arm. This package includes matplotlib plotting as well as realtime data sending to the robotic arm itself.

## Installation

Run the following to install the package :

```console
$ pip install cubituskinematics
```

## Usage

First of all, you need to import cubituskinematics package/library into your project's python file.

```python
import cubituskinematics as ck
# or you could also use (but not recommended):
from cubituskinematics import *
```

Next you can test this package using simple commands as shown below :

#### Point
```python
# moves to one certain point in 3D space
ck.move_to_point(210, 0, 170)
```

> NOTE: if you want to know more about a function, hover on its name to reveal more information

#### Line
```python
# declare two points (each as a list)
A = [200, 0, 120]
B = [200, 0, 260]

# performs a line movement
ck.perform_line(A, B, sampling=10, repeat=1)
# use 'sampling' and 'repeat' arguments to determine sampling and number of repetitions
```

#### Circle
```python
# declare three points (each as a list)
A = [150, 0, 200]
B = [185, -80, 190]
C = [210, 30, 150]

# performs a circle movement
ck.perform_circle(A, B, C, sampling=10, repeat=1)
# use 'sampling' and 'repeat' arguments to determine sampling and number of repetitions
```

#### Parabola
```python
# define vertex point (defined as XZ relation, so it's a 2D point)
V = [160, 170]

# performs a parabolic movement
ck.perform_parabola(0.06, 40, V, sampling=10, repeat=1)
# use 'sampling' and 'repeat' arguments to determine sampling and number of repetitions
```

#### Bezier curve
```python
# declare three points (each as a list)
A = [230, 0, 140]
B = [280, 20, 280]
C = [240, 50, 150]

# performs a bezier curve movement
ck.perform_bezier(A, B, C, sampling=10, repeat=1)
# use 'sampling' and 'repeat' arguments to determine sampling and number of repetitions
```

#### Custom XML file

To use a custom-made .xml file you'll need to load it into the system like so :
> Note that your .xml file `MUST` be in the same folder as your .py script, otherwise fails to proceed !

```python
# declare a name of your .xml file
xml_name = "manipulator.xml" # or you can use just "manipulator"

# it is very important to have __file__ as a first argument as it indicates relative file path to your .xml file
ck.load_xml(__file__, xml_name)
```

### Simple User Interface Terminal

If you want to use user interface use one simple command as shown below :

```python
# opens user interface which acts like a simple command line terminal
ck.run_ui()
```

### Usage

After the command (shown above) is executed, the terminal should look like this.

```console
+------------- CUBITUS ROBOTIC ARM -------------+
|                 TUKE FEI KKUI                 |
+------------- USER INTERFACE v1.4 -------------+

    Enter 'help' to show list of all comands.
```

When you type 'help' as show below

```console
>> help
```

the list of all possible commands appears on the screen. Each of these commands can be used to interface with the robotic arm itself via command line terminal :

```console
>> help         Shows all commands.
>> loadxml      Loads user defined XML into system. (needs external command)
>> fold         Folds the arm to its initial position.
>> default      Sets the arm to its default (kinematic) pose.
>> grip         Sets gripper state to *hold* position. (default)
>> ungrip       Sets gripper state to *open* position.
>> eefangle     Sets end effector angle (X Y Z angles).
>> perform      Perform a specific movement based on input.
>> equation     Perform a custom curve based on input.
>> about        Show application info.
>> reset        Reset application.
>> clear        Clear terminal.
>> exit         Exit interface.
```

# CHANGELOG
All notable changes to this project will be documented here.

## [0.1.0] - 04/07/2021
### Description
- More minor improvements in code
- Fixed default pose plotting ( a bug in **ForwardKinematics.Plot()** function )
- In file `cubitus.xml` kinematic part label 'joint' was renamed to 'part'

## [0.0.9] - 03/26/2021
### Description
- Some minor improvements in code
- Fixed command 'clear' in **run_ui()** function ( bad lambda function syntax )
- Fixed raising UnreachablePositionError under certain conditions ( fixing bug in version 0.0.8 )

## [0.0.8] - 03/19/2021
### Description
- Fixed `cubitus.xml` file ( has incorrect translation values or in wrong order )
- Fixed 'point' shape ( has incorrectly set end effector angles for IK to calculate )
- Fixed 'grip' and 'ungrip' commands in **run_ui()** function
- Added new 'default' option in **run_ui()** user interface
- Some minor improvements in `Kinematics.py` ( less number of iterations in **InverseKinematics.Calculate()** function )

## [0.0.7] - 02/14/2021
### Description
- Added **fold_arm()** function to fold the arm to its initial (starting) position
- In **run_ui()** mode if 'reset' is typed into terminal it also executes new **fold_arm()** function mentioned above
- Fixed some bugs in **run_ui()** function ( eg. not properly functional 'point' argument in 'perform' )
- Fixed raising UnreachablePositionError when performing 'circle' ( end effector angles are now computed correctly )

## [0.0.6] - 02/06/2021
### Description
- Removed special character which contained all 'bezier' strings because of markdown text encoding problem
- Improved **set_end_effector()** function
- Added CHANGELOG at the end of `MARKDOWN.md`
- Fixed non-functional parabola example
- Fixed non-functional bezier example
- Fixed **PerformParabola()** function in `Core.py`

## [0.0.5] - 02/05/2021
### Description
- More of major code changes for better functionality
- Better UI ( more options, better user-asking algorithm, prettier 'about' strings )
- Added examples for each 'shape' ( the user now sees this examples in terminal )
- Major changes in `README.md` ( enriched by more examples )
- Modified **load_xml()** function ( fixed .xml file loading problem )

## [0.0.4] - 02/02/2021
### Description
- Bugfix release of this package ( added 'pyserial' into 'install_requires' args in `setup.py` )
- Some minor code changes for better functionality

## [0.0.3] - 02/02/2021
### Description
- Bugfix of previous release (0.0.2) of this package ( fixed module dependencies ) - now fully functional

## [0.0.2] - 02/01/2021
### Description
- Bugfix release of this package ( fixed module dependencies )

## [0.0.1] - 02/01/2021
### Description
- First release of this package ( no minor/major changes made yet )