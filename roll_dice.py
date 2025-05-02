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

    if (not request) or ('favicon.ico' in request):
        client_socket.close()
        continue

    request_line = request.splitlines()[0]
    print(f"Request Line: {request_line}")

    roll = random.randint(1, 6)
    response_body = f"{request_line}\n{roll}"
    # http_method = request_line.split(' ')[0]
    # print("http_method: ", http_method)
    # http_version = request_line.split(' ')[2]
    # print("http_version: ", http_version)

    response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/plain\r\n"
        f"Content-Length: {len(response_body)}\r\n"
        "\r\n"
        f"Request Line: {request_line}\r\n"
        # f"{response_body}\n"
        # f"HTTP Method: {http_method}\r\n"
    )
    print(f"Server response: {response}")
    
    client_socket.sendall(response.encode())
    client_socket.close()
