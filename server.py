import socket
import time
import threading
from queue import Queue

class OTPServer:
    def __init__(self, shared_seed):
        self.shared_seed = shared_seed
        self.last_valid_token = None
        self.timeout_flag = False
        self.attempts = 0

    def run(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost', 8080))
        server_socket.listen(1)

        print("En attente de connexion...")
        client_socket, address = server_socket.accept()
        print(f"Connexion établie avec {address}")

        attempts = 0
        start_time = time.time()
        last_block_start_time = start_time

        while attempts < 5:
            expected_token = client_socket.recv(1024).decode()
            print(f"Nouveau jeton reçu : {expected_token}")

            timeout_queue = Queue()
            threading.Thread(target=self.input_timeout, args=(timeout_queue,)).start()
            threading.Thread(target=self.get_user_input, args=(timeout_queue,)).start()

            user_input = self.wait_for_user_input(timeout_queue)
            elapsed_time = time.time() - start_time

            if self.timeout_flag or elapsed_time >= 10:
                if elapsed_time >= 60:
                    print(f"Dernier jeton valide du bloc précédent : {self.last_valid_token}")
                    last_block_start_time = time.time()
                print("Accès refusé (temps écoulé)!")
            elif self.validate_token(expected_token, user_input):
                print("Accès confirmé !")
                self.last_valid_token = expected_token
                attempts = 0  # Réinitialiser le compteur d'essais après une validation réussie
            else:
                print("Accès refusé !")
                attempts += 1

            if attempts == 5:
                print("Limite de tentatives atteinte. Fermeture de la connexion.")
            else:
                time.sleep(1)  # Attente avant de générer un nouveau jeton

            # Mise à jour du seed à chaque itération pour rester synchronisé avec le client
            self.shared_seed += 1

        print("Fermeture de la connexion.")
        client_socket.close()
        server_socket.close()

    def input_timeout(self, queue):
        time.sleep(10)
        self.timeout_flag = True

    def get_user_input(self, queue):
        user_input = input("Veuillez saisir le jeton : ")
        queue.put(user_input)

    def wait_for_user_input(self, queue):
        user_input = None
        while user_input is None and not self.timeout_flag:
            try:
                user_input = queue.get(block=False)
            except:
                pass
        return user_input

    def validate_token(self, expected_token, user_input):
        return all(expected_token.count(digit) == user_input.count(digit) for digit in expected_token)

if __name__ == "__main__":
    shared_seed = 12345
    server = OTPServer(shared_seed)
    server.run()
