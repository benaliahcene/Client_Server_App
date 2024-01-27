from client import OTPClient
from server import OTPServer

if __name__ == "__main__":
    client = OTPClient(seed=12345)  # Remplacez par la valeur appropriée
    server = OTPServer()

    # Exécutez le client et le serveur dans des threads ou des processus séparés
    # selon votre préférence et les besoins de votre application.
