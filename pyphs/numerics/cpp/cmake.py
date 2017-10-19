#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 25 12:07:58 2017

@author: Falaize
"""
import os


def cmake_write(project_name, path):
    """
    Write the CMakeLists.txt for cmake build and compilation.

    Parameters
    ----------

    project_name : str
        Name for the cmake project and for the binary.

    path : str
        Path to the directory where the build shall be made.
    """
    filepath = os.path.join(path, 'CMakeLists.txt')
    f = open(filepath, 'w+')
    f.write(_template(project_name))
    f.close()
    return filepath


def _template(project_name):
    """
    Template for CMakeLists.txt.
    """
    return """
# Specify the minimum version for CMake
cmake_minimum_required(VERSION 3.1.0 FATAL_ERROR)

# Project's name
project(%s CXX)

# Set target to RELEASE
set(CMAKE_BUILD_TYPE Release)

# Set the output folder where program will be created
set(CMAKE_BINARY_DIR ${CMAKE_SOURCE_DIR}/bin)
set(EXECUTABLE_OUTPUT_PATH ${CMAKE_BINARY_DIR})
set(LIBRARY_OUTPUT_PATH ${CMAKE_BINARY_DIR})

# Set the needed source files
set(SOURCE_FILES
    src/core.cpp
    src/core.h
    src/parameters.cpp
    src/parameters.h
    src/simu.cpp)

find_package (Eigen3 3.3 REQUIRED NO_MODULE)

# Set executable with same name as the project
add_executable(%s ${SOURCE_FILES})
target_link_libraries (%s Eigen3::Eigen)

# Activate C++11
target_compile_features(%s PUBLIC cxx_std_11)
""" % (project_name, project_name, project_name, project_name)
