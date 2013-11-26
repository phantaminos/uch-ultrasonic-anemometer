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