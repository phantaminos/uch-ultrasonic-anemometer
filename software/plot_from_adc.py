""" Example of how to use adc_reader. It will plot one frame. """

import adc_reader
import numpy as np

import pylab

def main():
  """ Reads data from the ADC and plots it on screen. """
  data = np.zeros(10000)

  reader = adc_reader.ADCReader()
  reader.GetFrame(data)

  pylab.plot(data)
  pylab.show()


if __name__ == "__main__":
  main()


