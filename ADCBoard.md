# Introduction #

This board is in charge of digitizing the signals coming from the amplifier board.


# Interface #

This board has the following connectors.
  * **Analog Input**: This is the input port where the signal to be digitized is connected. The value captured by the ADC is the difference of both signals.
  * **Vref**: This output port is a constant signal at 2.5 volts that can be used as reference for the amplifier board to center the signals around this value.
  * **Power out and Chip Select**: This port provides 5 volts from the USB port to be connected to other boards. This also outputs the chip\_select signal from the SPI interface of the ADC. The start of a conversion is indicated by a falling edge on chip\_select. This signal is used by the microcontroller in the Excitation board to start a frame.

# Working Details #

This board is composed basically of two subsystems. First the analog-digital converter [ADC](http://en.wikipedia.org/wiki/Analog-to-digital_converter) takes as input an analog signal and transforms it into a digital representation that can be stored in a computer memory for further analysis. The digital interface of the ADC uses the [SPI](http://en.wikipedia.org/wiki/Serial_Peripheral_Interface_Bus) protocol. As most computers do not have external SPI ports and SPI-USB bridge is used to transmit this data using a standard USB port.

# Utilized ICs #

  * [FT2232](http://www.ftdichip.com/Support/Documents/DataSheets/ICs/DS_FT2232H.pdf) This FTDI ic is a general USB bridge. It can connect many different protocols to the USB port.
  * [ADC122S706](http://www.ti.com/lit/ds/symlink/adc122s706.pdf) This is an 12-bit 1 million samples per second adc.