import tkinter as tk
from tkinter import messagebox
from client.connection_pannel import ConnApp

class MainApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title('Aplicação Principal')

        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(side=tk.TOP)

        # Instancia a classe App
        self.app = ConnApp(self.top_frame)

        # Frame para componentes adicionais
        self.message_frame = tk.Frame(self.root)
        self.message_frame.pack(side=tk.TOP, pady=10)

        # Adiciona widgets ao frame adicional
        tk.Label(self.message_frame, text='Outro Componente Aqui').pack(pady=5)

        self.another_button = tk.Button(self.message_frame, text='Botão Adicional', command=self.message_action)
        self.another_button.pack(pady=5)

    def message_action(self):
        messagebox.showinfo('Ação Adicional', f'Você clicou no botão adicional! {self.app.ip}')


if __name__ == '__main__' :
    print('oi')
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()