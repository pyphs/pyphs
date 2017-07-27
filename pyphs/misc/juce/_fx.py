#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 22:32:59 2017

@author: Falaize
"""

import os
from pyphs.numerics.cpp.tools import indent

def snippetAudioProcessorHDeclare(objlabel):

    code = """
//=========================================================================
// Define PHS object (see AudioProcessor contructor for initialization).
{0} {1};

//=========================================================================
// Allocate some memories.
unsigned int phsInputIndex = 0;
unsigned int phsOutputIndex = 0;
double phsInput = 0.f;""".format(objlabel.upper(), 
                                 objlabel.lower())
    return indent(code)
    

def snippetAudioProcessorHInclude(src_folder):
    include = os.path.join('..', src_folder, 'core.h')
    return '#include "{}"'.format(include)


def snippetAudioProcessorCppInitList(objlabel):
    return """:
#ifndef JucePlugin_PreferredChannelConfigurations
     AudioProcessor (BusesProperties()
                     #if ! JucePlugin_IsMidiEffect
                      #if ! JucePlugin_IsSynth
                       .withInput  ("Input",  AudioChannelSet::stereo(), true)
                      #endif
                       .withOutput ("Output", AudioChannelSet::stereo(), true)
                     #endif
                       ),
#endif
{}()
""".format(objlabel) + '{\n}'

    
def snippetAudioProcessorCppProcessBlock(objlabel):
    code = ""
    code += indent("\n// Recover left data.")
    code += indent("\nfloat* leftData = buffer.getWritePointer(0);\n")
    code += indent("\n// Set right data equal to left data if plugin is mono.")
    code += indent("\nfloat* rightData = buffer.getWritePointer(0);")
    code += indent("\nif (totalNumInputChannels==2)")
    code += indent("\n{")
    code += indent(indent("\nrightData = buffer.getWritePointer(1);"))
    code += indent("\n}\n")
    code += indent("\n// Walk over buffer elements")
    code += indent("\nfor(long i=0; i<buffer.getNumSamples(); i++)")
    code += indent("\n{")
    temp = indent("\n// Single input of PHS is average of left and right data.")
    temp += indent("\nphsInput = (leftData[i] + rightData[i])/2.f;")
    temp += indent("\n")
    temp += indent("\n// Update PHS input.")
    temp += indent("\n{0}.set_u(phsInput, phsInputIndex);\n".format(objlabel))
    temp += indent("\n// Core PHS update.")
    temp += indent("\n{0}.update();\n".format(objlabel))
    temp += indent("\n// Get PHS ouput.")
    temp += indent("\nleftData[i] = {0}.y(phsOutputIndex);\n".format(objlabel))
    temp += indent("\nif (totalNumOutputChannels==2)")
    temp += indent("\n{")
    temp += indent(indent("\nrightData[i] = {0}.y(phsOutputIndex);".format(objlabel)))
    temp += indent("\n}")
    code += indent(temp)
    code += indent("\n}")
    return code


def snippetAudioProcessorCppPrepareToPlay(objlabel):
    return """
    // Update PHS sample-rate.
    {0}.set_sampleRate(sampleRate);""".format(objlabel)

        