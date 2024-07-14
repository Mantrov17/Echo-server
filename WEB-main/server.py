import socket
import os
import threading
from settings import HOST, PORT, WORKING_DIR, REQUEST_SIZE
from check import code_request
from datetime import datetime
import threading
from time import sleep
from threading import Lock
def handle_connection(sock, addr):  # New
    with sock:
        print("Connected by", addr)
        while True:
            try:
                request = conn.recv(REQUEST_SIZE).decode().split("\n")
            except ConnectionError:
                print(f"Client suddenly closed while receiving")
                break
            if not request:
                break

            method, url, protocol = request[0].split(" ")
            url = os.path.join(WORKING_DIR, url[1:])

            if os.path.isdir(url):
                url = os.path.join(url, "index.htm")

            code, body, content_type = code_request(url)

            response = f"HTTP/1.1 {code}\n"
            response += "Server: my_dummy_server\n"
            response += datetime.now().strftime("Date: %a, %d %m %Y %H:%M:%S GMT\n")
            response += f"Content-type: {content_type}\n"
            response += f"Content-length: {REQUEST_SIZE}\n"
            response += "Connection: close\n"
            response += "\n"
            response += f"{body}"

            with lock:
                with open('/home/odinmary/6_Web_server/log/log.txt', 'a+') as log:
                    log.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' || ' + addr[0]
                              + ' || ' + url + f' || {code}\n')

            try:
                conn.send(response.encode())
            except ConnectionError:
                print(f"Client suddenly closed, cannot send")
                break
        print("Disconnected by", addr)


if __name__ == "__main__":
    lock = Lock()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(1)
        while True:
            print("Waiting for connection...")
            conn, addr = server.accept()
            t = threading.Thread(target=handle_connection, args=(conn, addr))  # New
            t.start()
            sleep(2)


# while True:
#
#     conn, addr = server.accept()
#     print("Connected", addr)
#
#     request = conn.recv(8192).decode().split('\n')
#
#     method, url, protocol = request[0].split(' ')
#     print(url)
#     url = os.path.join(WORKING_DIR, url[1:])
#     print(url)
#
#     code = "404 Not Found"
#     body = ""
#     url = os.path.join(url, 'index.htm')
#     if os.path.isfile(url):
#         code = "200 OK"
#         body = open(url, 'r').read()
#         print(f"Body: {body}")
#
#     resp = f'HTTP/1.1 {code}\n'
#     resp += "Server: my_dummy_server"
#     resp += '\n\n'
#     resp += body
#     conn.send(resp.encode())
#     conn.close()
#     print('Connection closed\n')