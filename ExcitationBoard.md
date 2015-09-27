# Introduction #

This board is in charge of exciting the ultrasonic transducers and output the corresponding signals to be read by the ADC.


# Interface #

This board has the following connectors.
  * **Power**: The power supply is connected into this module. This board need two voltage levels to operate. It needs 5 volts to supply power to the controller and controlling signals. It also needs a higher voltage in the VDD input to supply power to the transducers and the related electronics. This higher voltage range is used to excite the transducers because this increases the response, facilitating the signal treatment. This high voltage is also used to power up most of the signal-related electronic components, so it is limited by their tolerance. At this time a 12V VDD input is used.

  * **Transducers**: Every of the ports north, south, east, west, top and bottom may be connected to paired transducers (one facing the other). Each port has three connectors. The two connectors on the sides are for the two terminals of the transducer and the mid one is a ground connector that may be used with a shielded cable.

  * **Output**: This is a differential signal that is meant to be captured. The common mode voltage depends on the power supply voltage.
  * **Activation**: This input port must be connected to the chip\_select signal from the ADC ISP interface. On the falling edge of this signal the controller will start the capture of a single frame.
  * **Programming port**: This port is an standard AVR-ISP programming port used to upload the firmware into the controller.

<img src='http://wiki.uch-ultrasonic-anemometer.googlecode.com/git/images/exc-gimp.png' height='60%' width='60%' />

# Working Details #

This board is composed mainly by tree subsystems.

## Excitation/Driver ##

This subsystem is in charge of generating a strong enough signal to drive the transducers and also being able to disconnect electrically when the transducer is in the listening state in order to no interfere with the signal. To accomplish this a [H-bridge](http://en.wikipedia.org/wiki/H_bridge) is used. In a nutshell an H-bridge behaves like 4 switches connected on pairs on each side of the transducers as in the next figure:

![http://upload.wikimedia.org/wikipedia/commons/d/d4/H_bridge.svg](http://upload.wikimedia.org/wikipedia/commons/d/d4/H_bridge.svg)

When all four switches are in open state the transducer is in the listening state. When closed S1 and S4 the transducer is polarized in +VDD. When S2 and S3 are closed the transducer is polarized to -VDD. This way the transducer receives a signal that is in practice twice as much as the input voltage.

## Multiplexing ##

This subsystem simply selects which pair of signals are sent to the ADC. The multiplexer used is a two pole eight throw, similar to the one show in the figure:

![http://upload.wikimedia.org/wikipedia/commons/1/18/Diagram_of_2P6T_switch.png](http://upload.wikimedia.org/wikipedia/commons/1/18/Diagram_of_2P6T_switch.png)

The signals connected to this switch are one for every transducer plus one connected directly to the excitation pulse from the microcontroller.

## Control ##

This subsystem is in charge of generating the pulses to excite the transducers (through the drivers), and the control signals to select which driver is active and which signal the multiplexer selects as output.

# Utilized ICs #

  * [ATmega328](http://www.atmel.com/Images/doc8161.pdf) This is a programmable microcontroller that has the logic for the generation of signals on the corresponding sequences.
  * [sn754410](http://www.ti.com/lit/ds/slrs007b/slrs007b.pdf) The H-bridge acts as a buffer but the output voltage is different from the input voltage and the output can be selected to be high impedance.
  * [ADG5207](http://www.analog.com/static/imported-files/data_sheets/ADG5206_5207.pdf) Signal multiplexer.