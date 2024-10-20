from socket import htonl, ntohl
from struct import pack, unpack
from datetime import datetime

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
HOST_IP = '0.0.0.0'#socket.gethostbyname(socket.gethostname())
PORT = 12345
ADDR = (HOST_IP, PORT)

#para o log
def log(tag: str, msg:str):
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    tag = tag.ljust(13)
    msg = f'{time} | {tag}{msg}'
    print(msg)


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
    texto = msg[37:].rstrip(b'\x00').decode(fmt)
    return tipo, remetente, destinatario, tamTexto, nome, texto

def sendOi(server, dest, addr, msg):
    msg = packMessage(
        tipo=MSG_OI,
        remetente=SERVER_ID,
        destinatario=dest,
        tamTexto=len(msg),
        nome=SERVER_NAME,
        texto=msg
    )
    server.sendto(msg, addr)

def sendTchau(server, dest, addr): #nao precisa retornar mensagem, mas se precisar, só tirar o return
    msg = packMessage(
        tipo=MSG_TCHAU,
        remetente=SERVER_ID,
        destinatario=dest,
        tamTexto=0,
        nome=SERVER_NAME,
        texto='xau'
    )
    server.sendto(msg, addr)

def sendMsg(server, msg, addr):
    server.sendto(msg, addr)

def make_standard_message(dest):
    texto = f'Oi, sou o {SERVER_NAME}, meu id eh {SERVER_ID}'
    send_msg =  packMessage(
        tipo=MSG_MSG,
        remetente=SERVER_ID,
        destinatario=dest,
        tamTexto=len(texto),
        nome=SERVER_NAME,
        texto=texto
    )
    return send_msg