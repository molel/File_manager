import os
import shutil


class FileManager:

    def __init__(self):
        self.path = os.getcwd() + "\\"
        self.commands = {
            "createdir": self.createDir,
            "removedir": self.removeDir,
            "changedir": self.changeDir,
            "createfiles": self.createFiles,
            "writefile": self.writeFile,
            "readfile": self.readFile,
            "removefiles": self.removeFiles,
            "copyfiles": self.copyFiles,
            "movefiles": self.moveFiles,
            "renamefile": self.renameFile,

        }
        self.loop()

    def loop(self):
        while True:
            line = input(f"{self.path}> ").split(" ")
            if line != "":
                command, arguments = line[0], line[1:]
                if command in self.commands.keys():
                    self.commands[command](*arguments)
                else:
                    print("There is no such command")

    def createDir(self, *args):
        if len(args) > 1:
            print("Too many arguments")
        else:
            dirName = args[0]
            try:
                os.mkdir(self.path + dirName)
            except Exception as e:
                print(e)

    def removeDir(self, *args):
        if len(args) > 1:
            print("Too many arguments")
        else:
            dirName = args[0]
            try:
                shutil.rmtree(self.path + dirName)
            except Exception as e:
                print(e)

    def changeDir(self, *args):
        if len(args) > 1:
            print("Too many arguments")
        else:
            try:
                os.chdir(args[0])
                self.path = os.getcwd()
            except Exception as e:
                print(e)

    @staticmethod
    def createFiles(*args):
        try:
            for fileName in args:
                if ".txt" not in fileName:
                    fileName += ".txt"
                open(fileName, 'a').close()
        except Exception as e:
            print(e)

    @staticmethod
    def writeFile(fileName, *data):
        try:
            if ".txt" not in fileName:
                fileName += ".txt"
            with open(fileName, 'a') as file:
                file.write(" ".join(data) + "\n")
        except Exception as e:
            print(e)

    @staticmethod
    def readFile(*args):
        if len(args) > 1:
            print("Too many arguments")
        else:
            try:
                fileName = args[0]
                if ".txt" not in fileName:
                    fileName += ".txt"
                with open(fileName, 'r') as file:
                    for line in file:
                        print(line)
            except Exception as e:
                print(e)

    @staticmethod
    def removeFiles(*fileNames):
        try:
            for fileName in fileNames:
                if ".txt" not in fileName:
                    fileName += ".txt"
                os.remove(fileName)
        except Exception as e:
            print(e)

    @staticmethod
    def copyFiles(*args):
        fileNames = args[:-1]
        dirPath = args[-1]
        try:
            for fileName in fileNames:
                if ".txt" not in fileName:
                    fileName += ".txt"
                shutil.copy(fileName, dirPath)
        except Exception as e:
            print(e)

    @staticmethod
    def moveFiles(*args):
        fileNames = args[:-1]
        dirPath = args[-1]
        for fileName in fileNames:
            if ".txt" not in fileName:
                fileName += ".txt"
            shutil.move(fileName, dirPath)

    @staticmethod
    def renameFile(*args):
        if len(args) > 2:
            print("Too many arguments")
        elif len(args) < 2:
            print("Too few arguments")
        else:
            fileName = args[0]
            if ".txt" not in fileName:
                fileName += ".txt"
            newFileName = args[1]
            if ".txt" not in newFileName:
                newFileName += ".txt"
            os.rename(fileName, newFileName)


if __name__ == '__main__':
    fileManager = FileManager()
