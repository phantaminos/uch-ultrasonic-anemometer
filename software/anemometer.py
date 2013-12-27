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
# along with this program.  If not, see <http:#www.gnu.org/licenses/>.
#
# Authors: Luis Alberto Herrera <herrera.luis.alberto@gmail.com>


class Anemometer:
  """ Interface to the anemometer. This is the public interface for
      users of this library.
  """

  def __init__(self, frames_per_measure=50):
    self.frames_per_measure = frames_per_measure
    pass

  def calibrate(self):
    """ This function must be called once for every particular piece of
        equipment. This must be called from an interactive terminal. The
        user prompted to enter values of temperature, humidity pressure and
        distrance betweeen trasnducers.
    """
    pass

  def measure_wind_speed(self):
    """ This function should be called every time the user wants to measure
        the wind speed. The return value is a vector wit the wind in every
        component.
    """
    pass
