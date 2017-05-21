This repository contains a Python library and simple use-case for controlling a multi-jointed robot arm using
an Arduino microcontroller.  By using standard Python (instead of C++ or MicroPython), the library allows 
you to import and use other powerful Python libraries like [NumPy](http://www.numpy.org/) and 
[OpenCV](http://opencv.org/) to add intelligent behaviors 
(e.g, [inverse kinematics](https://studywolf.wordpress.com/2013/04/11/inverse-kinematics-of-3-link-arm-with-constrained-minimization-in-python/) to your robot.  

To get started, you should download and install
[PyFirmata](https://github.com/tino/pyFirmata).  Once your robot arm is
connected to your Arduino, launch the Arduino IDE and upload the sketch in
<b>File/Exmaples/Firmata/StandardFirmata</b>.  If you have a [Lynxmotion
AL5](http://www.lynxmotion.com/c-124-al5a.aspx) arm (without wrist rotation)
you should be able to run the <b>LynxmotionAL5.py</b> example right away. As
show in this [video](https://youtu.be/86_qCa1Hl9k), this example will start the
robot arm in an upright position, move it down and to the right, and then
return it to its original position.  Because the arm will move immediately to
the initial position at the start of the program, you should use caution when
first running this program!

You can install the library for access from other directories by doing
<pre>
  python3 setup.py install
</pre>




