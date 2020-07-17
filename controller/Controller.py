import os
import sys, getopt
import fnmatch
import subprocess
import json

from pathlib import Path
from glob import glob
from os import getcwd


class Controller:


    def __init__(self):
        self.CurrentPath = getcwd()
        result = self.checkCommand(sys.argv[1:])
        if not result:
            print("Something went wrong, check the configuration file. I don't understand something there.")
            input("Press enter to exit.")

        sys.exit()


    def getAnswere(self):
        answere = ""
        while True:
            if answere.lower() == "a" or answere.lower() == "w" or answere.lower() == "n":
                break
            else:
                answere = input("[a/w/n] : ")
        return answere.lower()


    def checkCommand(self,argv):
        config = []

        # Setup the commands
        try:
            opts, args = getopt.getopt(argv,"hp:c:t",["help","path=","command=","this"])
        except getopt.GetoptError:
            print ('startupapps.exe -p <path/to/file/or/folder> -c <cmd that is in ENV PATH>')
            sys.exit(2)

       
        if opts == []:
            self.run()
            return True

        for opt, arg in opts:
            if opt == '-h':
                print ('startupapps.exe -p <path/to/file/or/folder> -c <cmd that is in ENV PATH>')
                sys.exit()
            elif opt in ("-p", "--path"):
                config.append({"path":arg})
            elif opt in ("-c", "--command"):
                config.append({"command":arg})
            elif opt in ("-t", "--this"):
                config.append({"path": self.CurrentPath})

        # By default, we create a new file and the name is the folder name
        answere = "w"
        fileName = self.CurrentPath.split('\\')[-1:][0]+".stapps"

        # If a config file exists, check append or overright
        if Path(self.CurrentPath+"\\"+fileName).exists():
            print(f"{fileName} already exists, would you like to overright[w], append[a] or create a new[n] file?")
            answere = self.getAnswere()

            if answere == "n":
                fileName = input("[eg: myfile] : ")+".stapps"
                answere = "w"


        with open(self.CurrentPath+"\\"+fileName,answere,encoding="utf8") as newConfig:
            json.dump(config, newConfig)

        print('Config file was generated successfully, you can edit it manually in notepad if you made a mistake ;) \n')
        input('Press any key to exit')
        return True


    def getFileChoice(self,listOfChoices):
        answere = "999"
        while True:
            if answere not in str(listOfChoices):
                answere = input('[Run] : ')
            else:
                break

        return int(answere)


    def run(self):
        listOfFiles = glob("*.stapps")

        if len(listOfFiles) > 1:
            print(f'\n{len(listOfFiles)} config files exists in the directiory, Which one would you like to run? \n')

            choices = []
            for i,configFile in enumerate(listOfFiles):
                print(f'[{i}] : {configFile}')
                choices.append(i)
            
            configFileName = listOfFiles[self.getFileChoice(choices)]
        else:
            try:
                configFileName = listOfFiles[0]
            except IndexError:
                print("Could not find a config file! First setup a config file, then run the app")
                self.help()

        with open(self.CurrentPath+"\\"+configFileName,"r",encoding="utf8") as config:

            try:
                newList = json.loads(config.read())
            except json.decoder.JSONDecodeError as e:
                print(e)
                print("Check your .stapps file, make sure all paths are escaped 'C:\\\\Users\\\\user\\\\' not 'C:\\Users\\user\\'")
                print("Use double backslash not single backslash")
                input("Press enter to exit")

            for row in newList:
                try:
                    command = row['command']
                    check = os.system(command)
                    if check == 1:
                        subprocess.call(f"start {command}",shell=True)
                except KeyError:
                    pass

                try:
                    path = row['path'].replace("/","\\")
                    subprocess.call("explorer "+path, shell=True)
                except KeyError:
                    pass

        return True


    def help(self):
        print("""
[-h] => Help
[-p] => Path to folder | eg: startupapps.exe -p "C:/path/to/folder/one" -p "C:/path/to/folder/two"
[-c] => Path to executable/environment variable | eg: -c "python C:\folder\example.py" -c "code ." -c "chrome github.com"

To execute the startup app, don't pass any paramenters

* make sure you have a config.stapps in the current directory,
if you do not, create one by passing in parameters to this app.
        """)
        input("Press enter to exit")