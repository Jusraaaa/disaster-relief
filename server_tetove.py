import socket

requests_list = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 5002  # Porta për Tetovë

server_socket.bind((host, port))
server_socket.listen()

print(f"[Tetovë] Serveri është duke pritur në {host}:{port}...")

while True:
    conn, addr = server_socket.accept()
    print(f"[Tetovë] Lidhje e pranuar nga: {addr}")

    data = conn.recv(1024).decode('utf-8')
    if not data:
        break

    print(f"[Tetovë] Kërkesë e re: {data}")
    requests_list.append(data)

    conn.send("Kërkesa u pranua nga Tetova ✅".encode('utf-8'))
    conn.close()
