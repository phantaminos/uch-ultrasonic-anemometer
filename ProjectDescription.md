# Introduction #

The aim of this project is to build an ultrasonic anemometer.

An ultrasonic anemometer works by sending pulses of sound through the air and measuring the corresponding time of flight (ToF). In this project the measurement is done in two ways over the same path to eliminate dependency on the air temperature.


# High Level Design #

This project is comprised of both hardware and software. The hardware must be able to excite the transducers and collect the echoes produced, then amplify and feed those signals to a computer using a standard USB interface. The software must analyze that signal, deduce the ToF in every measurement and then produce an estimation of the wind speed.

## Hardware Design ##

The hardware is composed by these basic components:
  * **Ultrasonic Transducers**: They transmit and capture pressure waves in the air.
  * **Drivers**: Inject a voltage signal into the transducer. The driver must have a high output impedance output that allows electrically disconnect the driver from the transducer so the output signal of the transducer can be perceived accordingly.
  * **Analog Switch**: Select which transducer signal is fed into the ADC to be sent to the computer.
  * **ADC**: This component transform an analog electrical signal into binary digital symbols.
  * **USB bridge**: This component allows to interface the ADC output interface (ISP) with the USB interface, so the computer can access the data produced by the ADC.
  * **Controller**: The controller is in charge of generating the control signals for the drivers and analog switch. It generate the 40kHz pulse that is applied to the transducers and also selects which signals are sent to the ADC for capture. The measuring sequence is started when a communication start signal is detected on the ADC ISP protocol.

![http://wiki.uch-ultrasonic-anemometer.googlecode.com/git/images/hardware_high_level.png](http://wiki.uch-ultrasonic-anemometer.googlecode.com/git/images/hardware_high_level.png)

# Future Work #

  * **Amplifier Stage**: Amplifiers must be moved near the transducers to diminish the noise caused by the length of the cable that connects them to the ADC. Also using one independent amplifier per transducer is highly recomended for the same reason.