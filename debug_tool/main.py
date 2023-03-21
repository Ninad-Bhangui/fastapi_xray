import datetime
import json
import multiprocessing
import socket
import os
import sqlite3
import uuid
from multiprocessing import Process
from typing import Dict

from cli_app.ui import render_ui

HOST = '0.0.0.0'  # The server's hostname or IP address
PORT = 8989  # The port used by the server

request_data = []


def start_server(sharedQueue):
    # Create a socket object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print(f"Started debug server on {HOST}:{PORT}")
        # Bind the socket to a specific address and port
        s.bind((HOST, PORT))

        while True:
            try:
                # Listen for incoming connections
                s.listen()

                # Wait for a client to connect
                conn, addr = s.accept()
                with conn:
                    # Receive data from the client
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        # Process the data received from the client

                        sharedQueue.put(data.decode('utf-8'))

            except Exception as e:
                print("An error occurred:", e)
                # Restart the program if it crashes
                os.execv(__file__, os.sys.argv)


if __name__ == '__main__':
    data = [
        {
            "request_id": str(uuid.uuid4()),
            "time": 0.123,
            "url": "https://www.google.com",
            "method": "GET",
            "headers": {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br",
                "Host": "www.google.com",
            },
            "body": "",
            "cookies": {
                "JSESSIONID": "",
            },
            "user_agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
            "referer": "https://www.google.com/",
            "host": "www.google.com",
            "ip": "127.0.0.1",
            "path": "/todo",
            "protocol": "https",
            "query_string": {
                "q": "",
                "oq": "",
            },
            "body_params": {
                "q": "",
                "oq": "",
            },

        },
        {
            "request_id": str(uuid.uuid4()),
            "time": 0.123,
            "url": "https://www.google.com",
            "method": "POST",
            "headers": {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br",
                "Host": "www.google.com",
            },
            "body": "",
            "cookies": {
                "JSESSIONID": "",
            },
            "user_agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
            "referer": "https://www.google.com/",
            "host": "www.google.com",
            "ip": "127.0.0.1",
            "path": "/todo",
            "protocol": "https",
            "query_string": {
                "q": "",
                "oq": "",
            },
            "body_params": {
                "q": "",
                "oq": "",
            },

        }
    ]

    sharedQueue = multiprocessing.Queue()

    p1 = Process(target=start_server, args=(sharedQueue,))  # process p1
    p1.daemon = True
    p1.start()

    p2 = Process(target=render_ui, args=(sharedQueue,))  # process p2
    p2.start()

    p1.join()
    p2.join()

    start_server(sharedQueue)
    render_ui(sharedQueue)
