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
    # Initialize echoes and noise dict
    self.echoes = dict()

    # Create a triangular signal for which zero crossings are known:
    # np.arange(0.5, 49.5). 
    x = np.ones(50)
    aux = np.zeros(len(x))
    for i in range(0,len(x)):
      if i%2: aux[i] = -1
      else: aux[i] = 1
    
    for direction in dpp.DIRECTIONS:
      self.echoes[direction] = aux
    
  def test_average(self):
    for direction in dpp.DIRECTIONS:
      self.assertTrue((self.echoes[direction] == 
                       so.average(self.echoes)[direction]).all())
      self.assertTrue((self.echoes[direction] == 
                       so.average((self.echoes, self.echoes))[direction]).all())
  
  def test_remove_crosstalk(self):
    crosstalk = dict()
    for direction in dpp.DIRECTIONS:
      crosstalk[direction] = self.echoes[direction] - 2

    for direction in dpp.DIRECTIONS:
      self.assertTrue((2*np.ones(len(self.echoes[direction])) == 
                       so.remove_crosstalk(self.echoes, 
                                           crosstalk)[direction]).all())
  
  def test_zero_crossings(self):
    # Calculate zero crossings
    zeroes = so.zero_crossings(self.echoes)
    
    for direction in dpp.DIRECTIONS:
      self.assertTrue((zeroes[direction] == np.arange(0.5,49.5)).all())    
  
if __name__ == '__main__':
  unittest.main()