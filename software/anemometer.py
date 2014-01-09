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
    self.data = np.zeros((self.frames_per_measurement, adc_reader.kFrameSize))
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
    for number_of_frame in range(self.frames_per_measurement):
      aux_echo = dpp.split_frame(self.data[number_of_frame])
      if aux_echo != None:
        echoes = echoes + aux_echo
  
    # Ask user for necessary data:
    # Temperature in celsius
    temperature = input('Temperature in Celsius: ')
    # Pressure in hPa
    pressure = input('Presure in [hPa]: ')
    # Relative humidity as a decimal number in [0,1] interval
    relative_humidity = input('Relative humidity in [0,1]: ')

    distance = dict()
    # Create a dict with keys in flattened dpp.AXES, asking the user
    # len(dpp.AXES) times
    for direction in dpp.AXES:
      aux_distance = input('Distance bewteen ' + ', '.join(direction) + 
          ' in [m]: ')
      for dir in direction:
        distance[dir] = aux_distance
    
    # Save calibration information (deltas and distance between transucers)
    # into a file
    delta_in_samples_aux = []
    distance_aux = []
    delta_in_samples = so.calibration(echoes,
                                      distance,
                                      temperature,
                                      pressure,
                                      relative_humidity)

    for direction in dpp.CARDINAL_POINTS:
      delta_in_samples_aux.append(delta_in_samples[direction])
      distance_aux.append(distance[direction])
      delta_in_samples_aux.append(delta_in_samples[direction])
    np.save('delta_in_samples.npy', delta_in_samples_aux)
    np.save('distance.npy', distance_aux)


  def measure_wind_speed(self):
    """ This function should be called every time the user wants to measure
        the wind speed. The return value is a list with the wind for every axis.
    """

    echoes = []
    # In the case when none of the frames pass the sanity check, echoes might be
    # an empty list.
    # Bug reported by Federico Flores on 09-01-2014. We must make sure that 
    # echoes is not an empty list.
    while len(echoes) == 0:
      # Load data from the ADC
      self.reader.GetNFrames(self.data)
  
      # Create echoes dict()
      for number_of_frame in range(self.frames_per_measurement):
        aux_echo = dpp.split_frame(self.data[number_of_frame])
        if aux_echo != None:
          echoes = echoes + aux_echo

    # Load calibration data
    delta_in_samples = dict()
    try:  
      delta_in_samples_aux = list(np.load('delta_in_samples.npy'))
    except IOError:
      print "Calibrate first! Run clibrate.py with no wind for calibration."
      exit(0)
    for direction in dpp.CARDINAL_POINTS:
      delta_in_samples[direction] = delta_in_samples_aux.pop(0)

    distance = dict()
    try:
      dist = np.load('distance.npy')
    except IOError:
      print "Calibrate first! Run calibrate.py with no wind for calibration."
      exit(0)
    dist = list(dist)
    for direction in dpp.CARDINAL_POINTS:
      distance[direction] = dist.pop(0)

    speed = so.calculate_wind_speed(echoes,
                                    so.THRESHOLD,
                                    delta_in_samples,
                                    distance)    
      
    return speed
