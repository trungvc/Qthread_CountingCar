import sys
from PyQt5 import uic

with open('m1.py', 'w', encoding='utf-8') as fout:
    uic.compileUi('untitled.ui', fout)
