from os import getcwd
from controller.Controller import Controller

if __name__ == "__main__":
    CurrentFile = getcwd()+'/StartupApps.config'
    Controller(CurrentFile)