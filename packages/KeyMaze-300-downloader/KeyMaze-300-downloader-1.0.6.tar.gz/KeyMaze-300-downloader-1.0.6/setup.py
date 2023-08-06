#!/usr/bin/env python
# -*- coding: utf-8 -*-
import setuptools
setuptools.setup(
    name='KeyMaze-300-downloader',
    version='1.0.6',
    url='https://pypi.org/project/KeyMaze-300-downloader/:q',
    author='Vincent-Xavier JUMEL',
    author_email='endymion@thetys-retz.net',
    description="Keymaze 300",
    requires=['serial'],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    data_files=[('/etc/udev/rules.d',['src/etc/udev/rules.d/90-KeyMaze300.rules']),('/usr/share/km',['src/usr/share/km/firsttrackpoints.bin','src/usr/share/km/nexttrackpoints.bin','src/usr/share/km/waypoints.bin'])],
    license='GPL-3',
    scripts=['src/usr/km-downloader']
)
