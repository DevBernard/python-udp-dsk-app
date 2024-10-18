import socket
from client_utils import *
import time











cli = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cli.settimeout(5)

loko = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
loko.settimeout(5)


print("fazendo cli 1")
sendOi(cli, 1, 'sexo')
resposta, addr = cli.recvfrom(STD_MSG_SIZE)
print(addr)
print(unpackMessage(resposta))


print('fazendo cli 2')
sendOi(loko, 2, 'PIPI')
resposta, addr = loko.recvfrom(STD_MSG_SIZE)
print(addr)
print(unpackMessage(resposta))



print("cli MANDANO")
msg = packMessage(
    MSG_MSG,
    1,
    0,
    10,
    'sexo',
    '1234567890'
)
sendMsg(cli, msg)

print("loko RECEBENDO")
msg, addr = loko.recvfrom(STD_MSG_SIZE)
print(unpackMessage(msg))
print(addr)



sendTchau(cli, 1, 'sexo')
sendTchau(loko, 2, 'PIPI')

time.sleep(3)
cli.close()
loko.close()
