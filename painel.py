import tkinter as tk
from tkinter import messagebox
from connection_pannel import ConnApp
import socket

class MessagingApp:
    def __init__(self, root, connectionApp: ConnApp):
        self.root = root
        self.messages = []  # Lista de mensagens

        # Frame para mensagens
        self.message_frame = tk.Frame(root)
        self.message_frame.pack(pady=10)

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
        self.private_var = tk.BooleanVar()
        self.private_checkbox = tk.Checkbutton(
            self.private_frame,
            text="Privada",
            variable=self.private_var,
            command=self.toggle_destinatario_entry
        )
        self.private_checkbox.pack(anchor='w')  

        # Label e campo de destinatário
        self.destinatario_label = tk.Label(self.private_frame, text="Para (se privada):")
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

    def toggle_destinatario_entry(self):
        if self.private_var.get():
            self.destinatario_entry.config(state=tk.NORMAL)
        else:
            self.destinatario_entry.config(state=tk.DISABLED)
            self.destinatario_entry.delete(0, tk.END)  # Limpar o campo

    def send_message(self):
        print(connApp.connected)
        message = self.message_entry.get().strip()
        destinatario = self.destinatario_entry.get().strip()

        if not message:
            messagebox.showwarning("Aviso", "A mensagem não pode estar vazia.")
            return

        if self.private_var.get() and not destinatario:
            messagebox.showwarning("Aviso", "Preencha o destinatário para mensagens privadas.")
            return

        tag = "[pública]" if not self.private_var.get() else f"[para: {destinatario}]"
        complete_message = f"{tag} {message}"

        self.messages.append(complete_message)
        self.message_list.insert(tk.END, complete_message)

        #reseta mensagem
        self.message_entry.delete(0, tk.END)

        #joga a tela das mensagens pro final, caso o usuario tenha scrollado pra cima
        self.message_list.yview_scroll(self.message_list.winfo_height(), tk.UNITS)

#é um módulo, porém coloco este código para testar a unidade
if __name__ == "__main__":
    root = tk.Tk()
    cli = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    connApp = ConnApp(root, cli)
    app = MessagingApp(root, connApp)
    root.mainloop()
