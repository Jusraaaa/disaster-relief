import socket

# Ruaj listën e kërkesave
requests_list = []

# Krijo socket server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'  # IP lokale
port = 5001         # Port për Shkup

server_socket.bind((host, port))
server_socket.listen()

print(f"[Shkup] Serveri është duke pritur në {host}:{port}...")

while True:
    conn, addr = server_socket.accept()
    print(f"[Shkup] Lidhje e pranuar nga: {addr}")

    data = conn.recv(1024).decode('utf-8')
    if not data:
        break

    print(f"[Shkup] Kërkesë e re: {data}")
    requests_list.append(data)

    conn.send("Kërkesa u pranua nga Shkupi ✅".encode('utf-8'))
    conn.close()
