# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 23:48:26 2016

@author: Falaize
"""

eigen_path = '/Users/.../eigen'

cpp_build_and_run_script = None

#xcode_template_path = '/Users/.../xcode_template_pyphs'
#cpp_build_and_run_script = """
#
#echo "Copy xcode template"
#mkdir phobj_path/xcode
#cp -r """ + xcode_template_path + """/* phobj_path/xcode
#
#echo "Copy cpp files"
#cp -r phobj_path/cpp/* phobj_path/xcode/xcode_template_pyphs/
#
#echo "Build release"
#xcodebuild -project phobj_path/xcode/xcode_template_pyphs.xcodeproj -alltargets \
#-configuration Release
#
#echo "Run"
#phobj_path/xcode/build/Release/xcode_template_pyphs
#
#"""
