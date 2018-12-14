import sys
from cx_Freeze import setup, Executable

setup(
    name = "Explosions",
    version = "5 bajillion",
    description = "A game come on",
    executables = [Executable("main.py", base="Win32GUI")])
