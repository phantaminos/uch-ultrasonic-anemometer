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

import signal_operations as so
import data_preprocessing as dpp
import numpy as np
import unittest

class TestSignalOperations(unittest.TestCase):

  def setUp(self):
    # Initialize dicts() for easy testing
    self.signal = dict() # Triangular signal
    self.echoes = dict() # Simulated echo
    self.threshold = dict() # Threshold

    # Create a triangular signal for which zero crossings are known.
    # Other attributes such as derivative, argmax are also known.
    x = np.ones(50)
    aux = np.zeros(len(x))
    for i in range(0,len(x)):
      if i%2:
        aux[i] = -1
      else:
        aux[i] = 1

    # Create a simulated echoes dict()
    V_0 = 10
    m = 3
    h = 1
    theta = 0
    w = 10
    zeros = 100
    t = np.zeros(zeros + 100*w)
    t[zeros:] = np.linspace(0, 20, 100*w)
    echo = V_0*t**m*np.exp(-t/h)*np.cos(w*t + theta)
    
    for direction in dpp.CARDINAL_POINTS:
      # Assign signal, echo and threshold values.
      self.signal[direction] = aux
      self.echoes[direction] = echo
      self.threshold[direction] = 0.3
      
  def test_average(self):
    for direction in dpp.CARDINAL_POINTS:
      # assertTrue is used instead of assertEqual to compare all the elements
      # in two different arrays.
      self.assertTrue((self.signal[direction] == 
                       so.average(self.signal)[direction]).all())
      self.assertTrue((self.signal[direction] == 
                       so.average((self.signal, self.signal))[direction]).all())
  
  def test_remove_crosstalk(self):
    crosstalk = dict()
    offset = 2
    for direction in dpp.CARDINAL_POINTS:
      crosstalk[direction] = self.signal[direction] - offset

    for direction in dpp.CARDINAL_POINTS:
      self.assertTrue((2*np.ones(len(self.signal[direction])) == 
                       so.remove_crosstalk(self.signal, 
                                           crosstalk)[direction]).all())
  
  def test_zero_crossings(self):
    # Calculate zero crossings
    zeroes = so.zero_crossings(self.signal)
    
    for direction in dpp.CARDINAL_POINTS:
      self.assertTrue((zeroes[direction] == np.arange(0.5,49.5)).all())    
  
  def test_differentiate(self):
    derivative = so.differentiate(self.signal)
    for direction in dpp.CARDINAL_POINTS:
      self.assertTrue((derivative[direction] == 
          -2*self.signal[direction][0:-1]).all)
          
  def test_argmax(self):
    arbitrary_point = 3    
    for direction in dpp.CARDINAL_POINTS:
      # Change the value of an arbitrary point to make sure this point is
      # considered the arg_max
      self.signal[direction][arbitrary_point] = 10

    arg_max = so.argmax(self.signal)
    
    for direction in dpp.CARDINAL_POINTS:
   
      self.assertEqual(arg_max[direction], arbitrary_point)

  def test_samples_of_flight_threshold(self):
    threshold_crossings = so.samples_of_flight_threshold(self.echoes,
                                                         self.threshold)
    threshold_echo_intersection = 125.45564873732962
    for direction in dpp.CARDINAL_POINTS:
      self.assertEqual(threshold_crossings[direction], 
                       threshold_echo_intersection)

  def test_samples_to_time(self):
    samples = dict()
    time = dict()
    for direction in dpp.CARDINAL_POINTS:
      samples[direction] = 200
      time[direction] = samples[direction]/dpp.SAMPLING_RATE      

    time_from_function = so.samples_to_time(samples)
    for direction in dpp.CARDINAL_POINTS:
      self.assertEqual(time_from_function[direction], time[direction])

  def test_normalize(self):
    aux_signal = dict()
    for direction in dpp.CARDINAL_POINTS:
      aux_signal[direction] = 2*self.signal[direction]
      
    normalized_aux_signal = so.normalize(aux_signal)
    
    for direction in dpp.CARDINAL_POINTS:
      self.assertTrue((normalized_aux_signal[direction] ==
          self.signal[direction]).all())

  def test_speed_of_sound(self):
    temperature = 24.5 # temperature in Celsius
    pressure = 950     # pressure in hPa
    relative_humidity = 0.6 # Fraction in [0,1]
    
    speed_of_sound = 347.14416646466151

    self.assertEqual(so.speed_of_sound(temperature, 
                                       pressure, 
                                       relative_humidity),
                     speed_of_sound)
  
if __name__ == '__main__':
  unittest.main()