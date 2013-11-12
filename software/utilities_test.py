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
import utilities

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import netcdf
import scipy as sp

path = '/Users/karel/Dropbox/Anemometro/AnemometroSonico/samples/20131108'
number_of_measurements = 100
measurements_on_file = 1

echoes_noecho = []
echoes_v_zero = []

for measurement in range(number_of_measurements):
  # No echo: Load data
  f = netcdf.netcdf_file(path + '/noecho/_%04d.nc'%(measurement), 'r')
  measurement_noecho = f.variables['frame']
  f.close()
  
  # Concatenate the new list from split_frame into the echoes list
  echoes_noecho = echoes_noecho + dpp.split_frame(measurement_noecho.data, 
                                                  measurements_on_file)
  
  plt.figure(1)
  plt.subplot(211) 
  plt.plot(echoes_noecho[measurement]['NORTH'],'r')
  plt.grid(True)
  plt.subplot(212)
  plt.plot(echoes_noecho[measurement]['SOUTH'], 'r')
  plt.grid(True)
  
  # v = 0: Load data
  f = netcdf.netcdf_file(path + '/v_zero/_%04d.nc'%(measurement), 'r')
  measurement_v_zero = f.variables['frame']
  f.close()
  
  # Concatenate the new list from split_frame into the echoes list
  echoes_v_zero = echoes_v_zero + dpp.split_frame(measurement_v_zero.data, 
                                                  measurements_on_file)
  
  plt.figure(1)
  plt.subplot(211) 
  plt.plot(echoes_noecho[measurement]['NORTH'],'r')
  plt.grid(True)
  plt.subplot(212)
  plt.plot(echoes_noecho[measurement]['SOUTH'], 'r')
  plt.grid(True)
  
  plt.figure(2)
  plt.subplot(211) 
  plt.plot(echoes_v_zero[measurement]['NORTH'],'r')
  plt.grid(True)
  plt.subplot(212)
  plt.plot(echoes_v_zero[measurement]['SOUTH'], 'r')
  plt.grid(True)

# Average
average_noecho = utilities.average(echoes_noecho)

plt.figure(1)
plt.subplot(211)
plt.plot(average_noecho['NORTH'],'k')

plt.subplot(212)
plt.plot(average_noecho['SOUTH'],'k')

average_v_zero = utilities.average(echoes_v_zero)

plt.figure(2)
plt.subplot(211)
plt.plot(average_v_zero['NORTH'],'k')

plt.subplot(212)
plt.plot(average_v_zero['SOUTH'],'k')


# Zero crossings
t_zeros = utilities.zero_crossings(utilities.calibrate(average_v_zero, average_noecho))

plt.figure(3)
plt.subplot(211)
plt.plot(average_v_zero['NORTH'] - average_noecho['NORTH'])
plt.plot(t_zeros['NORTH'], [0]*len(t_zeros['NORTH']),'*k')
plt.grid(True)
plt.axvline(142, linestyle = '--', color = 'r')
plt.legend(('Calibrated signal','Zero crossings','ToF'))
plt.ylabel('Amplitude')
plt.xlabel('Samples')

plt.subplot(212)
plt.plot(t_zeros['NORTH'][:-1], np.diff(t_zeros['NORTH']))
plt.grid(True)
plt.axvline(142, linestyle = '--', color = 'r')
plt.ylabel('Zero crossings difference')
plt.xlabel('Samples')