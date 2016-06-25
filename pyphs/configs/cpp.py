# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 12:45:58 2016

@author: Falaize
"""

eigen_path = '/Users/Falaize/Documents/DEV/c++/bibliothèques/eigen'

xcode_template_path = '/Users/Falaize/Documents/DEV/c++/xcode_template'

cpp_build_and_run_script = """

echo "Copy xcode template"
mkdir phobj_path/xcode
cp -r """ + xcode_template_path + """/* phobj_path/xcode

echo "Copy cpp files"
cp -r phobj_path/cpp/* phobj_path/xcode/xcode_template/

echo "Build release"
xcodebuild -project phobj_path/xcode/xcode_template.xcodeproj -alltargets \
-configuration Release

echo "Run"
phobj_path/xcode/build/Release/xcode_template

"""
