# Introduction #

# Details #

The current configuration for the anemometer uses a router and a RaspberryPi to connect to the anemometer and measure wind speed. The router creates a WAN network to which any user can connect. Users can connect to the network:
  * Network Name: AnemometroSonico
  * Password: AnemometroSonico

The RaspberryPi has been configured to have the static IP 192.168.0.139. This has been done following the information on the link: http://www.raspberryshake.com/raspberry-pistatic-ip-address/

Therefor, onced connected to the network AnemometroSonico, connect through SSH:
```
ssh -X pi@192.168.0.139
password: raspberry
```
-X is used in case it is necessary to plot the obtained fraimed from the anemometer.

Navigatation to the directory should be done through:
```
cd uch-ultrasonic-anemometer/software/build
```
Here, run the file `anemometer_example.py` to obtain measurements through the standard output:
```
python anemometer_example.py
```
Wind speeds should be read from the standard output.