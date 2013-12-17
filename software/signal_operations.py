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
import matplotlib.pyplot as plt

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

  for direction in dpp.DIRECTIONS:
    values = []
    for i in range(len(echoes)):
      values.append(echoes[i][direction])
      averages[direction] = np.average(values, 0)
      
  return averages
  
def remove_crosstalk(echoes, noise):
  """ Given an echoes signal and a noise signal, both signals are substructed to
      obtain a calibrated (without crosstalk) signal.
  """
  calibrated_echo = dict()
  for direction in dpp.DIRECTIONS:
    calibrated_echo[direction] = echoes[direction] - noise[direction]
  
  return calibrated_echo

def zero_crossings(echoes):
  """ Calculates the zero crossings for one echo and returns a dict containing
      the zero crossings for each direction.
  """
  zero_crossings = dict()
  t_zeros = dict()
  
  for direction in dpp.DIRECTIONS:
    # Calculate the sample right *before* the sign change.
    zero_crossings[direction] = np.where(np.diff(np.sign(echoes[direction])))[0]

    # Linear interpolation: z - z0 = m*(t - t0) to calculate the exact time at
    # which the zero crossing occurs    
    m = (echoes[direction][zero_crossings[direction]+1] - \
         echoes[direction][zero_crossings[direction]]) / \
        (zero_crossings[direction] + 1 - zero_crossings[direction])
    t_zeros[direction] = zero_crossings[direction] - \
                         echoes[direction][zero_crossings[direction]]/m
 
  return t_zeros
  
def differentiate(echoes):
  """ Calculate numpy.diff() for every direction in 
      data_preprocessing.DIRECTIONS.
  """
  echoes_diff = dict()
  for direction in dpp.DIRECTIONS:
    echoes_diff[direction] = np.diff(echoes[direction])
    
  return echoes_diff
    
def substract_mean(echoes):
  """ Subtract the mean of and echo structure, using the direction in 
      data_preprocessing.DIRECTIONS.
  """
  echoes_minus_mean = dict()
  
  for direction in dpp.DIRECTIONS:
    echoes_minus_mean[direction] = (echoes[direction] - 
                                    np.mean(echoes[direction]
                                                  [0:dpp.EXCITATION_LENGTH/3]))

  return echoes_minus_mean
  
def argmax(echoes):
  """ Calculate the argument of the maximum amplitude for an echo structure,
      using the directions in data_preprocessing.DIRECTIONS.
  """  
  argmax = dict()
  for direction in dpp.DIRECTIONS:
    argmax[direction] = np.argmax(echoes[direction])

  return argmax

def samples_of_flight_phase_detection(echoes):
  """ Calculate the samples of flight for an echo structure through phase 
      detection using the zero crossings of the signal.
      This function returns the samples of flight of the preprocessed echo, the 
      argument of the maximum value of the echo, and the argument of the time of
      flight.
  """  
  time_of_flight = dict()
  arg = dict()
  arg_init = dict()

  # Calculate the argument of the maximum value of the echo  
  # TODO: Might be optimized using a value closer to the beginning of the echo
  arg_max = argmax(echoes) 
  # Calculate the zero crossings of the echo
  t_zeros = zero_crossings(echoes)
  
  # Interval for the zero crossings difference. The EXCITATION_PERIOD is used
  # because this interval uses information of the frequency of the signal and
  # the samping rate of the ADC.
  interval = np.arange(np.floor(dpp.EXCITATION_PERIOD/2) - 2, 
                       np.floor(dpp.EXCITATION_PERIOD/2) + 3, 
                       4)
                         
  for direction in dpp.DIRECTIONS:
    # Calculate the index in t_zeros corresponding to the maximum amplitude 
    # of the received echo
    arg[direction] = np.argwhere(arg_max[direction] > t_zeros[direction])[-1][-1]
    arg_init[direction] = arg[direction]
  
    # While the difference of t_zeros lies inside the interval, we substract 1
    # from the argument. The third condition considers the case where the
    # difference bewteen to zero crossings is zero.
    while ((np.diff(t_zeros[direction])[arg[direction]] <= interval[1]) and 
           (np.diff(t_zeros[direction])[arg[direction]] >= interval[0]) or
           (np.diff(t_zeros[direction])[arg[direction]] == 0)):
      arg[direction] -=1
  
    time_of_flight[direction] = t_zeros[direction][arg[direction]]
  
  return time_of_flight, arg, arg_init
  
def samples_of_flight_threshold(echoes, threshold):
  """ Calculated the sample in which the echoes cross a given threshold value.
  """  
  echoes_minus_threshold = dict()
  # To reuse the zero_crossings function, we substract the threshold from the
  # the echo and use zero_crossings to find the first crossing of the echo and
  # the threshold.
  for direction in dpp.DIRECTIONS:
    echoes_minus_threshold[direction] = echoes[direction] - threshold[direction]
  
  # Use zero_crossings to calculate the threshold crossings, and return only the
  # first value of the array.   
  threshold_crossings = zero_crossings(echoes_minus_threshold)
  for direction in dpp.DIRECTIONS:
    threshold_crossings[direction] = threshold_crossings[direction][0]
    
  return threshold_crossings
  
def samples_to_time(samples):
  """ Convert number of sample to time, using dpp.SAMLING_RATE.
  """
  time_of_flight = dict()
  for direction in dpp.DIRECTIONS:
    time_of_flight[direction] = samples[direction]/dpp.SAMPLING_RATE
    
  return time_of_flight
  
def wind_speed_from_time_of_flight(time_of_flight, distance1, distance2):
  """ Calculate the wind_speed using the time of flight.
  """
  wind_speed = dict()  
  wind_speed['NS'] = distance1/2*(1.0/time_of_flight['NORTH'] - 1.0/time_of_flight['SOUTH'])
  wind_speed['EW'] = distance2/2*(1.0/time_of_flight['WEST'] - 1.0/time_of_flight['EAST'])
  
  return wind_speed
  
def speed_of_sound_from_time_of_flight(time_of_flight, distance1, distance2):
  """ Calculate the wind_speed using the time of flight.
  """
  speed_of_sound = dict()  
  speed_of_sound['NS'] = distance1/2*(1.0/time_of_flight['NORTH'] + 1.0/time_of_flight['SOUTH'])
  speed_of_sound['EW'] = distance2/2*(1.0/time_of_flight['WEST'] + 1.0/time_of_flight['EAST'])
  
  return speed_of_sound
  
def normalize(echoes):
  """ Normalize the echoes dict().
  """  
  for direction in dpp.DIRECTIONS:
    echoes[direction] = echoes[direction]/np.max(echoes[direction])
  return echoes
  
def wind_speed(echoes_00, echoes_xx, threshold, distance):
  """ Calculate the wind speed based upon the comparisson of the phase of an
      echo with respect to a reference echo. The phase comparisson is performed
      in the vicinity of a threshold.
      The echoes are normalized for a consequent threshld usage.
  """  
  # Prepare the measurements by averaging, differentiating to remove the offset
  # and normalizing to be able to easily use a threshold.
  echoes_00 = normalize(differentiate(average(echoes_00)))
  echoes_xx = normalize(differentiate(average(echoes_xx)))
  
  # First, we calculate the number of samples until the echo meets the threshold
  samples_of_flight_threshold_00 = \
      samples_of_flight_threshold(echoes_00, threshold)
  samples_of_flight_threshold_xx = \
      samples_of_flight_threshold(echoes_xx, threshold)

  # Now we calculate the zero crossings to calculate the phase difference 
  # between the received echo and a reference echo.
  zeros_00 = zero_crossings(echoes_00)
  zeros_xx = zero_crossings(echoes_xx)
  
  arg_00 = dict()
  arg_xx = dict()
  speed = dict()
  delta_time = dict()
  t1 = dict()
  direction = dict()

  for direction in dpp.DIRECTIONS:
    t1[direction] = distance[direction]/dpp.V_S
    # Calculate the index in zeros_xx corresponding to the zero crossings right
    # before the threshold crossing.
    # The next ten differences between the reference echo and the received echo
    # are avreaged to get the pahse difference (delta time) between both echoes.
    arg_00[direction] = np.argwhere(samples_of_flight_threshold_00[direction] > 
                                    zeros_00[direction])[-1][-1]
    arg_xx[direction] = np.argwhere(samples_of_flight_threshold_xx[direction] >
                                    zeros_xx[direction])[-1][-1]
    delta_time[direction] = \
        np.mean(zeros_xx[direction][arg_xx[direction]:arg_xx[direction]+10] -
        zeros_00[direction][arg_00[direction]:arg_00[direction]+10])/\
        dpp.SAMPLING_RATE  
    if direction == 'NORTH' or direction == 'SOUTH':
      speed[direction] = distance[direction]*delta_time[direction]/\
          (t1[direction]*(t1[direction] + delta_time[direction]))
    else: # EAST or WEST
      speed[direction] = distance[direction]*delta_time[direction]/\
          (t1[direction]*(t1[direction] + delta_time[direction]))

  return speed
