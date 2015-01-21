from distutils.core import setup
import py2exe
import pygame
setup(#console=['InfoRectMaker.py'],
      windows=['InfoRectMaker.py'],
      options = {"py2exe":
                     {"includes":["pygame", "pickle", "PIL", "tkinter", "tkinter.filedialog", "tkinter.messagebox"]}
      }
)
