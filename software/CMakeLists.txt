cmake_minimum_required (VERSION 2.6)
project (UchUltrasonicAnemometer)


add_custom_target(lint)
add_dependencies(lint pylint cpplint)
file(GLOB CC_SOURCES RELATIVE ${CMAKE_CURRENT_BINARY_DIR} *.cc *.h)
add_custom_target(cpplint
  COMMAND python ${CMAKE_CURRENT_SOURCE_DIR}/cpplint.py --root=software ${CC_SOURCES}
)
# Copy python files to build directory so they can find the compiled swig
# wrappers
function(add_python_source)
  add_custom_target(pylint
    COMMAND pylint --rcfile=${CMAKE_CURRENT_SOURCE_DIR}/pylintrc ${ARGN}
  )

  foreach(file ${ARGN})
    add_custom_command(
      OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/${file}
      COMMAND ${CMAKE_COMMAND} -E copy ${CMAKE_CURRENT_SOURCE_DIR}/${file} ${CMAKE_CURRENT_BINARY_DIR}/${file}
      MAIN_DEPENDENCY ${CMAKE_CURRENT_SOURCE_DIR}/${file})

    STRING(REGEX REPLACE "/" "_" target_name ${CMAKE_CURRENT_BINARY_DIR}/${file})
    add_custom_target(${target_name} ALL DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/${file})
    add_dependencies(pylint ${target_name})

  endforeach()
endfunction()

set(CMAKE_CXX_FLAGS "-std=c++0x")
include_directories(${CMAKE_CURRENT_SOURCE_DIR})

find_package(SWIG REQUIRED)
include(${SWIG_USE_FILE})
find_package(PythonLibs)
include_directories(${PYTHON_INCLUDE_PATH})

#python targets
add_python_source(plot_from_adc.py)

# Swig targets
SET_SOURCE_FILES_PROPERTIES(adc_reader.i PROPERTIES CPLUSPLUS ON)
SWIG_ADD_MODULE(adc_reader python adc_reader.i adc_reader.cc)
SWIG_LINK_LIBRARIES(adc_reader ${PYTHON_LIBRARIES} mpsse)

# Test targets
add_subdirectory(gtest)
enable_testing()
include_directories(${gtest_SOURCE_DIR}/include ${gtest_SOURCE_DIR})
add_executable(adc_reader_test adc_reader_test.cc adc_reader.cc)
target_link_libraries(adc_reader_test gtest gtest_main mpsse)
add_test(adc_reader_test adc_reader_test)
