# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='text2img',
    version='0.0.55',
    url='https://github.com/tuaplicacionpropia/text2img',
    download_url='https://github.com/tuaplicacionpropia/text2img/archive/master.zip',
    author=u'tuaplicacionpropia.com',
    author_email='tuaplicacionpropia@gmail.com',
    description='Python library for generate images from text.',
    long_description='Python library for generate images svg from text and svg templates.',
    keywords='svg, text, json, generator',
    classifiers=[
      'Development Status :: 4 - Beta',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python', 
      'Programming Language :: Python :: 2.7', 
      'Intended Audience :: Developers', 
      'Topic :: Multimedia :: Graphics',
    ],
    scripts=['bin/text2img', 'bin/text2img.cmd',],
    packages=find_packages(exclude=['tests']),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    license='MIT',
    install_requires=[
        'lxml==3.3.3',
        'hjson==2.0.2',
        'Pillow==3.4.2',
    ],
)

