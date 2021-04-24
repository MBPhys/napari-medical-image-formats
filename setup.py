#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup, find_packages


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


# Add your dependencies in requirements.txt
# Note: you can add test-specific requirements in tox.ini
requirements = []
with open('requirements.txt') as f:
    for line in f:
        stripped = line.split("#")[0].strip()
        if len(stripped) > 0:
            requirements.append(stripped)


# https://github.com/pypa/setuptools_scm
use_scm = {"write_to": "napari_medical_image_formats/_version.py"}

setup(
    name='napari-medical-image-formats',
    author='Marc Boucsein, Marc Buckmakowski',
    license='BSD-3',
    url='https://github.com/MBPhys/napari-medical-image-formats',
    description='A Plugin in order to read medical image formats such as DICOM and NIfTI',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    python_requires='>=3.7',
    install_requires=requirements,
    use_scm_version=use_scm,
    setup_requires=['setuptools_scm'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Framework :: napari',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
    ],
    entry_points={
        'napari.plugin': [
            'napari-medical-image-formats = napari_medical_image_formats',
        ],
    },
)
