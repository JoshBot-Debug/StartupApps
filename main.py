from os import getcwd
from controller.Controller import Controller
import subprocess

if __name__ == "__main__":
    CurrentFile = getcwd()+'/StartupApps.config'
    Controller(CurrentFile)
