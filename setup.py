#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os

import please
import please.utils
from please.executors.compiler import compile
from please.utils.form_error_output import form_err_string_by_std
from please.utils.exceptions import PleaseException
import please.log

path = os.path.join(os.path.dirname(please.__file__), 'checkers')
for file in os.listdir(path):
    res,fout, err = None, None, None
    if os.path.splitext(file)[1] == '.cpp':
        res, fout, err = compile(os.path.join(path, file))
        if res.verdict != 'OK':
            print(form_err_string_by_std(fout, err))

from setuptools import setup, find_packages

package_data = {
    'please': ['templates/*.*', 'checkers/*.*'],
    'please.exporter': ['templates/*.*'],
    'please.language': ['mime.types'],
}

entry_points = {
    'console_scripts' : ['please = please.launcher:main']
}

install_requires = [
    'psutil',
    'colorama',
    'HTML.py==0.04',
]

dependency_links = [
    'https://please.googlecode.com/svn/third_party/HTML.py-0.04.zip',
]

develop_requires = [
    'mox',
]

extras_require = {
    'develop' : develop_requires
}

try:
    from setup_extensions.develop import develop
except ImportError as e:
    print('Error while importing develop extension: %s' % (str(e)))

setup_params = {
    'name'             : 'Please',
    'version'          : '0.3',
    'license'          : 'MIT',
    'description'      : 'Tool for programming contest problem maintaining',
    'package_dir'      : {'please': 'please'},
    'packages'         : ['please.' + x for x in find_packages('please')] + ['please'],
    'package_data'     : package_data,
    'install_requires' : install_requires,
    'extras_require'   : extras_require,
    'dependency_links' : dependency_links,
    'entry_points'     : entry_points,
    'cmdclass'         : {'develop' : develop},
}

setup(**setup_params)


import platform
system = platform.system()[0]
if (system == 'W'):
    path = os.getenv('path').replace('"', '').split(';')
    pp = os.path.join(conf.PREFIX, 'scripts')
    if (not (pp in path or (pp + os.sep) in path)):
        req = 'echo Y | reg add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v PATH /t REG_SZ /d "%s;%s"' % (os.getenv('path'), pp)
        os.system(req)

