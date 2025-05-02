# Highlighted lines indicate changes from echo_server.py

import socket
import random

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 3003))
server_socket.listen()

print("Server is running on localhost:3003")

while True:
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr}")

    request = client_socket.recv(1024).decode()
    if not request or 'favicon.ico' in request:
        client_socket.close()
        continue
    
    request_line = request.splitlines()[0]
    print("Request Line: ", request_line) # GET /?rolls=2&sides=6 HTTP/1.1

    http_method, path, _ = request_line.split(" ")
    path, params = path.split("?")
    print("HTTP Method: ", http_method) # GET
    print("Path: ", path) # /
    print("Parameters: ", params) # rolls=2&sides=6
    params = params.split("&") # ["rolls=2", "sides=6"]
    print("Parameters: ", params)
    params = {param.split("=")[0]: param.split("=")[1] for param in params}
    print("Parameters: ", params)
    
    response_body = (
        f"Request Line: {request_line}\n"
        f"HTTP Method: {http_method}\n"
        f"Path: {path}\n"
        f"Parameters: {params}\n"
    )
    print("Response Body: ", response_body)
    # GET /?rolls=2&sides=6 HTTP/1.1
    # 5

    count = int(params["rolls"])
    print("Count: ", count)

    result = ""
    for _ in range(count):
        roll = random.randint(1, 6)
        result += f"Roll: {roll}\n"
    
    response_body += f"{result}"

    response = ("HTTP/1.1 200 OK\r\n"
                "Content-Type: text/plain\r\n"
                f"Content-Length: {len(response_body)}\r\n"
                "\r\n"
                f"{response_body}\n")

    client_socket.sendall(response.encode())
    client_socket.close()