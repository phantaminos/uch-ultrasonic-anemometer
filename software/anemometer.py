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

  def __init__(self, frames_per_measure=50):
    self.frames_per_measure = frames_per_measure
    pass

  def calibrate(self):
    """ This function must be called once for every particular piece of
        equipment. This must be called from an interactive terminal. The
        user is prompted to enter values of temperature, humidity, pressure and
        distance betweeen the ultrasonic transducers.
    """
    # Load data from the ADC
    reader = adc_reader.ADCReader()
    data = np.zeros((self.frames_per_measure, adc_reader.kFrameSize))
    reader.GetNFrames(data)
    
    echoes = []
    for number_of_frame in self.frames_per_measure:
      aux_echo = dpp.split_frame(data[number_of_frame])
      if aux_echo != None:
        echoes = echoes + aux_echo
  
    # Thermodynamic operations
    Rd = 287.04 # [J kg^-1 K^-1], Gas constant for dry air   
    Rv = 461.50 # [J kg^-1 K^-1], Gas constant for water vapor
    epsilon = Rd/Rv
    gamma = 1.4
  
    temperature = raw_input('Temperature in Celsius: ') # Temperature in celsius
    pressure = raw_input('Presure in [hPa]: ') # Pressure in hPa
    relative_humidity = raw_input('Relativ humidity as a decimal number in' + 
        + '[0,1]:') # Relative humidity as a decimal number in [0,1] interval

    distance = dict()
    # Create a dict with keys in flattened dpp.AXES, asking the user
    # len(dpp.AXES) times
    for direction in dpp.AXES:
      aux_distance = raw_input('Distance bewteen ' + ', '.join(direction) + 
          ' in [m]: ')
      for dir in direction:
        distance[dir] = aux_distance

    # According to Hyland and Wexler (1983), 173 - 473.
    e_sat =  np.exp(-0.58002206*(10**4)/temperature \
                  + 0.13914993*10*temperature**(0) \
  		     - 0.48640239*(10**-1)*temperature \
  		     + 0.41764768*(10**-4)*temperature**2 \
  		     - 0.14452093*(10**-7)*temperature**3 \
  		     + 0.65459673*10*np.log(temperature))/100
  
    r_sat = epsilon*e_sat/(pressure - e_sat)
    r = r_sat*relative_humidity
    virtual_temperature = temperature*(1 + r/epsilon)/(1 + r)
    speed_of_sound = np.sqrt(gamma*Rd*virtual_temperature)
    
    # Calculate the time of flight
    ToF = dict()
    for direction in dpp.CARDINAL_POINTS:
      ToF[direction] = distance[direction]/speed_of_sound
  
    # Load echoes and calculate the time delta in samples
    delta_in_samples = so.delta_samples(echoes, so.THRESHOLD, ToF)
    
    # Save calibration information into a file
    np.savez('delta_in_samples', delta_in_samples, dpp.CARDINAL_POINTS)
    np.savez('distance', distance, dpp.CARDINAL_POINTS)


  def measure_wind_speed(self):
    """ This function should be called every time the user wants to measure
        the wind speed. The return value is a list with the wind for every axis.
    """
    # Load data from the ADC
    reader = adc_reader.ADCReader()
    data = np.zeros((self.frames_per_measure, adc_reader.kFrameSize))
    reader.GetNFrames(data)
    
    echoes = []
    for number_of_frame in self.frames_per_measure:
      aux_echo = dpp.split_frame(data[number_of_frame])
      if aux_echo != None:
        echoes = echoes + aux_echo

    # Prepare the measurements by averaging, differentiating to remove the 
    # offset and normalizing to be able to easily use a threshold.
    echoes = so.normalize(so.differentiate(so.average(echoes)))
    
    # First, we calculate the number of samples until the echo meets the 
    # threshold
    samples_of_flight_threshold = so.samples_of_flight_threshold(echoes, 
                                                                 so.THRESHOLD)
  
    # Now we calculate the zero crossings to calculate the phase difference 
    # between the received echo and a reference echo.
    zeros = so.zero_crossings(echoes)
    
    arg = dict()
    speed = []
    ToF = dict()
  
    # Load calibration file
    delta_in_samples = np.load('delta_in_samples')
    distance = np.load('distance')

    for direction in dpp.CARDINAL_POINTS:
      # Calculate the index in zeros_xx corresponding to the zero crossings 
      # right before the threshold crossing.
      arg[direction] = np.argwhere(samples_of_flight_threshold[direction] >
                                      zeros[direction])[-1][-1]
  
      # Calculate the time of flight considering the use of the derivative.   
      ToF[direction] = (zeros[direction][arg[direction]] -
          delta_in_samples[direction] + dpp.EXCITATION_LENGTH + 
          dpp.EXCITATION_PERIOD/4)/dpp.SAMPLING_RATE
  
    # Create the list of speeds for each direction.
    for direction in dpp.AXES:
      speed.append((distance[direction[0]]/2)*(1/ToF[direction[0]] - 
          1/ToF[direction[1]]))
  
    return speed