import tkinter as tk
from tkinter import messagebox
from typing import TYPE_CHECKING
import client_utils as cutils
import threading
from socket import timeout as socket_timeout

#importa apenas para mostrar os tipos das classes pra ajudar no desenvolvimento
if TYPE_CHECKING:
    from socket import socket
    from connection_pannel import ConnApp
    from tkinter import Tk

class MessagingApp:
    def __init__(self, root: 'Tk', connection_app: 'ConnApp', client_socket: 'socket'):
        self.root = root
        self.connApp = connection_app
        self.client = client_socket
        self.messages = []  # Lista de mensagens
        self.message_recv_thread = threading.Thread(target=self.message_receiver, daemon=True) 

        self.buildWidgets(root)

        self.message_recv_thread.start()

    # def fecha_thread(self): não precisa disso com daemon=True
    #     if self.connApp.connected:
    #         self.connApp.toggle_connection()
    #     self.message_recv_thread.join()

    def message_receiver(self):
        while True:
            try:
                msg, _ = self.client.recvfrom(cutils.STD_MSG_SIZE)
            except socket_timeout:
                continue 
            if msg:
                tipo, _, _, _, r_nome, texto = cutils.unpackMessage(msg)
                if tipo == cutils.MSG_ERRO:
                    texto = f'ERRO: {texto}'
                formatted_message = f'[De: {r_nome}]: {texto}'
                self.root.after(0, self.update_msgs, formatted_message)

    def update_msgs(self, msg):
        self.messages.append(msg)
        self.message_list.insert(tk.END, msg)

    def send_message(self):
        warnings = []
        message = self.message_entry.get()

        if self.is_private.get():
            try:
                destinatario = int(self.destinatario_entry.get())
            except ValueError:
                warnings.append("O destinatario deve ser um inteiro")
                destinatario = -1
            if not (1 <= destinatario <= 999):
                warnings.append("O destinatario deve estar entre 1 e 999")
        else:
            destinatario = cutils.SERVER_ID #broadcasta pra todos

        if not self.connApp.connected:
            warnings.append("Você não está Conectado")
        if not message:
            warnings.append("A mensagem não pode estar vazia.")
        if len(message) > 140:
            warnings.append("A mensagem deve ter ate 140 caractereres")
        if self.is_private.get() and not destinatario:
            warnings.append("Preencha o destinatário para mensagens privadas.")

        if warnings:
            messagebox.showwarning("Aviso(s)", "\n\n".join(warnings))
            return

        tag = "[pública]" if not self.is_private.get() else f"[para: {destinatario}]"
        viewer_message = f"{tag} {message}"

        #envia mensagens com SOCKET
        packed_message = cutils.packMessage(
            tipo= cutils.MSG_MSG,
            remetente= self.connApp.user_id,
            destinatario= destinatario,
            tamTexto= len(message),
            nome= self.connApp.user_name,
            texto= message
        )
        cutils.sendMsg(self.client, packed_message)

        #insere mensagem na exibição / view e no controle interno
        self.update_msgs(viewer_message)

        #reseta mensagem
        self.message_entry.delete(0, tk.END)

        #joga a tela das mensagens pro final, caso o usuario tenha scrollado pra cima
        self.message_list.yview_scroll(self.message_list.winfo_height(), tk.UNITS)

    def toggle_destinatario_entry(self):
        if self.is_private.get():
            self.destinatario_entry.config(state=tk.NORMAL)
        else:
            self.destinatario_entry.config(state=tk.DISABLED)
            self.destinatario_entry.delete(0, tk.END)  # Limpar o campo

    def buildWidgets(self, root):
        # Frame para mensagens
        self.message_frame = tk.Frame(root)
        self.message_frame.pack(pady=10, side=tk.TOP)

        # Lista de mensagens
        self.message_list = tk.Listbox(self.message_frame, width=50, height=10)
        self.message_list.pack(side=tk.TOP)

        # Frame principal para entrada de mensagem
        self.input_frame = tk.Frame(root)
        self.input_frame.pack(pady=10)

        # Frame para destinatário e checkbox
        self.private_frame = tk.Frame(self.input_frame)
        self.private_frame.pack(side=tk.LEFT, padx=10)

        # Checkbox para mensagem privada
        self.is_private = tk.BooleanVar()
        self.private_checkbox = tk.Checkbutton(
            self.private_frame,
            text="Privada",
            variable=self.is_private,
            command=self.toggle_destinatario_entry
        )
        self.private_checkbox.pack(anchor='w')  

        # Label e campo de destinatário
        self.destinatario_label = tk.Label(self.private_frame, text="ID Dest.:")
        self.destinatario_label.pack(anchor='w')  

        self.destinatario_entry = tk.Entry(self.private_frame, width=10, state=tk.DISABLED)
        self.destinatario_entry.pack(anchor='w')  

        # Frame para mensagem
        self.message_input_frame = tk.Frame(self.input_frame)
        self.message_input_frame.pack(side=tk.LEFT)

        # Label e campo de mensagem
        self.message_label = tk.Label(self.message_input_frame, text="Mensagem:")
        self.message_label.pack(anchor='w')  

        self.message_entry = tk.Entry(self.message_input_frame, width=40)
        self.message_entry.pack(anchor='w')  

        # Botão de enviar
        self.send_button = tk.Button(
            self.message_input_frame,
            text="Enviar",
            command=self.send_message
        )
        self.send_button.pack(anchor='w')  
