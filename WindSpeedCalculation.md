# Introduction #

Due to the crosstalk and noise introduced in the data acquisition stage, it has not been possible to determine the time of flight directly from the obtained echoes. A walkaround has been designed, which involves a calibration stage for each of the anemometers produced. The calibration is performed running:
```
python calibration.py
```
in a place with no wind. This script creates two files:
  * delta\_in\_samples.npy,
  * distance.npy.

These files contain the necessary information to perform the wind speed calculations.

# Details #

The method considers that the true time of flight can be calculated theoretically, using:
  * Temperature,
  * Air pressure,
  * Relative humidity.

The employed method considers that the speed of sound can be calculated through the expression:
```
speed_of_sound = √(gamma*Rd*virtual_temperature),
```
where:
  * gamma = 1.4 is a constant,
  * Rd = 287.04 [kg^-1 K^-1](J.md) is the gas constant for dry air.

---

TODO: Consider the definitions of virtual temperature and the variables that it depends on.

---

Having the speed of sound, the time of flight is a direct calculation considering that the calibration has been performed in a room with no wind speed.

The time of flight in the obtained echoes is calculated with the intersection of a threshold. The time of flight in the data is calculated at the first zero crossing of the echo right before the intersection with the echo.

The time `delta` between the first zero crossing before the threshold intersection and the theoretical time of flight is a constant for the anemometer (in each direction). This is considered the calibration (or adjustment) information, which is stored in `delta_in_samples.npy`.

As a summary, for each of the echoes, the time of flight is calculated in the zero crossing right before the intersection with the threshold. From this time of flight, the `delta` is substracted. This new time of flight is used to calculate the wind speed.