#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 17:20:52 2018

TODO: rewrite? cuda_objects not visible in py36.
Solution: took out . from 'from .retina import Retina'.
TODO: Python version check should go here...

@author: Piotr Ozimek
"""

from .retina import Retina
import retinavision.utils

datadir = join(dirname(dirname(__file__)), "data")

del dirname, join
