import socket
import threading


class Client:
    def __init__(self, server_ip='192.168.1.50', server_port=65432):
        self.server_ip = server_ip
        self.server_port = server_port
        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.cliente.connect((self.server_ip, self.server_port))
        send_thread = threading.Thread(target=self.send_messages)
        recv_thread = threading.Thread(target=self.receive_messages)
        send_thread.start()
        recv_thread.start()

    def send_messages(self):
        while True:
            mensaje = input("Ingrese el mensaje a enviar al servidor ('exit' para salir): ")
            if mensaje.lower() == 'exit':
                self.cliente.close()
                break
            self.cliente.sendall(mensaje.encode())

    def receive_messages(self):
        while True:
            data = self.cliente.recv(1024)
            if not data:
                print("Se ha perdido la conexión con el servidor.")
                break
            print('Respuesta del servidor:', data.decode())



