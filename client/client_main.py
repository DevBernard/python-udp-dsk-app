import tkinter as tk
from connection_pannel import ConnApp
from messaging_pannel import MessagingApp
import socket


if __name__ == "__main__":
    #definindo socket
    cli = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    cli.settimeout(.5)

    #definindo painel
    root = tk.Tk()
    root.wm_title('TWITTER AVANÇADISSIMO')
    connApp = ConnApp(root, cli)
    app = MessagingApp(root, connApp, cli)
    root.mainloop()

    #finaliza
    cli.close()