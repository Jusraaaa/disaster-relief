import socket

# Përcakto portet për çdo qytet
ports = {
    "shkup": 5001,
    "tetove": 5002,
    "gostivar": 5003
}

# Zgjedh qytetin
city = input("Zgjedh qytetin [shkup / tetove / gostivar]: ").strip().lower()

if city not in ports:
    print("Qyteti i zgjedhur nuk është valid!")
    exit()

host = '127.0.0.1'
port = ports[city]

# Lidhja me serverin përkatës
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((host, port))

    message = input("Shkruaj kërkesën për ndihmë: ")
    client_socket.send(message.encode('utf-8'))

    response = client_socket.recv(1024).decode('utf-8')
    print(f"[Serveri] {response}")

except ConnectionRefusedError:
    print("Nuk u lidh me serverin. A është serveri i qytetit duke punuar?")
finally:
    client_socket.close()
