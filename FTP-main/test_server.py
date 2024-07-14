import unittest
import socket
from authorization import auto
from time import sleep
HOST = "localhost"  # The remote host
PORT = 50400  # The same port as used by the server
IS_RECONNECT_ENABLED = False

class Test1(unittest.TestCase):
    def test1(self):
        self.assertEqual(main("Test", ["makedir loop", "changedir loop", "createfile new1"]), ['makedir loop',"changedir loop" ,'createfile new1', 'Client disconnected'])
    def test2(self):
        self.assertEqual(main("Test", ["makedir loop", "changedir loop", "createfile new1"]), ['Incorrect directory name', 'changedir loop', 'Its file exists', 'Client disconnected'])

    def test3(self):
        self.assertEqual(main("Test",
                        ["changedir loop", "getpath", "createfile new3", "writefile new3 Hello!"]), ['changedir loop', '/home/odinmary/5_FTP_server/Test/loop', 'createfile new3', 'writefile new3 Hello!', 'Client disconnected'])

def main(name, acts):
    is_started = False
    report = []
    while IS_RECONNECT_ENABLED or not is_started:
        is_started = True
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((HOST, PORT))
            # Send login
            sock.send(name.encode())
            print(name)
            sleep(1)
            for act in acts:
                if act == "exit":
                    report.append("Close by client")
                    return report
                    break
                # Send
                sock.send(act.encode())
                # Receive
                data = sock.recv(1024).decode()

                if not data:
                    report.append("Closed by server")
                    return report
                    break
                report.append(data)
            sock.close()
            report.append("Client disconnected")
            return report
            print(report)


if __name__ == "__main__":
    print(main("Test", ["makedir loop", "changedir loop", "createfile new1"]))
    # print(main("Test", ["makedir loop", "changedir loop", "createfile new1"]))
    # print(main("Test", ["changedir loop", "getpath", "createfile new3", "writefile new3 Hello!", "removefile new3"]))