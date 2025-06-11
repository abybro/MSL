import socket

HOST = '192.168.0.10'  # IP de la caméra ou du robot
PORT = 8500            # Port de COMMANDE

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5)
        s.connect((HOST, PORT))
        print("Connexion établie")

        commande = "TRG\r"  # ou autre commande attendue, mais impérativement terminée par '\r'
        s.sendall(commande.encode('ascii'))
        print("Commande envoyée")

        response = s.recv(4096)
        print("Réponse :", response.decode(errors='ignore'))

except socket.timeout:
    print("Erreur : timeout lors de la réception")
except Exception as e:
    print("Erreur :", e)
