import socket
import pickle


class Client:
    HEADER = 10 # serve para descobrir o tamanho da mensagem, PODE SER PEQUENO
    PORT = 5050
    FORMAT = 'utf-8'
    DISCONNECT_MESSAGE = "!DISCONNECT"
    SERVER = "189.5.176.14"
    ADDR = (SERVER, PORT)
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.ADDR)


    def send(self, msg):

        message = pickle.dumps(msg)
        
        send_length = len(message)

        send_length = bytes(f"{send_length:<{self.HEADER}}", self.FORMAT)

        self.client.send(send_length)
        self.client.send(message)

    def receive(self):

        msg_length = self.client.recv(self.HEADER) # espera a mensagem do cliente
        
        if msg_length:
            msg_length = int(msg_length)

            msg = self.client.recv(msg_length)
            
            print(msg)
            msg = pickle.loads(msg)

            if msg == self.DISCONNECT_MESSAGE:
                connected = False
            
            print(msg)
            return msg