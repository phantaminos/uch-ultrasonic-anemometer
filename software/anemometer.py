#
# Copyright (C) 2013  UNIVERSIDAD DE CHILE.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http:#www.gnu.org/licenses/>.
#
# Authors: Luis Alberto Herrera <herrera.luis.alberto@gmail.com>


import adc_reader
import data_preprocessing as dpp
import signal_operations as so
import numpy as np

class Anemometer:
  """ Interface to the anemometer. This is the public interface for
      users of this library.
  """

  def __init__(self, frames_per_measurement = 100):
    self.frames_per_measurement = frames_per_measurement
    self.data = np.zeros((self.frames_per_measure, adc_reader.kFrameSize))
    self.reader = adc_reader.ADCReader()    

  def calibrate(self):
    """ This function must be called once for every particular piece of
        equipment. This must be called from an interactive terminal. The
        user is prompted to enter values of temperature, humidity, pressure and
        distance betweeen the ultrasonic transducers.
        Data is read from the ADC. The anemometer must be placed in an
        environment with no wind.
    """
    self.reader.GetNFrames(self.data)    
    
    echoes = []
    for number_of_frame in self.frames_per_measure:
      aux_echo = dpp.split_frame(self.data[number_of_frame])
      if aux_echo != None:
        echoes = echoes + aux_echo
  
    # Ask user fornecessary data
    # Temperature in celsius
    temperature = input('Temperature in Celsius: ')
    # Pressure in hPa
    pressure = input('Presure in [hPa]: ')
    # Relative humidity as a decimal number in [0,1] interval
    relative_humidity = input('Relativ humidity as a decimal number in' + 
        + '[0,1]:')

    distance = dict()
    # Create a dict with keys in flattened dpp.AXES, asking the user
    # len(dpp.AXES) times
    for direction in dpp.AXES:
      aux_distance = input('Distance bewteen ' + ', '.join(direction) + 
          ' in [m]: ')
      for dir in direction:
        distance[dir] = aux_distance
    
    # Save calibrate information (deltas and distance between transucers) into a
    # file
    so.calibration(echoes, distance, temperature, pressure, relative_humidity)
    np.savez('distance', distance, dpp.CARDINAL_POINTS)


  def measure_wind_speed(self):
    """ This function should be called every time the user wants to measure
        the wind speed. The return value is a list with the wind for every axis.
    """
    # Load data from the ADC
    self.reader.GetNFrames(self.data)
    
    echoes = []
    for number_of_frame in self.frames_per_measure:
      aux_echo = dpp.split_frame(self.data[number_of_frame])
      if aux_echo != None:
        echoes = echoes + aux_echo

    # Load calibration data
    delta_in_samples = np.load('delta_in_samples')
    distance = np.load('distance')

    speed = so.calculate_wind_speed(echoes,
                                    so.threshold,
                                    delta_in_samples,
                                    distance)    
      
    return speed
