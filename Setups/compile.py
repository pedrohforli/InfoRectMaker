from cx_Freeze import setup, Executable

exe=Executable(
     script="InfoRectMaker.py",
     base="Win32Gui",
     )

includefiles=[('confs')]
includes= []
excludes=[]
packages=["os", "tkinter","pygame", "shelve", "PIL"]
setup(
     version = "1.0",
     description = "Obtain the rects inside an image",
     author = "Pedro Forli e Ivan Veronezzi",
     name = "Info Rect Maker",
     options = {'build_exe': {'excludes':excludes,'packages':packages,'include_files':includefiles}},
     executables = [exe]
     )
