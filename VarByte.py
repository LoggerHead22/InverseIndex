

class VarByte:

    def __init__(self):
        self.flag_byte = int('10000000', 2)

    def encodeNumber(self, n):
        """
        Кодируем число
        """
        n_bytes = (self.flag_byte | (n & 127)).to_bytes(1, byteorder='big', signed=False)

        n = n >> 7

        while n  > 0:
            n_bytes = (n & 127).to_bytes(1, byteorder='big', signed=False) + n_bytes

            n = n >> 7
        return n_bytes


    def encode(self, array):
        """
        Кодируем массив чисел
        """
        result = bytearray()
        for num in array:
            result += self.encodeNumber(num)
        return result


    def decode(self, bytes_arr):
        """
        Декодируем последвательность байт
        Функция - генератор целых чисел
        """

        n_bytes = 0
        for byte in bytes_arr:
            i = int(byte)

            n_bytes  = n_bytes << 7

            if i & self.flag_byte == 128:
                n_bytes |= i & 127
                yield n_bytes
                n_bytes = 0
            else:
                n_bytes |= i


