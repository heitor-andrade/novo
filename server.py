import socket
import threading
import pickle # para serializar objetos e poder mandá-los
# pickle métodos: pickle.dump(<msg>) e pickle.loads(<msg>)
# recv() e accept() são blocks code

HEADER = 10 # serve para descobrir o tamanho da mensagem, PODE SER PEQUENO
PORT = 5050
SERVER = 'DESKTOP-TC231IV'
ADDR = ('DESKTOP-TC231IV', PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

# AF_INET = tipo da conexão, ipv4, ipv6
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR) # permite conectar nesse computador

CONNECTIONS = 0


def handle_clients(conn1, addr1, conn2, addr2):
    print(f"[NEW CONNECTIONs] {addr1} e {addr2} connected")

    connected = True
    while connected:
        print("esperando client1")
        msg_length = conn1.recv(HEADER) # espera a mensagem do cliente
        print("recebi do client1")
        if msg_length:
            msg_length_int = int(msg_length)
            
            msg = conn1.recv(msg_length_int)
            
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr1}] \n {msg}")

            conn2.send(msg_length)
            conn2.send(msg)

        msg_length = conn2.recv(HEADER) # espera a mensagem do cliente
        print("recebi do client2")
        if msg_length:
            msg_length_int = int(msg_length)
            
            msg = conn2.recv(msg_length_int)
            
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr1}] \n {msg}")

            conn1.send(msg_length)
            conn1.send(msg)

    conn1.close
    conn2.close

def start(): # recebe e divide os clientes
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    
    while True:
        conn1, addr1 = server.accept() # espera a conexão e retorna o endereço(IP, PORT) e um objeto socket que permite mandar informações
        conn2, addr2 = server.accept() # espera a conexão e retorna o endereço(IP, PORT) e um objeto socket que permite mandar informações

        thread = threading.Thread(target = handle_clients, args = (conn1, addr1, conn2, addr2))
        thread.start()
        start_message = "comecou"
        
        start_message = pickle.dumps(start_message)
        
        conn1.send(bytes(f'{len(start_message):<{HEADER}}', FORMAT))
        conn1.send(start_message)

        conn2.send(bytes(f'{len(start_message):<{HEADER}}', FORMAT))
        conn2.send(start_message)
        print("começou")


print("[STARTING] server is starting")
start()