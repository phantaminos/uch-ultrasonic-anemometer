# Introduction #

This page shows the necessary steps to obtain wind speed measurements from the standard output.


# Details #

Navigate to the /build folder, using:
```
cd uch-ultrasonic-anemometer/software/build
```

To operate the anemometer, it is first necessary to make a small adjustment, which should be run only once in a room with **no wind**. To do this, run
```
python calibrate.py
```
and follow the instructions. Temperature, air pressure, relative humidity, and distance between transducers will be asked.

To measure wind speed, run in the same directory:
```
python anemometer_example.py
```
This example file creates an instance of `anemometer.py`, which serves as a connection to the anemometer:
```
anemometer_connection = anemometer.Anemometer()
```
This connection is used to measure wind speed, using
```
anemometer_connection.measure_wind_speed()
```