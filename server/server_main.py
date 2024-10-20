import socket
import threading
from typing import List
from server_utils import *
import time

#INICIANDO SOCKET DO SERVIDOR
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(ADDR)
server.settimeout(3) #segundos

#LISTA DE CONTROLE DE CLIENTES ATIVOS:
#{<id>:(<ip>,<porta>)}
active_clients = {}

def thread_sender_loop():
    while True:
        time.sleep(60) #temporização de 1 minuto
        for client, addr in active_clients.items():
            msg = make_standard_message(client) #monta mensagem de identificaçao
            sendMsg(server,msg,addr)

def return_error(msg, remetente, addr):
    """ monta uma mensagem com o erro especificado no argumento msg"""

    send_msg = packMessage(
        tipo= MSG_TCHAU,
        remetente= SERVER_ID,
        destinatario= remetente,
        tamTexto= len(msg),
        nome= SERVER_NAME,
        texto=msg
    )
    server.sendto(send_msg, addr)

def validate_msg(raw_msg,addr):
    """ utilizada para validar se a mensagem veio com os argumentos corretos e faz sentido"""

    tipo, remetente, destinatario, tamTexto, nome, texto = unpackMessage(raw_msg)
    is_active = remetente in active_clients

    if tipo not in range(4):
        return "Tipo de mensagem inválido"
    if is_active:
        if tipo == MSG_OI:
            if addr == active_clients[remetente]:
                return "Cliente já conectado"
            else:
                return "Já existe um cliente com este código"
        if destinatario and destinatario not in active_clients:
            return "Destinatário não encontrado"
    else:
        if tipo != MSG_OI:
            return "Uma conexão deve ser estabelecida (OI)"
        if len(active_clients) == 15:
            return "Quantidade maxima de clientes atingida"
        if remetente < 1 or remetente > 999:
            return "Numero de remetente inválido"


def handle_recv(raw_msg, addr):
    """ função principal do sistema, utilizado para tratar todas as mensagens recebidas, é utilizada de modo concorrente"""

    tipo, remetente, destinatario, tamTexto, nome, texto = unpackMessage(raw_msg)
    err = validate_msg(raw_msg, addr)

    if err: 
        return_error(err, remetente, addr)
        return
    
    if tipo == MSG_OI:
        log('[ADDING]',f'adicionando usuario {remetente}')
        active_clients[remetente] = addr
        sendOi(server, remetente, addr, texto)
    elif tipo == MSG_MSG:
        if destinatario == SERVER_ID:
            for cli_addr in active_clients.values():
                if cli_addr != addr:
                    sendMsg(server,raw_msg,cli_addr)
        else:
            dest_addr = active_clients[destinatario]
            sendMsg(server, raw_msg, dest_addr)
    elif tipo == MSG_TCHAU:
        log('[REMOVING]', f'removendo usuario {remetente}')
        active_clients.pop(remetente)
        sendTchau(server, remetente, addr)

def endServer(threads: List[threading.Thread]):
    """função para finalizar o sistema"""

    for thread in threads:
        thread.join()
    for cli, addr in active_clients.items():
        sendTchau(server, cli, addr)
    log('[ENDING]', "finalizando server")
    server.close()

def startServer():
    threads = []
    log('[STARTING]', 'iniciando server')

    #inicia um loop secundário, para o envio periódico de mensagens
    envio_periodico = threading.Thread(target=thread_sender_loop, daemon=True)
    envio_periodico.start()
    
    try:
        #loop principal, lê mensagens infinitamente e cria uma thread pra lidar com as respostas
        while True: 
            try:
                raw_msg, addr = server.recvfrom(STD_MSG_SIZE)
                if raw_msg:
                    thread = threading.Thread(target=handle_recv, args=(raw_msg, addr))
                    thread.start()
                    threads.append(thread)
                    #handle_recv(raw_msg, addr)
            except socket.timeout: pass
    except KeyboardInterrupt:
            log('[WARNING]','finalização forçada capturada')

    endServer(threads)

    
startServer()