import socket
import random

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(('127.0.0.1', 3003))
server_socket.listen()

print("Server is running on 127.0.0.1:3003")

while True:
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr}")
    request = client_socket.recv(1024).decode()

    if (not request) or ('favicon.ico' in request):
        client_socket.close()
        continue

    request_line = request.splitlines()[0]
    print(f"request_line: {request_line}")
    http_method = request_line.split()[0]
    print(f"http_method: {http_method}")
    path = request_line.split()[1].split("?")[0]
    print(f"path: {path}")
    rolls = request_line.split()[1].split("?")[1].split("&")[0].split("=")
    rolls = rolls[1]
    print(f"rolls: {rolls}")
    sides = request_line.split()[1].split("?")[1].split("&")[1].split("=")
    sides = sides[1]
    print(f"sides: {sides}")
    params = {}
    params['rolls'] = rolls
    params['sides'] = sides
    print(f"params: {params}")

    def roll_dice(num):
        result = []
        for _ in range(num):
            roll = random.randint(1, int(sides))
            result.append(roll)
        
        return result
    
    dice_rolls = roll_dice(int(rolls))
    
    response_body = f"<html>Request Line: {request_line}\nHTTP Method: {http_method}\nPath: {path}\nParameters: {params}\n{"\n".join([f"Roll: {roll}" for roll in dice_rolls])}\n</html>"
    
    print(f"response_body: {response_body}")

    response = ("HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html\r\n"
                f"Content-Length: {len(response_body)}\r\n"
                "\r\n"
                f"{response_body}\n")
    client_socket.sendall(response.encode())
    client_socket.close()