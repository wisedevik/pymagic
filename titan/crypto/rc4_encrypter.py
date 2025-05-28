class RC4Encrypter:
    def __init__(self, base_key, nonce):
        self.key = [i for i in range(256)]
        self.x = 0
        self.y = 0

        self.init_state(base_key.encode() + nonce.encode())

    def init_state(self, key):
        j = 0
        for i in range(256):
            j = (j + self.key[i] + key[i % len(key)]) % 256
            self.key[i], self.key[j] = self.key[j], self.key[i]

        for i in range(len(key)):
            self.x = (self.x + 1) % 256
            self.y = (self.y + self.key[self.x]) % 256
            self.key[self.x], self.key[self.y] = self.key[self.y], self.key[self.x]

    def decrypt(self, input_bytes):
        return self.encrypt(input_bytes)

    def encrypt(self, input_bytes):
        output = bytearray()
        for byte in input_bytes:
            self.x = (self.x + 1) % 256
            self.y = (self.y + self.key[self.x]) % 256
            self.key[self.x], self.key[self.y] = self.key[self.y], self.key[self.x]
            output.append(byte ^ self.key[(self.key[self.x] + self.key[self.y]) % 256])
        return output
