# Introduction #

Add your content here.


# Details #

First it is necessary to solder the usb micro-b connector using a oven. Then all others smd components can be soldered using an soldering iron. Finally it is necessary to connect the wires between the modules as shown in the next figure:

![http://wiki.uch-ultrasonic-anemometer.googlecode.com/git/images/connections.jpg](http://wiki.uch-ultrasonic-anemometer.googlecode.com/git/images/connections.jpg)

To check that the usb bridge is working connect it to a computer running linux and run the command `dmesg`. The output should look like this:

```
[68090.784667] usb 2-1.2: new high-speed USB device number 65 using ehci-pci
[68090.877229] usb 2-1.2: New USB device found, idVendor=0403, idProduct=6010
[68090.877248] usb 2-1.2: New USB device strings: Mfr=1, Product=2, SerialNumber=0
[68090.877260] usb 2-1.2: Product: Dual RS232-HS
[68090.877272] usb 2-1.2: Manufacturer: FTDI
[68090.878117] ftdi_sio 2-1.2:1.0: FTDI USB Serial Device converter detected
[68090.878256] usb 2-1.2: Detected FT2232H
[68090.878270] usb 2-1.2: Number of endpoints 2
[68090.878281] usb 2-1.2: Endpoint 1 MaxPacketSize 512
[68090.878292] usb 2-1.2: Endpoint 2 MaxPacketSize 512
[68090.878303] usb 2-1.2: Setting MaxPacketSize 512
[68090.879240] usb 2-1.2: FTDI USB Serial Device converter now attached to ttyUSB0
[68090.879716] ftdi_sio 2-1.2:1.1: FTDI USB Serial Device converter detected
[68090.879816] usb 2-1.2: Detected FT2232H
[68090.879825] usb 2-1.2: Number of endpoints 2
[68090.879833] usb 2-1.2: Endpoint 1 MaxPacketSize 512
[68090.879841] usb 2-1.2: Endpoint 2 MaxPacketSize 512
[68090.879849] usb 2-1.2: Setting MaxPacketSize 512
[68090.880242] usb 2-1.2: FTDI USB Serial Device converter now attached to ttyUSB1
```

To load the firmware connect the avr programmer using the avr-isp port. Keep the adc connected to the computer.

![http://wiki.uch-ultrasonic-anemometer.googlecode.com/git/images/firmware_loading.jpg](http://wiki.uch-ultrasonic-anemometer.googlecode.com/git/images/firmware_loading.jpg)

Then in the folder `uch-ultrasonic-anemometer/hardware/firmware` execute the following commands:

```
make writefuses
make writeflash
```

Some boards have a slightly different version of the ATMega328 and the loading will complain that the signatures do not match. In that case edit the file /etc/avrdude.conf as described [here](http://forum.arduino.cc/index.php?topic=58670.0).