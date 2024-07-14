import os
import shutil
import pathlib
from time import sleep

PATH = "/home/odinmary/5_FTP_server"
class FileManager:
    def __init__(self, name):
        # self.first_path = str(os.getcwd())
        if name == "admin":
            self.root = PATH
            self.first_path = self.root
            self.current_path = self.first_path
        else:
            self.first_path = os.path.join(PATH, name)
            self.current_path = self.first_path
            if not os.path.isdir(name):
                os.mkdir(name)
            os.chdir(self.first_path)
        self._limit = 100

    def dirSize(self, path_):
        size = 0
        for path, dirs, files in os.walk(path_):
            for dir in dirs:
                size += self.dirSize(os.path.join(path, dir))
            for file in files:
                size += os.path.getsize(os.path.join(path_, file))
        return size


    # 1
    def makedir(self, name):
        try:
            os.mkdir(name)
            # if self.dirSize(self.first_path)>self._limit:
            #     os.rmdir(name)
            #     return "Limit reached"
        except:
            return "Incorrect directory name"

    # 2
    def removedir(self, name):
        try:
            os.rmdir(name)
        except:
            return "This directory doesn`t exist in this path"
        return True
    # 3
    def changedir(self, name):
        if name == "*up":
            if self.current_path == self.first_path:
                return "You can`t exit the work folder"
            else:
                os.chdir(self.first_path)
        else:
            try:
                os.chdir(name)
                self.current_path=os.path.join(self.first_path, name)
            except:
                return"This directory doesn`t exist in this path"

    # 4
    def createfile(self, name):

        try:
            if not os.path.isfile(os.path.join(self.current_path, name)):
                file = open(name, "w", encoding="utf-8")
            else:
                return "Its file exists"
            # if self.dirSize(self.first_path)>self._limit:
            #     os.remove(name)
            #     return "Limit reached"
        except:
            return "Incorrect file name"


    # 5
    def writefile(self, name, text):

        self.createfile(name)
        try:
            with open(f"{os.path.join(self.first_path, name)}", "w", encoding="utf-8") as f:
                f.write(text)

            # if self.dirSize(self.first_path) > self._limit:
            #     file = open(name, "w", encoding="utf-8")
            #     return "Limit reached"
        except:
            return "You have entered incorrect symbols"

    # 6
    def readfile(self, name):
        try:
            with open(f"{os.path.join(self.first_path,name)}", "r", encoding="utf-8") as f:
                print(f.read())
        except:
            return "This file doesn`t exist"

    # 7
    def removefile(self, name):
        try:
            os.remove(name)
        except:
            return "This file doesn`t exist"

    # 8
    def copyfile(self, filename, dirname):
        try:
            from_dir = os.path.join(self.first_path, filename)
            to_dir = os.path.join(os.path.join(self.first_path, dirname), filename)
            shutil.copyfile(from_dir, to_dir)

        except:
            return "This file or directory doesn`t exist"

    # 9
    def movefile(self, name1, name2):
        try:
            shutil.move(name1, name2)
        except:
            return "Incorrect file name"

    # 10
    def renamefile(self, name1, name2):
        try:
            os.replace(name1, name2)
        except:
            return "Incorrect file name"

    # 11
    def showall(self):
        return " ".join(os.listdir())

    def free(self):
        return self._limit-self.dirSize(self.first_path)

    def getpath(self):
        return self.current_path

    def create_user_dir(self, name):
        # self.makedir(name)
        self.first_path = os.path.join(self.first_path, name)
        self.current_path = os.path.join(self.current_path, name)

    def help(self):
        return '''Choose action:
    +------------+-----------+-----------+ 
    | makedir    | removedir | changedir |
    +------------+-----------+-----------+ 
    | createfile | writefile | readfile  |
    +------------+-----------+-----------+ 
    | removefile | copyfile  | movefile  |
    +------------+-----------+-----------+ 
    | renamefile | showall   | getpath   |
    +------------+-----------+-----------+
    | quit       | close     | help      |
    +------------+-----------+-----------+'''


def handle_ftp_request(act: str, session):
    # session = FileManager()
    # print(session.current_path)
    act = act.split()
    act_steps = [act[i] if i > 0 else act[i].lower() for i in range(len(act))]
    match act_steps[0]:
        case "makedir":
            return session.makedir(act_steps[1])
        case "removedir":
            return session.removedir(act_steps[1])
        case "changedir":
            return session.changedir(act_steps[1])
        case "createfile":
            return session.createfile(act_steps[1])
        case "writefile":
            return session.writefile(act_steps[1], act_steps[2])
        case "readfile":
            return session.readfile(act_steps[1])
        case "removefile":
            return session.removefile(act_steps[1])
        case "copyfile":
            return session.copyfile(act_steps[1], act_steps[2])
        case "movefile":
            return session.movefile(act_steps[1], act_steps[2])
        case "renamefile":
            return session.renamefile(act_steps[1], act_steps[2])
        case "showall":
            return session.showall()
        case "getpath":
            return session.getpath()





if __name__ == "__main__":
    print(help())
    # print(pathlib.Path.cwd().joinpath("logs"))
    # sec = FileManager("nnn")
    # sec.createfile("rem")
    # sleep(5)
    # sec.removefile("rem")

    # file = open("rem", "w", encoding="utf-8")

    # name = input("Input login: ")
    # session = FileManager(name)
    # while True:
    #     print(session.help())
    #     act = input("Input action: ")
    #     if act == "quit":
    #         break
    #     f = handle_ftp_request(act, session)
    #     if f:
    #         print(f)