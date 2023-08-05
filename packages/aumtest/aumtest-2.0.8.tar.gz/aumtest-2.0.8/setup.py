# coding:utf-8


#############################################
# File Name: setup.py
# Author: TA_QA
# Created Time: 2021-3-27
#############################################

import sys
import setuptools

with open("README.md", "r", encoding='UTF-8') as fh:
    long_description = fh.read()

info = sys.version_info
if info.major == 3 and info.minor <= 7:
    requires = [
        'PyYAML>=5.1.2',
        'wd>=1.0.1',
        'selenium',
        'colorama',
        'opencv-contrib-python==3.4.2.16'
    ]
else:
    requires = [
        'PyYAML>=5.1.2',
        'wd>=1.0.1',
        'selenium',
        'colorama',
        'opencv-contrib-python'
    ]
setuptools.setup(
    name="aumtest",
    version="2.0.8",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={'aumtest/result':['resource/*']},
    python_requires='>=3.6.3',
    install_requires=requires,
    entry_points={
        'console_scripts':[
            'aumtest = aumtest.aumtest_runner:main'
        ]
    }
)