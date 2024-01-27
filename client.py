import socket
import time
import random

class OTPClient:
    def __init__(self, seed):
        self.seed = seed

    def generate_otp(self):
        random.seed(self.seed)
        return ''.join(str(random.randint(0, 9)) for _ in range(8))

    def run(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 8080))

        while True:
            token = self.generate_otp()
            print(f"Token généré côté client : {token}")

            # Envoyer le jeton au serveur
            client_socket.sendall(token.encode())

            time.sleep(10)
            self.seed += 1

if __name__ == "__main__":
    shared_seed = 12345
    client = OTPClient(shared_seed)
    client.run()