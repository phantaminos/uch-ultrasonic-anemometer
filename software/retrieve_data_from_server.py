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

import urllib
import argparse
import subprocess

# Check for ./server_samples folder. If not available, create folder.
p1 = subprocess.Popen(["ls"], stdout = subprocess.PIPE)
p2 = subprocess.Popen(["grep", "-w", "server_samples"], 
                      stdin = p1.stdout, 
                      stdout = subprocess.PIPE)
p1.stdout.close()
output = p2.communicate()[0]
if output == "": # Folder no available
  subprocess.call(["mkdir", "server_samples"])

# Create parser
parser = argparse.ArgumentParser(description = 
                                 'Retrieve data from Raspberry Pi using the ' +
                                 'installed web server. The data is saved in ' +
                                 'the folder ./server_samples.')
# Add optional arguments
parser.add_argument('-m',
                    '--measurements', 
                    type = int,
                    default = 10,
                    help = 'No. of measurements in every direction.')
parser.add_argument('-v',
                   '--velocity',
                   type = int,
                   default = 0,
                   help = 'Wind velocity for file name.')
parser.add_argument('-c',
                    '--calibration',
                    type = bool,
                    default = False,
                    help = 'Calibration boolean. Measure noise from ' +
                    'the electronics.')
parser.add_argument('-i',
                   '--ip',
                   type = str,
                   default = "192.168.0.139", # Static IP
                   help = 'IP address of the Raspberry Pi.')

# Parse arguments.
args = parser.parse_args()

# Retrieve data
for measurement in range(args.measurements):
  if not args.calibration:
    file_name = './server_samples/v_%02d_%04d.nc'%(args.velocity, measurement)
  else:
    file_name = './server_samples/v_--_%04d.nc'%(measurement)
  print "Retrieving", file_name  
  urllib.urlretrieve('http://' + args.ip + ':8000/', file_name)