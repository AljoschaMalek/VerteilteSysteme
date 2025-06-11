import socket  # Modul für Netzwerkverbindungen
import time    # Modul zur Zeitmessung (z.B. für RTT)

# Konfiguration des Servers (Docker-Container-Name!)
HOST = 'server'  # Standard: Name des Server-Containers in Docker
PORT = 8080      # Zielport, auf dem der Server lauscht
data = "temperature=22.5"  # Daten, die im POST-Request gesendet werden

# Funktion, um einen POST-Request zu senden
# Optional: man kann einen anderen Host oder Port übergeben (z.B. localhost beim lokalen Test)
def send_post(host=HOST, port=PORT):
    # Erstellen der HTTP-POST-Anfrage
    request = f"POST / HTTP/1.1\r\nHost: {host}\r\nContent-Length: {len(data)}\r\n\r\n{data}"

    # Starten des Timers für die RTT
    start = time.time()

    # Verbindungsversuche mit Retry
    for attempt in range(5):    # maximal 5 Verbindungsversuche
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  # Öffnet TCP/IP-Verbindung (IPv4, TCP)
                s.connect((host, port))  # Verbindung zum Server wird hergestellt
                s.sendall(request.encode())  # HTTP-POST-Anfrage senden
                response = s.recv(1024)  # Antwort vom Server empfangen (max. 1024 Bytes)
                break  # Schleife beenden, wenn es geklappt hat
        except ConnectionRefusedError:
            print(f"Verbindung fehlgeschlagen (Versuch {attempt + 1}/5). Warte 2 Sekunden...")  # Fehlermeldung und neuer Versuch
            time.sleep(2)  # 2 Sekunden warten vor neuem Verbindungsversuch
    else:
        print("Verbindung zum Server endgültig fehlgeschlagen.")  # Fehlermeldung, wenn alle Versuche fehlschlagen
        return

    end = time.time()  # Timer stoppen, um RTT zu messen

    # Ausgabe der Serverantwort und RTT
    print("Antwort:", response.decode())  # Antwort des Servers ausgeben
    print("RTT: {:.5f} Sekunden".format(end - start))  # RTT mit 5 Nachkommastellen ausgeben

# Nur ausführen, wenn direkt aufgerufen (nicht beim Importieren)
if __name__ == "__main__":
    send_post()
