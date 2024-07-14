import json
import getpass
import os


def create_secret_file():
    print("Enter file name: ")
    name = input()
    f = open(f"{name}.json", "w")


def register(filename="authorization.json"):
    # print("Input your name: ")
    name = input("Your name: ")
    # print("Input your password")\
    password = getpass.getpass(prompt="Password: ", stream=None)
    if os.stat(filename).st_size == 0:
        password_list = {name: password}
    else:
        with open(filename, "rb") as file:
            password_list = json.load(file)
            password_list[name] = password
    with open(filename, "w") as file:
        json.dump(password_list, file)
    return name


def login(filename="authorization.json"):
    # print("Input your name: ")
    name = input("Your name: ")
    # print("Input your password")
    password = getpass.getpass(prompt="Password: ", stream=None)
    with open(filename, "r") as file:
        password_list = json.load(file)
        if len(password_list) != 0:
            for key in password_list.keys():
                if name == key:
                    if password == password_list[name]:
                        return name
                    else:
                        return False
            return False
        return False


def auto():
    act = int(input('''Choose action: 1 Register new user 2 Log in: '''))

    if act == 1:
        return register()
    if act == 2:
        return login()


if __name__ == "__main__":
    auto()