import sys 
import cx_Freeze
from cx_Freeze import setup, Executable 
build_exe_options = {"packages": ["os","twisted","scrapy","test","cx_Freeze"], "includes": ["lxml._elementpath"],"include_msvcr":True} 

base = "Console"
setup(  name = "MyScript", 
        version = "0.1",
        description = "Demo", 
        options = {"build_exe": build_exe_options}, 
        executables = [Executable("script.py", base=base)]) 
