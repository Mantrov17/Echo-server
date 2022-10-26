import socket
import pickle

sock = socket.socket()
sock.connect(('localhost', 9090))

# msg = 'Hello, world!'
msg = 'Hello, '
sock.send(msg.encode())
msg = 'world!'
sock.send(msg.encode())

print(sock.recv(1024).decode())

sock.close()
