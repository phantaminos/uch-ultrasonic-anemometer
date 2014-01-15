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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors: Karel Mundnich <kmundnic@ing.uchile.cl>

import data_preprocessing as dpp
import numpy as np

THRESHOLD = dict()
for direction in dpp.CARDINAL_POINTS:
  THRESHOLD[direction] = 0.3

def average(echoes):
  """ Average echoes on an echo data structure (list of dictionaries) and
      return a dict containing the averaged signals.
  """
  assert len(echoes) > 0
  
  # If echoes has only one signal per direction, the same variable is returned.
  if type(echoes) == dict:
    return echoes
  
  # Calculate the average over every direction. The average is considering the
  # length of the list echo and not using number_of_measurements for the case 
  # where data is corrupted and len(echoes) < number_of_measurements.
  averages = dict()

  for direction in dpp.CARDINAL_POINTS:
    values = []
    for i in range(len(echoes)):
      values.append(echoes[i][direction])
      averages[direction] = np.average(values, 0)
      
  return averages
  
def remove_crosstalk(echoes, noise):
  """ Given an echoes signal and a noise signal, both signals are substructed to
      obtain a signal without crosstalk.
  """
  calibrated_echo = dict()
  for direction in dpp.CARDINAL_POINTS:
    calibrated_echo[direction] = echoes[direction] - noise[direction]
  
  return calibrated_echo

def zero_crossings(echoes):
  """ Calculates the zero crossings for one echo and returns a dict containing
      the zero crossings for each direction.
  """
  zero_crossings = dict()
  t_zeros = dict()
  
  for direction in dpp.CARDINAL_POINTS:
    # Calculate the sample right *before* the sign change.
    zero_crossings[direction] = np.where(np.diff(np.sign(echoes[direction])))[0]

    # Linear interpolation: z - z0 = m*(t - t0) to calculate the exact time at
    # which the zero crossing occurs    
    m = (echoes[direction][zero_crossings[direction] + 1] - \
         echoes[direction][zero_crossings[direction]]) / \
        (zero_crossings[direction] + 1 - zero_crossings[direction])
    t_zeros[direction] = zero_crossings[direction] - \
                         echoes[direction][zero_crossings[direction]]/m
 
  return t_zeros
  
def differentiate(echoes):
  """ Calculate numpy.diff() for every direction in 
      data_preprocessing.CARDINAL_POINTS.
  """
  echoes_diff = dict()
  for direction in dpp.CARDINAL_POINTS:
    echoes_diff[direction] = np.diff(echoes[direction])
    
  return echoes_diff
  
def argmax(echoes):
  """ Calculate the index of the maximum amplitude for an echo structure,
      using the CARDINAL_POINTS in data_preprocessing.CARDINAL_POINTS.
  """  
  argmax = dict()
  for direction in dpp.CARDINAL_POINTS:
    argmax[direction] = np.argmax(echoes[direction])

  return argmax
  
def samples_of_flight_threshold(echoes, threshold):
  """ Calculate the sample in which the echoes cross a given threshold value.
  """  
  echoes_minus_threshold = dict()
  # To reuse the zero_crossings function, we substract the threshold from the
  # the echo and use zero_crossings to find the first crossing of the echo and
  # the threshold.
  for direction in dpp.CARDINAL_POINTS:
    echoes_minus_threshold[direction] = echoes[direction] - threshold[direction]
  
  # Use zero_crossings to calculate the threshold crossings, and return only the
  # first value of the array. If the echo does nos intersect the threshold, the
  # program is terminated.
  threshold_crossings = zero_crossings(echoes_minus_threshold)
  for direction in dpp.CARDINAL_POINTS:
    try:
      threshold_crossings[direction] = threshold_crossings[direction][0]
    except IndexError:
      print ("signal_operations.py: Threshold does not intersect the echo. " + 
          "Please select a lower threshold (in [0,1]).")
      exit()
    
  return threshold_crossings
  
def samples_to_time(samples):
  """ Convert number of sample to time, using dpp.SAMLING_RATE.
  """
  time_of_flight = dict()
  for direction in dpp.CARDINAL_POINTS:
    time_of_flight[direction] = samples[direction]/dpp.SAMPLING_RATE
    
  return time_of_flight
      
def normalize(echoes):
  """ Normalize the echoes dict().
  """  
  for direction in dpp.CARDINAL_POINTS:
    echoes[direction] = echoes[direction]/np.max(echoes[direction])
  return echoes
  
def calculate_wind_speed(echoes, threshold, delta_in_samples, distance):
  """ Calculate the wind speed based upon time of flight calculation using
      threshold. This function considers the calibration for this purpose.
  """  
  # Prepare the measurements by averaging, differentiating to remove the offset
  # and normalizing to be able to easily use a threshold.
  echoes = normalize(differentiate(average(echoes)))
  
  # First, we calculate the number of samples until the echo meets the threshold
  samples_of_flight_threshold_xx = \
      samples_of_flight_threshold(echoes, threshold)

  # Now we calculate the zero crossings to calculate the time in which the zero
  # crossing right before the threshold intersection occurs.
  zeros = zero_crossings(echoes)
  
  arg = dict()
  speed = []
  ToF = dict()

  for direction in dpp.CARDINAL_POINTS:
    # Calculate the index in zeros corresponding to the zero crossings right
    # before the threshold crossing.
    # Reported bug: There are some cases where the frame passes sanity check,
    # but the echo in the signal is corrupted. In this case, trying to find the
    # index in zeros throws an IndexError.
    try:
      arg[direction] = np.argwhere(samples_of_flight_threshold_xx[direction] >
                                    zeros[direction])[-1][-1]
    except IndexError:
      print "signal_operations.py: Corrupt signal, please check connections."
      for direction in dpp.CARDINAL_POINTS:
        speed.append(0)
        return speed
    # Calculate the time of flight in seconds, considering the shift introduced
    # by the derivation of the echo.
    ToF[direction] = (zeros[direction][arg[direction]] -
        delta_in_samples[direction] + dpp.EXCITATION_LENGTH + 
        dpp.EXCITATION_PERIOD/4)/dpp.SAMPLING_RATE
  
  # Create the list of speeds for each direction.
  for direction in dpp.AXES:
    speed.append((distance[direction[0]]/2.0)*(1.0/ToF[direction[0]] - 
        1.0/ToF[direction[1]]))

  return speed
  
def delta_samples(echoes, threshold, ToF):
  """ Calculate the time delta between the theoretical time of flight and the
      and the closest zero crossing before the threshold crossing.
  """  
  echoes = normalize(differentiate(average(echoes)))

  arg = dict()
  delta_samples = dict()
  samples_of_flight = samples_of_flight_threshold(echoes, threshold)
  zeros = zero_crossings(echoes)
  
  for direction in dpp.CARDINAL_POINTS:
    arg[direction] = np.argwhere(samples_of_flight[direction] > 
                                      zeros[direction])[-1][-1]
    delta_samples[direction] = (zeros[direction][arg[direction]] - 
       (dpp.SAMPLING_RATE*ToF[direction] - 
       dpp.EXCITATION_LENGTH)/dpp.SAMPLING_CORRECTION)
      
  return delta_samples
  
def calibration(echoes, distance, temperature, pressure, relative_humidity):
  # Calculate the time of flight
  speed = speed_of_sound(temperature, pressure, relative_humidity)
  ToF = dict()
  for direction in dpp.CARDINAL_POINTS:
    ToF[direction] = distance[direction]/speed

  # Calculate the time delta in samples
  delta_in_samples = delta_samples(echoes, THRESHOLD, ToF)
  
  return delta_in_samples
  
def speed_of_sound(temperature, pressure, relative_humidity):
  temperature = temperature + 273.15 # Convert from Celsius to Kelvin  
  
  # Thermodynamic operations
  Rd = 287.04 # [J kg^-1 K^-1], Gas constant for dry air   
  Rv = 461.50 # [J kg^-1 K^-1], Gas constant for water vapor
  epsilon = Rd/Rv
  gamma = 1.4

  # According to Hyland and Wexler (1983), 173 - 473.
  e_sat = np.exp(-0.58002206 * np.power(10.0,  4.0) / temperature
               +  0.13914993 * np.power(10.0,  1.0) * np.power(temperature, 0.0)
               -  0.48640239 * np.power(10.0, -1.0) * temperature 
               +  0.41764768 * np.power(10.0, -4.0) * np.power(temperature, 2.0)
               -  0.14452093 * np.power(10.0, -7.0) * np.power(temperature, 3.0)
               +  0.65459673 * 10 * np.log(temperature)) / 100

  r_sat = epsilon*e_sat/(pressure - e_sat)
  r = r_sat*relative_humidity
  
  virtual_temperature = temperature*(1 + r/epsilon)/(1 + r)
  speed = np.sqrt(gamma*Rd*virtual_temperature)
  
  return speed
