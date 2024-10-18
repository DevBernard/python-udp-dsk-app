import tkinter as tk
from tkinter import simpledialog, messagebox
import re
import client_utils as cutils

class ConnApp:
    def __init__(self, root, client):
        self.root = root
        self.client = client
        #self.root.title('Configurações e Conexão')

        # Variáveis
        self.ip = cutils.HOST_IP
        self.port = cutils.PORT
        self.user_id = 0
        self.user_name = ''
        self.connected = False #importante: é passada pra MessagingApp para controle de envio e recebimento

        self.create_widgets()

    def create_widgets(self):
        # Frame que engloba tudo
        main_frame = tk.Frame(self.root)
        main_frame.pack()


        # Frame de Configurações
        config_frame = tk.Frame(main_frame)
        config_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.btn_config = tk.Button(config_frame, text='Configurações', command=self.open_config_window)
        self.btn_config.pack(pady=5)

        self.config_label = tk.Label(config_frame, text=f'Configurações:\nIP: {self.ip}\nPorta: {self.port}')
        self.config_label.pack()

        # Frame de Dados do Usuário
        user_frame = tk.Frame(main_frame)
        user_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.btn_user_data = tk.Button(user_frame, text='Dados do Usuário', command=self.open_user_data_window)
        self.btn_user_data.pack(pady=5)

        self.user_data_label = tk.Label(user_frame, text='Usuário:\nID: --\nNome: --')
        self.user_data_label.pack()

        # Frame Botão Conectar/Desconectar + Status da conexão
        connection_frame = tk.Frame(main_frame)
        connection_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.btn_connect = tk.Button(connection_frame, text='Conectar', command=self.toggle_connection, width=15, fg='white', bg='green')
        self.btn_connect.pack(pady=5)

        self.status_label = tk.Label(connection_frame, text='Status: Desconectado')
        self.status_label.pack(side=tk.TOP)

    def open_config_window(self):
        config_window = tk.Toplevel(self.root)
        config_window.title('Configurações')

        tk.Label(config_window, text='Informe o IP (xxx.xxx.xxx.xxx):').pack(pady=5)
        ip_entry = tk.Entry(config_window)
        ip_entry.pack(pady=5)

        tk.Label(config_window, text='Informe a Porta (0-65535):').pack(pady=5)
        port_entry = tk.Entry(config_window)
        port_entry.pack(pady=5)

        tk.Button(config_window, text='Salvar', command=lambda: self.save_config(ip_entry.get(), port_entry.get(), config_window)).pack(pady=10)

    def save_config(self, ip, port, config_window):
        try:
            self.port = int(port)
            if self.validate_config(ip, self.port):
                self.ip = ip
                self.config_label.config(text=f'Configurações:\nIP: {self.ip}\nPorta: {self.port}')
                config_window.destroy()
            else:
                messagebox.showerror('Erro', 'Configurações inválidas.')
        except ValueError:
            messagebox.showerror('Erro', 'Porta deve ser um número entre 0 e 65535.')

    def open_user_data_window(self):
        user_data_window = tk.Toplevel(self.root)
        user_data_window.title('Dados do usuário')

        tk.Label(user_data_window, text='Informe o ID (1-999):').pack(pady=5)
        user_id_entry = tk.Entry(user_data_window)
        user_id_entry.pack(pady=5)

        tk.Label(user_data_window, text='Informe o Nome (até 20 caracteres):').pack(pady=5)
        user_name_entry = tk.Entry(user_data_window)
        user_name_entry.pack(pady=5)

        tk.Button(user_data_window, text='Salvar', command=lambda: self.save_user_data(user_id_entry.get(), user_name_entry.get(), user_data_window)).pack(pady=10)

    def save_user_data(self, user_id, user_name, user_data_window):
        try:
            self.user_id = int(user_id)
            self.user_name = user_name

            if self.validate_user_data(self.user_id, self.user_name):
                self.user_data_label.config(text=f'Usuário:\nID: {self.user_id}\nNome: {self.user_name}')
                user_data_window.destroy()
            else:
                messagebox.showerror('Erro', 'Dados do usuário inválidos.')
        except ValueError:
            messagebox.showerror('Erro', 'ID deve ser um número entre 1 e 999.')

    #função importante, possui a maior parte da lógica
    def toggle_connection(self):
        if not self.connected:
            if self.validate_connection():
                response_oi = cutils.sendOi(self.client, self.user_id, self.user_name)
                if response_oi is True : #CONECTOU COM O SERVIDOR
                    self.connected = True
                    self.status_label.config(text='Status: Conectado')
                    self.btn_config.config(state=tk.DISABLED)
                    self.btn_user_data.config(state=tk.DISABLED)
                    self.btn_connect.config(text='Desconectar', bg='red')  # Muda para vermelho
                else:
                    messagebox.showerror('Erro',response_oi)

            else:
                messagebox.showerror('Erro', 'Preencha todos os campos antes de conectar.')
        else:
            response_xau = cutils.sendTchau(self.client, self.user_id, self.user_name)
            if response_xau is True:
                self.connected = False
                self.status_label.config(text='Status: Desconectado')
                self.btn_config.config(state=tk.NORMAL)
                self.btn_user_data.config(state=tk.NORMAL)
                self.btn_connect.config(text='Conectar', bg='green')  # Muda para verde
            else:
                    messagebox.showerror('Erro','Ocorreu um erro ao dar Tchau')


    def validate_config(self, ip, port):
        return ip and port is not None and self.is_valid_ip(ip) and 0 <= port <= 65535

    def validate_user_data(self, user_id, user_name):
        return user_id and user_name and 1 <= user_id <= 999 and len(user_name) <= 20

    def validate_connection(self):
        return self.validate_config(self.ip, self.port) and self.validate_user_data(self.user_id, self.user_name)

    def is_valid_ip(self, ip):
        pattern = r'^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
        return re.match(pattern, ip) is not None

if __name__ == '__main__':
    import socket
    cli = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #cli2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #cutils.sendOi(cli2,1,'1')
    root = tk.Tk()
    app = ConnApp(root,cli)
    root.mainloop()