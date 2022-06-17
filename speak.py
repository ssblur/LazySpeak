"""
    A quickly cobbled-together cross-platform speech proxy.
    This just detects if you have an existing compatible TTS library available and attempts to use it if so.
    Can be run standalone as a basic speech synthesizer proxy.
    Usage: "python speak.py {Text to read}"
    Author: Patrick Emery
    Contact: info@pemery.co
"""
import os 
from subprocess import Popen
from json import dumps
from platform import system
from distutils.spawn import find_executable
import sys


def win_ptts_speak(input):
    Popen([
        "ptts.exe",
        input
    ]).wait()

def win_SAPI_speak(input):
    Popen([
        "powershell.exe",
        "-Command", 
        f"Add-Type –AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak({dumps(input)});"
    ]).wait()

def win_cscript_speak(input):
    cwd = os.path.dirname(os.path.realpath(__file__))
    Popen(
        [
            "cscript.exe",
            "speak.vbs",
            input
        ],
        cwd=os.sep.join([cwd, "resources"])
    ).wait()

def osx_say_speak(input):
    Popen([
        "say",
        input
    ]).wait()

def x_spd_speak(input):
    Popen([
        "spd-say",
        input
    ]).wait()

def linux_espeak_speak(input):
    Popen([
        "espeak",
        input
    ]).wait()

def speak(input: str):
    """Attempt to speak using native tts commands.
    This is intended to fail if no suitable speak function is found.
    This will fail in any case if this OS is not based on Windows-NT, OSX Darwin, or Linux.
    
        Args:
            input: The string to attempt to say
    """
    if system() == "Windows":
        if find_executable("ptts.exe"):
            win_ptts_speak(input)
        elif find_executable("cscript.exe"):
            win_cscript_speak(input)
        elif find_executable("powershell.exe"):
            win_SAPI_speak(input)
        else:
            raise RuntimeError("No native speech synthesizer found. System appears to be Windows, please enable VBS or PowerShell and ensure SAPI is enabled, or install Peter's Text-to-Speech.")
    elif system() == "Darwin":
        if find_executable('say'):
            osx_say_speak(input)
        elif find_executable('spd-say'):
            x_spd_speak(input)
        else:
            raise RuntimeError("No native speech synthesizer found. System appears to be OSX Darwin, is system up-to-date? If say is not available on your system, spd-say is suggested.")
    elif system() == "Linux":
        if find_executable('spd-say'):
            x_spd_speak(input)
        elif find_executable('espeak'):
            linux_espeak_speak(input)
        else:
            raise RuntimeError("No native speech synthesizer found. System appears to be Linux, spd-say is suggested.")
    else:
        raise RuntimeError("No native speech synthesizer found. Aborting.")
                
if __name__ == "__main__":
    speak(" ".join(sys.argv[1:]))