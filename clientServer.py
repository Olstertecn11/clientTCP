
import socket
import threading
import json
import time
import random


class Client:
    def __init__(self, server_ip='192.168.1.50', server_port=65432):
        self.server_ip = server_ip
        self.server_port = server_port
        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.last_message = ""
        self.in_collision = False  # Bandera para indicar si está en estado de colisión

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
            self.send_message(mensaje)

    def send_message(self, mensaje):
        timestamp = time.strftime("%H:%M:%S", time.localtime())  # Obtener tiempo actual
        message_data = {"time": timestamp, "message": mensaje}
        message_json = json.dumps(message_data)
        self.cliente.sendall(message_json.encode())
        self.last_message = message_json  # Guardar el último mensaje enviado

    def receive_messages(self):
        while True:
            data = self.cliente.recv(1024)
            if not data:
                print("Se ha perdido la conexión con el servidor.")
                break
            response = data.decode()
            if response == '{"code": "collision"}':
                if not self.in_collision:  # Evitar bucles infinitos de colisiones
                    print("Colisión detectada. Reenviando mensaje...")
                    self.in_collision = True  # Establecer la bandera de colisión
                    # Espera un número aleatorio de segundos menor a 10
                    wait_time = random.random() * 10
                    print(f"Mensaje será enviado dentro de {wait_time} segundos")
                    time.sleep(int(wait_time))
                    # Reenviar el último mensaje enviado con un nuevo tiempo
                    self.send_message_with_new_time()
                    self.in_collision = False  # Restablecer la bandera de colisión después del reenvío
            else:
                print('Respuesta del servidor:', response)

    def send_message_with_new_time(self):
        mensaje_data = json.loads(self.last_message)
        mensaje_data["time"] = time.strftime("%H:%M:%S", time.localtime())  # Actualizar el tiempo
        new_message_json = json.dumps(mensaje_data)
        self.cliente.sendall(new_message_json.encode())  # Enviar mensaje actualizado

