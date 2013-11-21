//
// Copyright (C) 2013  UNIVERSIDAD DE CHILE.
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.
//
// Authors: Luis Alberto Herrera <herrera.luis.alberto@gmail.com>

#include "adc_reader.h"
#include "gtest/gtest.h"

TEST(ADCReaderTest, DataConversion) {
  ADCReader reader;
  int16_t zero = 0;

  int16_t two_thousand;
  ((char*)(&two_thousand))[0] = 0x07;
  ((char*)(&two_thousand))[1] = 0xD0;

  int16_t minus_two_thousand;
  ((char*)(&minus_two_thousand))[0] = 0x08;
  ((char*)(&minus_two_thousand))[1] = 0x30;

  EXPECT_EQ(0, reader.ConvertFromADCFormat(zero));
  EXPECT_EQ(2000, reader.ConvertFromADCFormat(two_thousand));
  EXPECT_EQ(-2000, reader.ConvertFromADCFormat(minus_two_thousand));
}
