import base64
import hashlib
from Cryptodome import Random
from Cryptodome.Cipher import AES

from privnoteApp.settings import KEY_AES


class AESCipher(object):

    def init(self, key):
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode()))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        # print(enc.decode())
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]


key = KEY_AES

C = AESCipher(key)

d = C.encrypt("hello from cyber sky")
print(d)

f = C.decrypt(r"FuP2V4peiCi/3Ckj8lkAMZQ2Ru1Fozta1nkZL8Iu6KqbO6Za7amsUDDfO/kzRsVT")
print(f)
