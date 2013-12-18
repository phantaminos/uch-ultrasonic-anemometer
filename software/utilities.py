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

from scipy.io import netcdf
import numpy as np
import matplotlib.pyplot as plt
import data_preprocessing as dpp

  
def load_echoes_from_file(filename,
                          measurements):
  """ Load an echoes data structure from file filename. The echos included in
      the result are those indicated by the list measurement.
  """
  echoes = []

  # Load data
  data = np.load(filename)

  for number_of_frame in measurements:
    # Concatenate the new list from split_frame into the echoes list
    aux_echo = dpp.split_frame(data[number_of_frame])
    if aux_echo != None:
      echoes = echoes + aux_echo

  return echoes

def plot_echoes(echoes, threshold, figure, color):
  """ Plot echoes dict().
  """    
  subplot = dict()
  plt.figure(figure)
  i = 1
  # The subplot number is created considering 2 rows and a variable number of
  # columns depending in the list dpp.DIRECTIONS.
  for direction in dpp.DIRECTIONS:
    subplot[direction] = np.int(2*100 + len(dpp.DIRECTIONS)/2*10 + i)
    plt.subplot(subplot[direction])
    plt.plot(echoes[direction], color)
    plt.plot(np.ones(len(echoes[direction]))*threshold[direction], 'g')
    plt.title(direction)
    plt.grid(True)
    i += 1
  plt.tight_layout()
