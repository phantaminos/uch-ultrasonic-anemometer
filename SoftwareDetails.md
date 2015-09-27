# Introduction #

The software consists in two main modules: data\_preprocessing.py and signal\_operations.py. This page describes the job of each one of these modules and the way in which they interact.


# Details #
## Data Preprocessing ##
`data_preprocessing.py` preprocesses the information obtained from the ADC. This module is in charge of performing sanity check of the obtained frame and splitting the complete frame into the different echoes that are analized in order to calculate the wind speed.

The functionality `data_preprocessing.py` and `signal_operations.py` dependes strictly upon the number of ultrasonic transducers that are employed in the anemometer. The current development has considered 4 transducers, labeled in `data_preprocessing.py` as:
```
AXES = [['NORTH', 'SOUTH'], ['EAST', 'WEST']]
```
To include the transducers in the z axis, on should change the line to:
```
AXES = [['NORTH', 'SOUTH'], ['EAST', 'WEST'], ['TOP', 'BOTTOM']]
```
The code has been designed so that everything works if that line is changed (this is, only one line of code needs to be changed if the amount of transducers is changed).

`data_preprocessing.py` is in charge of two jobs:
  1. Sanity check: The integrity of the obtained frame must be checked before the calculation of wind speed.
  1. Frame splitting: The frame is splitted to obtain aligned echoes, so that the calculations may be performed adequately.

The signal coming from the ADC is as follows:

---

INSERT frame.png HERE!

---

When preprocessing the data coming from the ADC, the function `data_preprocessing.split_frame()` performs sanity check and returns the amount of echoes corresponding to the amount of directions in `AXES`. The obtained signals are displayed in the following figure:

---

INSERT echoes\_raw.png HERE!

---



## Data Processing ##
The module `signal_operations.py` is in charge of processing the echoes returned by the `data_preprocessing.py` module, as seen on the previous figure.

This module uses the function `calculate_wind_speed()` to calculate the wind speed from the received echoes. `calculate_wind_speed()` performs the following operations:
  * Average the received echoes to reduce noise from electronics and turbulence
  * Differentiate the echoes to remove the offset obtained from the crosstalk of electronics
  * Normalize the echoes in order to have a standard threshold in the interval [0,1]
  * Calculate the zero crossing of the signal riht before the intersection with the threshold
  * Calculate the time of flight considering the adjustment, the signal differentiation and the removed samples from the original frame. The time of flight is calculated in samples and transformed to seconds dividing it by `data_preprocessing.SAMPLING_RATE`.

At this point, it is important to give detail about the adjustment just mentioned. Due to problems in the data, it has not been possible to estimate the true time of flight directly from the data. Therefor, and adjustment applied to every measurement is calculated using `signal_operations.calibrate()`, using the interface in `anemometer.py`. This function calculates the theoretical time of flight using the current temprature in ˚C, air pressure in [hPa](hPa.md) and relative humidity in a fraction in the interval [0,1].