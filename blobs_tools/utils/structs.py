from math import log2, ceil

# A collection of useful (to me at least) hand-made data structures and 
# representations.

class bitsarray():
    """A big endian array representation of bits.
    """
    
    def __init__(self, integer_value, pad_to=0, max_bits=None):
        """Takes an integer and returns its bitsarray representation.

        Args:
            integer_value (int): The integer value to be represented by the bitsarray
            pad_to (int, optional): If the length of the representation is 
            smaller than pad_to, pad the array with 0bits to the left 
            until the length is equal to pad_to. Defaults to 0.
            max_bits (int, optional): If the length of the representation is 
            greater than max_bits, truncate the array (from the left) so that
            its length is max_bits. 
            Defaults to None.
        """
        self.bits_list = []
        self._int_to_bits(integer_value)

        if len(self.bits_list) < pad_to:
            for _ in range(pad_to - len(self.bits_list)):
                self.bits_list.insert(0, 0)

        if max_bits and max_bits < len(self.bits_list):
            new_start = len(self.bits_list) - max_bits
            self.bits_list = self.bits_list[new_start:]


    def __str__(self) -> str:
        str_output = ''
        for bit in self.bits_list:
            str_output += str(bit)
        return str_output


    def __repr__(self) -> str:
        return f'{__name__}.bitsarray({self.bits_list})'


    def __len__(self) -> int:
        return len(self.bits_list)


    def index(self, value) -> int:
        """Returns the index of the first occurence of 'value' in the array. 
        Returns a ValueError if no occurence in the array.

        Args:
            value (int): The value (1 or 0) to look for

        Returns:
            int: Index of the first occurence of 'value'
        """
        return self.bits_list.index(value)
    
    
    def _int_to_bits(self, integer_value):
        """Helper funtion for the constructor that takes in an integer

        Args:
            integer_value (int): The integer value of the desired bitsarray
        """
        array_len = int(ceil(log2(integer_value)))
        
        self.bits_list = [0 for _ in range(array_len)]

        for bit_pos in range(array_len -1, -1, -1):
            if integer_value < 2**bit_pos:
                continue
            integer_value -= 2**bit_pos
            self.bits_list[array_len - bit_pos - 1] = 1


    def to_int(self) -> int:
        """Convert the bitsarray to an integer

        Returns:
            int: The integer value of the bitsarray representation.
        """
        int_repr = 0
        for bit_pos in range(len(self.bits_list)):
            int_repr += self.bits_list[bit_pos] * 2**(len(self.bits_list) - bit_pos - 1)
        return int_repr

    
    def pad_right(self, pad_to) -> int:
        """Adds 0bits to the right of the bits array up to the specified length.
        Ignores any padding lower than the original length.

        Args:
            pad_to (int): Total desired length once padded

        Returns:
            int: Number of bits added to the bits array.
        """
        appended = 0
        if pad_to > len(self.bits_list):
            for _ in range(pad_to - len(self.bits_list)):
                self.bits_list.append(0)
                appended += 1
        return appended


    def shift_left(self, shift=1):
        """Shifts all bits to the left. Bits do not loop around the array.

        Args:
            shift (int): Shift the array by 'shift' bits. Defaults to 1.
        """
        for _ in range(shift):
            self.bits_list = self.bits_list[1:]
            self.bits_list.append(0)


    def shift_right(self, shift=1):
        """Shifts all bits to the right. Bits do not loop around the array.

        Args:
            shift (int): Shift the array by 'shift' bits. Defaults to 1.
        """
        for _ in range(shift):
            self.bits_list = self.bits_list[:-1]
            self.bits_list.insert(0, 0)


if __name__ == '__main__':
    print("*********bitsarray tests*********")
    a = bitsarray(255, pad_to=7)
    b = bitsarray(12, pad_to=7)
    c = bitsarray(113)
    d = bitsarray(113, max_bits=5)
    print(a.to_int())
    print(f'test __str__: {a}')
    a.pad_right(13)
    print(f'test pad-right(13): {a}')
    print(b.to_int())
    print(f'test pad_to=7 {b}')
    print(c.to_int())
    print(f'default int=113: {c}')
    print(f'133 truncated to 5 bits: {d.to_int()}')
    print(f'same: {d}')