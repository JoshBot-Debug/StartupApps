import os
import sys
import fnmatch
from pathlib import Path
import subprocess

class Controller:

    COMMAND_LIST = ["-h","-p"]

    def __init__(self,CurrentFile):
        self.CurrentFile = CurrentFile
        out = self.checkCommand()
        if not out:
            print("Something went wrong, check the configuration file. I don't understand something there.")
        else:
            exit(1)

    def checkCommand(self):
        command = sys.argv

        if len(command) == 1:
            return self.run()

        if len(command) >= 2:
            if command[1] in self.COMMAND_LIST:

                if command[1] == "-h":
                    self.help()

                if command[1] == "-p":
                    for i,pth in enumerate(command):
                        if i > 1:
                            with open(self.CurrentFile,"w",encoding="utf8") as config:
                                for row in command:
                                    config.write(row+"\n")

                return True
        return False


    def run(self):
        if Path(self.CurrentFile).exists():
            with open(self.CurrentFile,"r",encoding="utf8") as config:
                data = config.read().replace("\n"," ").split("-p")
                for i,row in enumerate(data):
                    if i > 0:
                        if fnmatch.fnmatch(row, "*:/*") or fnmatch.fnmatch(row, "*:\\*"):
                            correctedSlash = row.replace("/","\\")
                            subprocess.call("explorer "+correctedSlash, shell=True)
                        else:
                            check = os.system(row)
                            if check == 1:
                                subprocess.call(f"start {row}",shell=True)
                return True

        self.help()
        return False


    def help(self):
        print("""
[-h] => Help
[-p] => Path to folder/executable/environment variable

To pass multiple files/folder/etc, seperate the paths by "-p".

To execute the startup app, don't pass any paramenters

* make sure you have a StartupApps.config in the current directory,
if you do not, create one by passing in parameters to this app.
        """)
        input("Press enter to exit")