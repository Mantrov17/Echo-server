import socket


def user(host='localhost', port=5001):
    try:
        with socket.socket() as s:
            print(">>> Соединение с сервером")
            s.connect((host, port))
            while True:
                inp = input(">>> Input: ")
                if inp == "exit":
                    s.close()
                    print(">>> Разрыв соединения с сервером")
                    break
                print(">>> Отправка данных серверу")
                s.send(inp.encode())
                print(">>> Прием данных от сервера")
                data = s.recv(1024)
                datad = data.decode()
                if datad == "":
                    s.close()
                    print(">>> Разрыв соединения с сервером")
                    break
                print('>>> Echoing: ', datad)

    except KeyboardInterrupt:
        exit(0)


if __name__ == '__main__':
    user()