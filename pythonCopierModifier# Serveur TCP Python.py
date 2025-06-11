pythonCopierModifier# Serveur TCP Python (à exécuter sur le PC) import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 9000))
server.listen(1)
print("En attente d'une connexion...")
conn, addr = server.accept()print(f"Connecté à {addr}")
while True:
    data = conn.recv(1024)
    if not data:
        breakprint(f"Reçu : {data}")
conn.close()