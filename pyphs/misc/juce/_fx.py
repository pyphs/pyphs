#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 22:32:59 2017

@author: Falaize
"""

import os
from pyphs.numerics.cpp.tools import indent
from pyphs.config import VERBOSE


def snippets(objlabel, src_folder, InputIndex, OutputIndex):

    if VERBOSE >= 1:
        print('Generate Juce C++ snippets rlc...')

    def write(name, content):
        path = os.path.join(src_folder, name + '.txt')
        if VERBOSE >= 1:
            print('    Write {}'.format(path))
        with open(path, 'w') as file:
            for line in content.splitlines():
                file.write(line + '\n')

    content = snippetAudioProcessorHDeclare(objlabel,
                                            InputIndex,
                                            OutputIndex)
    write('Processor_H_1-Declare', content)

    content = snippetAudioProcessorHInclude(src_folder)
    write('Processor_H_2-Include', content)

    content = snippetAudioProcessorCppInstanciation(objlabel)
    write('Processor_CPP_1-Instanciation', content)

    content = snippetAudioProcessorCppProcessBlock(objlabel)
    write('Processor_CPP_2-ProcessBlock', content)

    content = snippetAudioProcessorCppPrepareToPlay(objlabel)
    write('Processor_CPP_3-PrepareToPlay', content)


def snippetAudioProcessorHDeclare(objlabel, InputIndex, OutputIndex):

    code = """
//=========================================================================
// Define PHS object (see AudioProcessor contructor for initialization).
{0} {1};

//=========================================================================
// Allocate some memories.
unsigned int {1}InputIndex = {2};
unsigned int {1}OutputIndex = {3};
double phsInput = 0.f;""".format(objlabel.upper(),
                                 objlabel.lower(),
                                 InputIndex,
                                 OutputIndex)
    return indent(code)


def snippetAudioProcessorHInclude(src_folder):
    include = os.path.join('..', src_folder, 'core.h')
    return '#include "{}"'.format(include)


def snippetAudioProcessorCppInstanciation(objlabel):
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
    temp += indent("\n{0}.set_u(phsInput, {0}InputIndex);\n".format(objlabel))
    temp += indent("\n// Core PHS update.")
    temp += indent("\n{0}.update();\n".format(objlabel))
    temp += indent("\n// Get PHS ouput.")
    temp += indent("\nleftData[i] = {0}.y({0}OutputIndex);\n".format(objlabel))
    temp += indent("\nif (totalNumOutputChannels==2)")
    temp += indent("\n{")
    temp += indent(indent("\nrightData[i] = {0}.y({0}OutputIndex);".format(objlabel)))
    temp += indent("\n}")
    code += indent(temp)
    code += indent("\n}")
    return code


def snippetAudioProcessorCppPrepareToPlay(objlabel):
    return """
    // Update PHS sample-rate.
    {0}.set_sampleRate(sampleRate);""".format(objlabel)


if __name__ == '__main__':
    from pyphs.examples.rlc.rlc import core
    path = '/Users/afalaize/Desktop/rlc/src'
    method = core.to_method()
    method.to_cpp(path=path)
    snippets('myobject', path, 0, 1)

