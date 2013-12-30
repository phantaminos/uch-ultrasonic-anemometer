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
    m = (echoes[direction][zero_crossings[direction]+1] - \
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
    
def substract_mean(echoes):
  """ Subtract the mean of and echo structure, using the direction in 
      data_preprocessing.CARDINAL_POINTS.
      It considers only the first dpp.EXCITATION_LENGTH/3 values of the echo.
  """
  echoes_minus_mean = dict()
  
  for direction in dpp.CARDINAL_POINTS:
    assert len(echoes[direction]) > dpp.EXCITATION_LENGTH/3
    echoes_minus_mean[direction] = (echoes[direction] - 
                                    np.mean(echoes[direction]
                                                  [0:dpp.EXCITATION_LENGTH/3]))

  return echoes_minus_mean
  
def argmax(echoes):
  """ Calculate the argument of the maximum amplitude for an echo structure,
      using the CARDINAL_POINTS in data_preprocessing.CARDINAL_POINTS.
  """  
  argmax = dict()
  for direction in dpp.CARDINAL_POINTS:
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
                         
  for direction in dpp.CARDINAL_POINTS:
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
  for direction in dpp.CARDINAL_POINTS:
    echoes_minus_threshold[direction] = echoes[direction] - threshold[direction]
  
  # Use zero_crossings to calculate the threshold crossings, and return only the
  # first value of the array.   
  threshold_crossings = zero_crossings(echoes_minus_threshold)
  for direction in dpp.CARDINAL_POINTS:
    threshold_crossings[direction] = threshold_crossings[direction][0]
    
  return threshold_crossings
  
def samples_to_time(samples):
  """ Convert number of sample to time, using dpp.SAMLING_RATE.
  """
  time_of_flight = dict()
  for direction in dpp.CARDINAL_POINTS:
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
  for direction in dpp.CARDINAL_POINTS:
    echoes[direction] = echoes[direction]/np.max(echoes[direction])
  return echoes
  
def calculate_wind_speed(echoes_xx, threshold, delta_in_samples, distance):
  """ Calculate the wind speed based upon timeo flight calculation using
      threshold. This function considers the calibration for this purpose.
  """  
  # Prepare the measurements by averaging, differentiating to remove the offset
  # and normalizing to be able to easily use a threshold.
  echoes_xx = normalize(differentiate(average(echoes_xx)))
  
  # First, we calculate the number of samples until the echo meets the threshold
  samples_of_flight_threshold_xx = \
      samples_of_flight_threshold(echoes_xx, threshold)

  # Now we calculate the zero crossings to calculate the phase difference 
  # between the received echo and a reference echo.
  zeros = zero_crossings(echoes_xx)
  
  arg = dict()
  speed = []
  ToF = dict()

  for direction in dpp.CARDINAL_POINTS:
    # Calculate the index in zeros_xx corresponding to the zero crossings right
    # before the threshold crossing.
    arg[direction] = np.argwhere(samples_of_flight_threshold_xx[direction] >
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
  
def delta_samples(echoes, threshold, ToF):
  """ Calculate the time delta between the theoretical time of flight and the
      and the threshold crossing.
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
  # Thermodynamic operations
  Rd = 287.04 # [J kg^-1 K^-1], Gas constant for dry air   
  Rv = 461.50 # [J kg^-1 K^-1], Gas constant for water vapor
  epsilon = Rd/Rv
  gamma = 1.4

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

  # Calculate the time delta in samples
  delta_in_samples = delta_samples(echoes, THRESHOLD, ToF)
  
  # Save calibration information into a file
  np.savez('delta_in_samples', delta_in_samples, dpp.CARDINAL_POINTS)
