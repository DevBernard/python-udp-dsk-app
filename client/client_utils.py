from socket import htonl, ntohl
from struct import pack, unpack

#protocolos: tipo de mensagem
MSG_OI    = 0
MSG_TCHAU = 1
MSG_MSG   = 2
MSG_ERRO  = 3

#info do servidor
SERVER_ID = 0
SERVER_NAME = "SERVIDOR"

#constantes globais
FORMAT = 'utf-8'
STD_MSG_SIZE = 178 #visto a partir de testes, 4 * 4 bytes pros inteiros  + 21 + 141
HOST_IP = '127.0.0.1'
PORT = 12345
ADDR = (HOST_IP, PORT)

#transforma os campos em uma mensagem enviavel pelo socket
def packMessage(tipo: int, remetente: int, destinatario: int, tamTexto: int, nome: str, texto: str, fmt = 'utf-8'):
    new_tipo = htonl(tipo)
    new_remetente = htonl(remetente)
    new_destinatario = htonl(destinatario)
    new_tamTexto = htonl(tamTexto)
    new_nome = nome.ljust(20).encode(fmt) + b'\x00'
    new_texto = texto.encode(fmt) + b'\x00'
    send_msg = pack('!IIII', new_tipo, new_remetente, new_destinatario, new_tamTexto) + new_nome + new_texto
    return send_msg

#traduz a mensagem recebida nos seus devidos campos
def unpackMessage(msg: str, fmt: str = 'utf-8'):
    vals = unpack('!IIII', msg[:16])
    tipo, remetente, destinatario, tamTexto = [ntohl(val) for val in vals]
    nome = msg[16:37].rstrip(b'\x00').rstrip().decode(fmt) #21
    texto = msg[37:].rstrip(b'\x00').rstrip().decode(fmt)
    return tipo, remetente, destinatario, tamTexto, nome, texto

def sendOi(client, my_id, my_name):
    msg = packMessage(
        tipo=MSG_OI,
        remetente=my_id,
        destinatario=SERVER_ID,
        tamTexto=0,
        nome=my_name,
        texto='oi'
    )
    client.sendto(msg, ADDR)

    res_msg, _ = client.recvfrom(STD_MSG_SIZE)
    texto = unpackMessage(res_msg)[-1]
    if texto == 'oi':
        return True
    return texto

def sendTchau(client, my_id, my_name):
    msg = packMessage(
        tipo=MSG_TCHAU,
        remetente=my_id,
        destinatario=SERVER_ID,
        tamTexto=0,
        nome=my_name,
        texto='xau'
    )
    client.sendto(msg, ADDR)

    return True
    res_msg, _ = client.recvfrom(STD_MSG_SIZE) #NÃO DIZ NO TRABALHO QUE RECEBE UMA CONFIRMAÇÃO DO TCHAU (pelo q vi)
    texto = unpackMessage(res_msg)[-1]
    if texto == 'xau':
        return True
    return texto

def sendMsg(client, msg):
    client.sendto(msg, ADDR)
