# Introduction #

This page describe the necessary procedures that must be performed to run the software of the anemometer on a Debian based Linux distribution (it applies to Raspberry Pi).


# Details #

This instructions assume that you can connect to the Raspberry using ssh. If you do not there are plenty of tutorials on Internet that can help you with that.

First download to your computer the library libmpsse version 1.3 from [here](https://code.google.com/p/libmpsse/downloads/detail?name=libmpsse-1.3.tar.gz&can=2&q=). Once in your computer copy this file to the raspberry with the command:

```
$ scp libmpsse-1.3.tar.gz pi@ip-address-raspberry:~
```

Where `ip-address-raspberry` corresponds to the IP address of the raspberry. Then connect to the raspberry using:

```
$ ssh pi@ip-raspberry
```

You will be asked to enter the password for the user pi. By default it is `raspberry`. Once inside, install the necessary packages with the following command:

```
$ sudo apt-get install libftdi-dev swig python2.7-dev
```

Then you should build and install libmpsse:

```
$ tar -zxvf libmpsse-1.3.tar.gz
$ cd libmpsse-1.3/src
$ ./configure
$ make
$ sudo make install
```

Finally allow non root users access to the anemometer hardware:

```
$ sudo su
# echo SUBSYSTEM==\"usb\", ATTRS{idVendor}==\"0403\", ATTRS{idProduct}==\"6010\", MODE:=\"0666\" > /etc/udev/rules.d/20-anemometer.rules
# depmod -ae
# exit
```