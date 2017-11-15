#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 22:32:59 2017

@author: Falaize
"""

import os
from pyphs.numerics.cpp.tools import indent
from pyphs.config import VERBOSE, CONFIG_CPP


# -----------------------------------------------------------------------------

def jucelabel(objlabel):
    return objlabel[0].upper() + objlabel[1:].lower()


# -----------------------------------------------------------------------------

def method2jucefx(method, objlabel=None, io=None, inits=None, params=None,
                  subs=None, path=None, config=None):
    """
    Generate the c++ sources for a pyphs.Method and a bunch of c++ snippets
    to use in a Juce FX audio plugin.

    Parameters
    ----------

    method : pyphs.Method
        The object that will be converted to c++.


    objlabel : string (default is None)
        Name of the c++ class.


    io : tuple of lists of ports (default is None)
        Two lists of strings or pyphs Symbols defining the port of the pyphs
        object to be considered as the inputs and outputs of the Juce plugin.
        E.g. io=([u1, u3], (y2, y4)) for a stereo plugin with inputs from the
        ports 1 and 3 and outputs from the ports 2 and 4.


    params : dictionary (default is None)
        Parameters ranges and default values. If not None, params must have an
        entry for each parameter in method.p; the associated value is a tuple
        of three elements (vmin, vmax, init) that is used to define a Juce
        AudioParameterFloat. If None, the value for every parameters is set to
        (0., 1., 0.5)


    path : string (default is None)
        The source files will be generated in the folder 'path/label_Sources/',
        with 'label' the method label.


    inits : dictionary (default is None)
        Dictionary of initialization values `{name: array}` with `name` in
        ('x', 'dx', 'w', 'u', 'p', 'o') and `array` an vector of floats with
        appropriate shape.


    config : dictionary (default is None)
        Dictionary of configuration options (see pyphs.config.CONFIG_NUMERIC).


    subs : dictionary or list (default is None)
        Dictionary or list of dictionaries of substitution parameters.

    """

    if subs is None:
        subs = method.subs

    if params is None:
        params = dict()
        for p in method.p:
            params[p] = (0., 1., 0.5)

    const_u = dict()

    for u in method.u:
        if u in subs.keys():
            const_u[u] = subs[u]

    if io is None:
        io = ([method.u[0], ], [method.y[-1], ])
    inputs, outputs = io
    if len(inputs) > 2 or len(outputs) > 2:
        raise NotImplemented('Only mono or stereo plugin are supported.')

    def get_io_indices(names, attr):
        indices = list()
        for name in names:
            s = method.symbols(str(name))
            i = getattr(method, attr).index(s)
            indices.append(i)
        return indices

    indices_inputs = get_io_indices(inputs, 'u')
    indices_outputs = get_io_indices(outputs, 'y')

    if path is None:
        path = os.getcwd()

    objlabel = method.label.lower()
    cppfolder = os.path.join(path, method.label + '_Sources')
    CONFIG_CPP['float'] = 'float'
    method.to_cpp(objlabel=objlabel, path=cppfolder,
                  inits=inits,
                  config=config)
    snippetsfolder = os.path.join(path, method.label + '_Juce_Snippets')
    parametersFloats = audioParametersFloats(method, indices_inputs,
                                             indices_outputs, params)

    snippets(method, objlabel, snippetsfolder, indices_inputs, indices_outputs,
             parametersFloats)


# -----------------------------------------------------------------------------

def snippets(method, objlabel, path, indices_inputs, indices_outputs, parametersFloats):
    """
    Generate a bunch of small pieces of C++ code (snippets) associated with a
    pyphs c++ object and to be included in a JUCE template to produce an audio
    plugin effect (input-to-output). The file are generated in the folder
    pointed by `src_folder`.


    Parameters
    ----------


    objlabel : str
        Label of the associated pyphs c++ object.


   src_folder : str
       path to the folder that contains the c++ sources for the pyphs object.


   indices_inputs : int or list of ints
       Index of the pyphs object 's port of the that has to be considered as
       the input of the plugin.


   indices_outputs : int or list of ints
       Index of the pyphs object 's port of the that has to be considered as
       the output of the plugin.

    """

    if VERBOSE >= 1:
        print('Generate Juce C++ snippets {}...'.format(objlabel))

    if not os.path.exists(path):
        os.mkdir(path)

    def write(name, content):
        filepath = os.path.join(path, name + '.txt')
        if VERBOSE >= 1:
            print('    Write {}'.format(filepath))
        with open(filepath, 'w') as file:
            for line in content.splitlines():
                file.write(line + '\n')

    content = snippetPluginProcessorHInclude()
    write('Processor_H_1-Include', content)

    content = snippetPluginProcessorHPublic(objlabel,
                                            indices_inputs,
                                            indices_outputs)
    write('Processor_H_2-Public', content)

    content = snippetPluginProcessorHPrivate(method, objlabel, parametersFloats)
    write('Processor_H_3-Private', content)

    content = snippetPluginProcessorCppInstanciation(objlabel, parametersFloats)
    write('Processor_CPP_1-Instanciation', content)

    content = snippetPluginProcessorCppPrepareToPlay(objlabel, parametersFloats)
    write('Processor_CPP_2-PrepareToPlay', content)

    content = snippetPluginProcessorCppProcessBlock(objlabel, len(indices_inputs),
                                                    len(indices_outputs), parametersFloats)
    write('Processor_CPP_3-ProcessBlock', content)

    content = snippetPluginEditorHClassHeader(objlabel)
    write('Editor_H_1-Class_Header', content)

    content = snippetPluginEditorHPublic()
    write('Editor_H_2-Public', content)

    content = snippetPluginEditorHPrivate()
    write('Editor_H_3-Private', content)

    content = snippetPluginEditorCppInstanciation()
    write('Editor_CPP_1-Instanciation', content)

    content = snippetPluginEditorCppPaint(objlabel)
    write('Editor_CPP_2-Paint', content)

    content = snippetPluginEditorCppResized()
    write('Editor_CPP_3-Resized', content)

    content = snippetPluginEditorCppSlidersValuesChanged(objlabel)
    content += snippetPluginEditorCppTimerCallback(objlabel)
    content += snippetPluginEditorCppGetParameterForSlider(objlabel)
    write('Editor_CPP_4-Functions', content)





# -----------------------------------------------------------------------------

def snippetPluginProcessorHInclude():
    include = os.path.join('..', 'PyPHS_Sources', 'core.h')
    return '#include "{0}"'.format(include)


def audioParametersFloats(method, indices_inputs, indices_outputs, params,
                          vmin=-2., vmax=2., vinit=0.):
    sliders = list()
    for i, ind in enumerate(indices_inputs):
        label = 'inputGain{0}'.format(i+1)
        sliders.append({label: {'vmin': vmin,
                                'vmax': vmax,
                                'vinit': vinit}})

    for i, ind in enumerate(indices_outputs):
        label = 'outputGain{0}'.format(i+1)
        sliders.append({label: {'vmin': vmin,
                                'vmax': vmax,
                                'vinit': vinit}})

    for i, par in enumerate(params.keys()):
        label = str(par)
        sliders.append({label: {'vmin': params[par][0],
                                'vmax': params[par][1],
                                'vinit': params[par][2]}})
    return sliders


def snippetPluginProcessorHPublic(objlabel, indices_inputs, indices_outputs):

    code = """
//=========================================================================
// Define PHS object (see PluginProcessor constructor for initialization).
{0} {1};
""".format(objlabel.upper(), objlabel.lower())
    code += """
//=========================================================================
// Inputs and Outputs ports
"""
    nu = len(indices_inputs)
    code += "unsigned int {0}InputIndices[{1}] = ".format(objlabel.lower(), nu)
    code += "{"
    code += ("{}, "*nu).format(*indices_inputs)[:-2]
    code += "};\n"
    ny = len(indices_outputs)
    code += "unsigned int {0}OutputIndices[{1}] = ".format(objlabel.lower(), ny)
    code += "{"
    code += ("{}, "*ny).format(*indices_outputs)[:-2]
    code += "};\n"
    code += """
//=========================================================================
// Input value
double phsInput[{0}] = """.format(nu) + "{" + ("{}, "*nu).format(*([0.,]*nu))[:-2] + "};\n"
    return indent(code)


def snippetPluginProcessorHPrivate(method, objlabel, parametersFloats):

    code = """
//=========================================================================
// Define controled parameters\n"""
    for p in parametersFloats:
        code += "\nAudioParameterFloat* {0};\n".format(list(p.keys())[0])
        code += "float previous{0};\n".format(list(p.keys())[0][0].upper()+
                                              list(p.keys())[0][1:])
        if not (list(p.keys())[0].startswith('inputGain') or list(p.keys())[0].startswith('outputGain')):
            index = method.p.index(method.symbols(list(p.keys())[0]))
            code += "unsigned int index{0} = {1};\n".format(list(p.keys())[0][0].upper()+
                                                  list(p.keys())[0][1:], index)
    return indent(code)


def snippetPluginProcessorCppInstanciation(objlabel, parametersFloats):
    code = """#ifndef JucePlugin_PreferredChannelConfigurations
     : AudioProcessor (BusesProperties()
                     #if ! JucePlugin_IsMidiEffect
                      #if ! JucePlugin_IsSynth
                       .withInput  ("Input",  AudioChannelSet::stereo(), true)
                      #endif
                       .withOutput ("Output", AudioChannelSet::stereo(), true)
                     #endif
                       ),
#endif
{}()
""".format(objlabel)
    code += '{\n'
    code += indent("//=========================================================================\n// Define controled parameters\n")
    for p in parametersFloats:
        temp = """\n
addParameter ({0} = new AudioParameterFloat (
                    "{0}",    // parameter ID
                    "{1}",    // parameter name
                    {2},      // mininum value
                    {3},      // maximum value
                    {4}      // default value
                 )
             );"""
        ID = list(p.keys())[0]
        name = ID[0].upper() + ID[1:].lower()
        vmin = p[ID]['vmin']
        vmax = p[ID]['vmax']
        vinit = p[ID]['vinit']
        code += indent(temp.format(ID, name, vmin, vmax, vinit))
    code += '\n}\n'
    return code


def applygain(io='In', i=0):
    current = 'current{0}putGain{1}'.format(io, i+1)
    previous = 'previous{0}putGain{1}'.format(io, i+1)
    gain = '{0}putGain{1}'.format(io.lower(), i+1)

    code = "\nconst float {0} = *{1};".format(current, gain)
    code += "\nif ({0} == {1})".format(current, previous)
    code += "\n{"
    code += "\n    buffer.applyGain ({1}, 0, buffer.getNumSamples(), pow(10., {0}));".format(current, i)
    code += "\n}"
    code += "\nelse"
    code += "\n{"
    code += """
    buffer.applyGainRamp ({2}, 0, buffer.getNumSamples(), pow(10., {1}), pow(10., {0}));
    {1} = {0};""".format(current, previous, i)
    code += "\n}"
    return indent(code)


def applyparameter(objlabel, name):
    current = 'current{0}'.format(name[0].upper() + name[1:])
    previous = 'previous{0}'.format(name[0].upper() + name[1:])
    index = 'index{0}'.format(name[0].upper() + name[1:])
    par = '{0}'.format(name)
    code = "// Update PHS parameter {}".format(name)
    code += indent("\n{2} = {0} + (*{1}-{0})*(float(i)/buffer.getNumSamples());".format(previous, par, current))
    code += indent("\n{0}.set_p({1}, {2});\n".format(objlabel, current, index))
    return code

def snippetPluginProcessorCppProcessBlock(objlabel, ninputs, noutputs, parametersFloats):
    code = """{
    const int totalNumInputChannels  = getTotalNumInputChannels();
    const int totalNumOutputChannels = getTotalNumOutputChannels();
"""
    code += indent("\n// Apply input gains")
    for i in range(ninputs):
        code +=applygain('In', i)
    code += indent("\nfloat* leftData = buffer.getWritePointer(0);\n")
    if ninputs > 1:
        code += indent("\n// Get right data.")
        code += indent("\nfloat* rightData;")
        code += indent("\nif (totalNumInputChannels==2)")
        code += indent("\n{")
        code += indent(indent("\nrightData = buffer.getWritePointer(1);"))
        code += indent("\n}\n")
    if len(parametersFloats) > 2:
        for p in parametersFloats:
            if not (list(p.keys())[0].startswith('inputGain') or list(p.keys())[0].startswith('outputGain')):
                current = 'current{0}'.format(list(p.keys())[0][0].upper() + list(p.keys())[0][1:])
                previous = 'previous{0}'.format(list(p.keys())[0][0].upper() + list(p.keys())[0][1:])
                code += indent('\nfloat {0} = {1};'.format(current, previous))
        code += indent("\n")
    code += indent("\n// Walk over buffer elements")
    code += indent("\nfor(unsigned int i=0; i<buffer.getNumSamples(); i++)")
    code += indent("\n{")
    temp = indent("\n// Update PHS input 1.")
    temp += indent("\n{0}.set_u(leftData[i], {0}InputIndices[0]);\n".format(objlabel))
    temp += indent("\n")
    if ninputs > 1:
        temp += indent("\n// Update PHS input 2.")
        temp += indent("\nif (totalNumInputChannels==2)")
        temp += indent("\n{")
        temp += indent(indent("\n{0}.set_u(rightData[i], {0}InputIndices[1]);\n".format(objlabel)))
        temp += indent("\n}")
        temp += indent("\n")
    if len(parametersFloats) > 2:
        for p in parametersFloats:
            if not (list(p.keys())[0].startswith('inputGain') or list(p.keys())[0].startswith('outputGain')):
                temp += applyparameter(objlabel, list(p.keys())[0])
    temp += indent("\n// Core PHS update.")
    temp += indent("\n{0}.update();\n".format(objlabel))
    temp += indent("\n// Get PHS ouput 1.")
    temp += indent("\nleftData[i] = {0}.y({0}OutputIndices[0]);\n".format(objlabel))
    if noutputs > 1:
        temp += indent("\n// Update PHS ouput 2.")
        temp += indent("\nif (totalNumOutputChannels==2)")
        temp += indent("\n{")
        temp += indent(indent("\nrightData[i] = {0}.y({0}OutputIndices[1]);".format(objlabel)))
        temp += indent("\n}")
    code += indent(temp)
    code += indent("\n}\n")
    code += indent("\n// Apply output gains")
    for i in range(noutputs):
        code +=applygain('Out', i)
    if len(parametersFloats) > 2:
        code += indent("\n\n// Save parameters values")
        for p in parametersFloats:
            if not (list(p.keys())[0].startswith('inputGain') or list(p.keys())[0].startswith('outputGain')):
                current = 'current{0}'.format(list(p.keys())[0][0].upper() + list(p.keys())[0][1:])
                code += indent('\n{0} = *{1};'.format(previous, list(p.keys())[0]))
    code += "\n}"
    return code


def snippetPluginProcessorCppPrepareToPlay(objlabel, parametersFloats):
    code = "{" + """
    // Update PHS sample-rate.
    {0}.set_sampleRate(sampleRate);
""".format(objlabel) + "\n    // Init previous parameters"
    for p in parametersFloats:
        label = list(list(p.keys()))[0]
        code += indent("\nprevious{0} = *{1};".format(label[0].upper()+ label[1:], label))
    return code + "\n}"


# -----------------------------------------------------------------------------

def snippetPluginEditorHClassHeader(objlabel):
    code = """class {0}AudioProcessorEditor :
                                public AudioProcessorEditor,
                                private Slider::Listener,
                                private Timer
""".format(jucelabel(objlabel))
    return code

def snippetPluginEditorHPublic():
    code = """\n//==============================================================================
// Slider Listener
void sliderValueChanged (Slider* slider) override;

//==============================================================================
// Slider Drag start
void sliderDragStarted (Slider* slider) override;

//==============================================================================
// Slider Drag end
void sliderDragEnded (Slider* slider) override;

enum
{
    kParamControlHeight = 40,
    kParamLabelWidth = 80,
    kParamSliderWidth = 300
};\n"""
    return indent(code)


def snippetPluginEditorHPrivate():
    code = """
//==============================================================================
// UI Slider callback
void timerCallback() override;

//==============================================================================
// Shortcut for AudioParameter from slider change
AudioParameterFloat* getParameterForSlider (Slider* slider);

//==============================================================================
// Dummy Label
Label noParameterLabel;

//==============================================================================
// Arrays for Sliders and Labels
OwnedArray<Slider> paramSliders;
OwnedArray<Label> paramLabels;
"""
    return indent(code)


def instanciateSlider(name, vmin, vmax, init):
    code = """
    // {0} Slider
    addAndMakeVisible ({0}Slider);
    {0}Slider.setRange ({1}, {2});
    {0}Slider.addListener (this);
    {0}Slider.setValue ({3});

    // {0} Text
    addAndMakeVisible ({0}Label);
    {0}Label.setText ("{0}", dontSendNotification);
    {0}Label.attachToComponent (&{0}Slider, true);
""".format(name, vmin, vmax, init)
    return code


def snippetPluginEditorCppInstanciation():
    code = """,
          noParameterLabel ("noparam", "No parameters available")
"""
    code += "{\n"
    code += """
    const OwnedArray<AudioProcessorParameter>& params = p.getParameters();

    for (int i = 0; i < params.size(); ++i)
    {
        if (const AudioParameterFloat* param = dynamic_cast<AudioParameterFloat*> (params[i]))
        {
            Slider* aSlider;

            paramSliders.add (aSlider = new Slider (param->name));
            aSlider->setRange (param->range.start, param->range.end);
            aSlider->setSliderStyle (Slider::LinearHorizontal);
            aSlider->setValue (*param);

            aSlider->addListener (this);
            addAndMakeVisible (aSlider);

            Label* aLabel;
            paramLabels.add (aLabel = new Label (param->name, param->name));
            addAndMakeVisible (aLabel);
        }
    }
"""
    code += """
    //=========================================================================
    // Place No-Parameter Label
    noParameterLabel.setJustificationType (Justification::horizontallyCentred | Justification::verticallyCentred);
    noParameterLabel.setFont (noParameterLabel.getFont().withStyle (Font::italic));

    //=========================================================================
    // Set window size
    setSize (kParamSliderWidth + kParamLabelWidth,
             jmax (1, kParamControlHeight * paramSliders.size()));

    //=========================================================================
    // Start Timer
    if (paramSliders.size() == 0)
        addAndMakeVisible (noParameterLabel);
    else
        startTimer (100);
"""
    code += "}\n"
    return code


def snippetPluginEditorCppSlidersValuesChanged(objlabel):
    code = '//==============================================================================\n'
    code += '// Sliders listener\n'
    code += "void {0}AudioProcessorEditor::".format(jucelabel(objlabel))
    code += "sliderValueChanged (Slider* slider)\n"
    code += "{"
    temp = """if (AudioParameterFloat* param = getParameterForSlider (slider))
    *param = (float) slider->getValue();"""
    code += indent(temp)
    code += "\n}\n"
    code += '\n//==============================================================================\n'
    code += '// Sliders Drag start\n'
    code += "void {0}AudioProcessorEditor::".format(jucelabel(objlabel))
    code += """sliderDragStarted (Slider* slider)
{
    if (AudioParameterFloat* param = getParameterForSlider (slider))
        param->beginChangeGesture();
}
    """
    code += '\n//==============================================================================\n'
    code += '// Sliders Drag end\n'
    code += "void {0}AudioProcessorEditor::".format(jucelabel(objlabel))
    code += """sliderDragEnded (Slider* slider)
{
    if (AudioParameterFloat* param = getParameterForSlider (slider))
        param->endChangeGesture();
}
    """
    return code


def snippetPluginEditorCppTimerCallback(objlabel):
    code = '\n//==============================================================================\n'
    code += '// Timer Callback \n'
    code += "void {0}AudioProcessorEditor::".format(jucelabel(objlabel))
    code += """
timerCallback()
{
    const OwnedArray<AudioProcessorParameter>& params = getAudioProcessor()->getParameters();
    for (int i = 0; i < params.size(); ++i)
    {
        if (const AudioParameterFloat* param = dynamic_cast<AudioParameterFloat*> (params[i]))
        {
            if (i < paramSliders.size())
                paramSliders[i]->setValue (*param);
        }
    }
}
"""
    return code


def snippetPluginEditorCppGetParameterForSlider(objlabel):
    code = '\n//==============================================================================\n'
    code += '// Get Parameter For Slider \n'
    code += "AudioParameterFloat* {0}AudioProcessorEditor::".format(jucelabel(objlabel))
    code += """
getParameterForSlider (Slider* slider)
{
    const OwnedArray<AudioProcessorParameter>& params = getAudioProcessor()->getParameters();
    return dynamic_cast<AudioParameterFloat*> (params[paramSliders.indexOf (slider)]);
}
"""
    return code


def snippetPluginEditorCppResized():
    code = "{"
    code += """
    Rectangle<int> r = getLocalBounds();
    noParameterLabel.setBounds (r);

    for (int i = 0; i < paramSliders.size(); ++i)
    {
        Rectangle<int> paramBounds = r.removeFromTop (kParamControlHeight);
        Rectangle<int> labelBounds = paramBounds.removeFromLeft (kParamLabelWidth);

        paramLabels[i]->setBounds (labelBounds);
        paramSliders[i]->setBounds (paramBounds);
    }
"""
    code += "}\n"
    return code


def snippetPluginEditorCppPaint(objlabel):
    code = "{" + """
    g.setColour (getLookAndFeel().findColour (ResizableWindow::backgroundColourId));
    g.fillAll();
""".format(objlabel) + "}"
    return code


if __name__ == '__main__':
    from pyphs.examples.bjtamp.bjtamp import core
    core.subsinverse()
    path = '/Users/afalaize/Desktop/bjtamp'
    method = core.to_method()
    io = (['uIN', ],    # inputs
          ['yOUT', ])   # outputs
    inits = {'u': (0, 0, 9.)}
    method2jucefx(method, path=path, io=io, inits=inits)
