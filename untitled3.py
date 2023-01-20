# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 16:39:43 2022

@author: Smurf
"""

from PyQt5 import uic

with open('Hakkında.py','w',encoding=("utf-8"))as fout:
    uic.compileUi('Hakkında.ui', fout)
    
    