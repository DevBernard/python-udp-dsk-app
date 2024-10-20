import tkinter as tk
from connection_pannel import ConnApp
from messaging_pannel import MessagingApp
import socket

def close(app: MessagingApp):
    print('closing app')
    if app.connApp.connected:
        app.connApp.toggle_connection()
    app.root.destroy()
    

if __name__ == "__main__":
    #definindo socket
    cli = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    cli.settimeout(.5)

    #definindo painel
    root = tk.Tk()
    root.wm_title('TWITTER AVANÇADISSIMO')
    connApp = ConnApp(root, cli)
    app = MessagingApp(root, connApp, cli)
    root.wm_protocol('WM_DELETE_WINDOW', lambda: close(app))
    root.mainloop()

    #finaliza
    cli.close()