import socket
import threading
from file_manager import handle_ftp_request, FileManager
from datetime import datetime

import logging
import pathlib

def start_logger():
    path = pathlib.Path.cwd().joinpath("logs")
    path.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger('Server')
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    fh = logging.FileHandler(
        filename=f'logs/{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}_server.log'
    )
    ch.setLevel(logging.ERROR)
    fh.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '[%(asctime)s] - %(levelname)s - %(message)s'
    )

    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger


def handle_connection(conn, addr):
    with conn:
        name = conn.recv(1024).decode()
        print("Connected by", name)
        session = FileManager(name)
        while True:
            # Receive
            try:
                data = conn.recv(1024).decode()
            except ConnectionError:
                logger.warning(f"ConnectionError. Client suddenly closed while receiving")
                print(f"Client suddenly closed while receiving")
                break
            print(f"Received: {data} from: {addr}")
            logger.info(f"Received: {data} from: {addr}")
            if not data:
                break
            # Process
            if data == "close":
                break
            # handle client request
            try:
                f = handle_ftp_request(data, session)
                if f:
                    data = f
            except IOError:
                print("Incorrect action requested")
                logger.error("Incorrect action requested")
            # send answer
            if data:
                try:
                    conn.send(data.encode())
                except ConnectionError:
                    print(f"Client suddenly closed, cannot send")
                    logger.error("Client suddenly closed, cannot send")
                    break

        logger.info("Disconnected")
        print("Disconnected by", addr)


def get_user_name(conn, addr):
    with conn:
        try:
            name = conn.recv(1024).decode()
            return name
        except ConnectionError:
            return False


HOST = ""
PORT = 50400

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv_sock:
        serv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serv_sock.bind((HOST, PORT))
        serv_sock.listen(5)
        logger = start_logger()
        print("Server started")
        logger.info(f"Server started with {HOST}:{PORT}")
        while True:
            print("Waiting for connection...")
            conn, addr = serv_sock.accept()

            # handling client
            t = threading.Thread(target=handle_connection, args=(conn, addr))  # New
            t.start()