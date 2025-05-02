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
        "<!DOCTYPE html>\n"
        "<html lang=\"en\">\n"
        "<head>\n"
        "<meta charset=\"utf-8\">\n"
        "<title>HTML Response</title>\n"
        "<style>\n"
        "html {\n"
        "   margin: 0;\n"
        "   padding: 0;\n"
        "}\n"
        "body {\n"
        "   margin-left: 20px;"
        "   color: green;"
        "}\n"
        ".roll {\n"
        "   padding: 5px;\n"
        "   border: solid 1px black;\n"
        "   display: block;\n"
        "   width: 25%\n"
        "}\n"
        "h2, h4 {\n"
        "   display: inline-block;\n"
        "}\n"
        # "div {\n"
        # "   display:block;\n"
        # "}\n"
        "</style>"
        "</head>\n"
        "<body>\n"
        "<div>\n"
        f"<h2>Request Line: <h4>{request_line}</h4></h2>\n"
        "</div>\n"
        "<div>\n"
        f"<h2>HTTP Method: <h4>{http_method}</h4></h2>\n"
        "</div>\n"
        "<div>\n"
        f"<h2>Path: <h4>{path}</h4></h2>\n"
        "</div>\n"
        f"<h2>Parameters: <h4>{params}</h4></h2>\n"
    )
    print("Response Body: ", response_body)
    # GET /?rolls=2&sides=6 HTTP/1.1
    # 5

    rolls = int(params.get("rolls", "1"))
    print("Rolls: ", rolls)

    sides = int(params.get("sides", "6"))
    print("Sides: ", sides)

    for _ in range(rolls):
        roll = random.randint(1, sides)
        response_body += f"<h2 class=\"roll\">Roll: {roll}</h2>\n"
    
    response_body += f"</body>\n</html>\n"
    
    response = ("HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html\r\n"
                f"Content-Length: {len(response_body)}\r\n"
                "\r\n"
                f"{response_body}\n")

    client_socket.sendall(response.encode())
    client_socket.close()
