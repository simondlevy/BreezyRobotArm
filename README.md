This repository contains a Python library and simple use-case for controlling a multi-jointed robot arm using
an Arduino microcontroller.  By using standard Python (instead of C++ or MicroPython), the library allows 
you to import and use other powerful Python libraries like [OpenCV](http://opencv.org/) to add intelligent 
behaviors to your robot.  

To get started, you should download and install [PyFirmata](https://github.com/tino/pyFirmata).  If you 
have a [Lynxmotion AL5](http://www.lynxmotion.com/c-124-al5a.aspx) arm (without wrist rotation) you should
be able to run the <b>LynxmotionAL5.py</b> example right away. As show in this [video](https://youtu.be/86_qCa1Hl9k),
this example will start the robot arm in an upright position, move it down and to the right, and then return
it to its original position.  Because the arm will move immediately to the initial position at the start of the
program, you should use caution when first running this program!


