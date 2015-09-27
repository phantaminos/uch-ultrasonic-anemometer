# Introduction #

This board amplifies the small signals coming from the transducers while conditioning the amplified signal to voltage levels that are in the range of the ADC board input.


# Interface #

This board has the following connectors.
  * **Power Input K101**: Here it is necessary to connect the same supply voltage as the high voltage on the excitation board to VDD. Doing otherwise may damage this board. The REF pin is a high impedance input that must be connected to the reference voltage driven by the ADC board (usually 2.5V). The output signal will oscilate centered on this value.

  * **Sensor input P101**: Here must be connected the output from the excitation board. The differential value of this signal will be amplified in the output. It is important to respect the order in which the Sensors are connected (Sensor1 output from the excitation board must be connected to Sensor1 input of this board and the same for Sensor2). If this is not done, the diode which limits the output voltage to the ADC will be constantly leaking current, consuming power and heating.

  * **Output K102**: The OUT pin correspond to the amplified and trimmed version of the Sensor input signal. OUT is guaranteed to stay in the 0 - 5 Volts range. REF output is a copy of the REF input buffered by a Voltage Follower. These signals can be directly connected to the input of the ADC.


<img src='http://wiki.uch-ultrasonic-anemometer.googlecode.com/git/images/ampli-gimp.png' height='50%' width='50%' />


# Working Details #

This board main component is an INA2128 [Instrumentation Amplifier (IA)](http://en.wikipedia.org/wiki/Instrumentation_amplifier). This amplifiers are designed to amplify small **differential** transducer signals, rejecting their common mode to reduce noise.

The IA receives both the excitation signal and the response of the transducers, so it is powered with the maximum excitation voltage to avoid damage. It's amplification rate is selected using a single resistor following a chart specified in the Datasheet. Currently a 100 Ohm resistor is used, wich gives a Voltage Gain of approximately 500, since the transducers output signal is around 10mV.

In the output, the OUT signal is an amplified version of the original transducer response, centered around REF (in this version 2.5V), and trimmed to fit in a range between 4.7 and 0 Volts. This is done to protect the ADC because it only works in the 0-5V range.

To do the trimming a reversed 4.7V breakdown voltage [zener diode](http://en.wikipedia.org/wiki/Zener_diode) is used to leak current in case the voltage surpases it's value. This can happen because of the excitation signal amplification or an excess in the transducer signal amplification rate. A 1 kOhm resistor is connected in series to the amplifier output to limit the current leaked by the diode.

A buffer stage is requiered between the IA amplified output and the trimming circuit because it consumes a considerable amount of current (~100mA).

# Utilized ICs #

  * [INA2128](http://www.ti.com/lit/ds/sbos035a/sbos035a.pdf) Dual instrumentation amplifier from Texas Instrument.
  * [LT1010](http://cds.linear.com/docs/en/datasheet/1010fe.pdf) This power buffer can source/sink up to 150 mA.