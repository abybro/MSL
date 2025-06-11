import socket
import time

IP_CAM = "192.168.0.10"
PORT_CMD = 8500  # pour envoyer TRG
PORT_DATA = 8501  # pour recevoir les données (positions)

def send_trigger(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            s.connect((ip, port))
            s.sendall(b'TRG\r')  # KEYENCE attend '\r'
            print("[INFO] TRG envoyé.")
            response = s.recv(1024)
            print("[INFO] Réponse de la caméra :", response.decode(errors='ignore').strip())
    except Exception as e:
        print(f"[ERREUR] Envoi TRG : {e}")

def receive_data(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(3)
            s.connect((ip, port))
            print("[INFO] En attente des données...")
            data = s.recv(4096)
            decoded = data.decode('utf-8').strip()
            print(f"[INFO] Données reçues : {decoded}")
            return decoded
    except Exception as e:
        print(f"[ERREUR] Réception : {e}")
        return None

def extract_values(data):
    try:
        parts = data.split(',')
        score = float(parts[0])
        pos_x = float(parts[1])
        pos_y = float(parts[2])
        angle_rz = float(parts[3])
        return score, pos_x, pos_y, angle_rz
    except Exception as e:
        print(f"[ERREUR] Extraction : {e}")
        return None, None, None, None

def movejx(pos, sol):
    print(f"[ROBOT] Mouvement vers {pos} (solution {sol})")

# --- Exécution ---
send_trigger(IP_CAM, PORT_CMD)
time.sleep(1)  # petite pause pour laisser le temps à la caméra de traiter

data = receive_data(IP_CAM, PORT_DATA)
if data:
    score, pos_x, pos_y, angle_rz = extract_values(data)
    if score and score > 50:
        movejx([pos_x, pos_y, 40, 0, 180, angle_rz], sol=2)
    else:
        print("[INFO] Score insuffisant ou données invalides.")
else:
    print("[INFO] Aucune donnée reçue.")
