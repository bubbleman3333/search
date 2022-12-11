from Crypto.PublicKey import RSA
from conf import config
from Crypto.Cipher import PKCS1_OAEP


def make_key(num):
    private_key = RSA.generate(num)
    with open(str(config.SECRET_PATH) + "/private.pem", "w") as f:
        tmp = private_key.exportKey().decode("utf-8")
        f.write(tmp)
    with open(str(config.SECRET_PATH) + "/receiver.pem", "w") as f:
        f.write(private_key.public_key().export_key().decode("utf-8"))


def read_public_key():
    with open(str(config.SECRET_PATH) + "/receiver.pem", "r") as f:
        return RSA.importKey(f.read())


def read_private_key():
    with open(str(config.SECRET_PATH) + "/private.pem", "r") as f:
        return RSA.importKey(f.read())


def crypto(s):
    cipher_rsa = PKCS1_OAEP.new(read_public_key())
    cipher_txt = cipher_rsa.encrypt(s.encode())
    with open(str(config.SECRET_PATH) + "/pass.txt", "wb") as f:
        f.write(cipher_txt)


def read_pass():
    with open(str(config.SECRET_PATH) + "/pass.txt", "r", encoding="utf-8") as f:
        return f.read()


def decrypto():
    with open(str(config.SECRET_PATH) + "/pass.txt", "rb") as f:
        origin = f.read()
    # print(RSA.generate(1234).exportKey())
    decipher_rsa = PKCS1_OAEP.new(read_private_key())
    # decipher_rsa = PKCS1_OAEP.new(RSA.generate(1234))
    print(decipher_rsa.decrypt(origin).decode("utf-8"))


decrypto()
