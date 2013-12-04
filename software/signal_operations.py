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

def time_of_flight_phase_detection(echoes):
  """ Calculate the time of flight for an echo structure through phase detection
      using the zero crossings of the signal.
      This function returns the time of flight of the preprocessed echo, the 
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
  # beacause this interval uses information of the frequency of the signal and
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