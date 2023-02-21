from math import log2, ceil

# A collection of useful (to me at least) hand-made data structures and 
# representations.

class bitsarray():
    """A big endian bits array representation.
    """
    
    def __init__(self, integer_value, pad_to=0, bytes_align=False, max_bits=None):
        """Takes an integer and returns its bitsarray representation.

        Args:
            integer_value (int): The integer value to be represented by the bitsarray
            pad_to (int, optional): If the length of the representation is 
            smaller than pad_to, pad the array with 0bits to the left 
            until the length is equal to pad_to. Defaults to 0.
            bytes_align(bool, optional): Make the bits representation a length which
            is a multiple of 8. Will override pad_to. Defaults to False.
            max_bits (int, optional): If the length of the representation is 
            greater than max_bits, truncate the array (from the left) so that
            its length is max_bits. 
            Defaults to None.
        """
        
        # Does not support negative values so far
        if integer_value < 0:
            raise ValueError('Bitsarray does not support negative integet values so far')
        
        self.bits_list = []
        self._int_to_bits(integer_value)

        # If we align to bytes, 
        if bytes_align:
            # Get the number of bits
            bits_num = len(self)
            bytes_num = ceil(bits_num / 8)
            # Major it to the closest multiple of 8 higher than that number of bits
            pad_to = bytes_num * 8
            

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
        str_output += ' : ' + str(self.to_int())
        return str_output


    def __repr__(self) -> str:
        return f'{__name__}.bitsarray({self.bits_list})'


    def __len__(self) -> int:
        return len(self.bits_list)

    def __getitem__(self, index):
        return self.bits_list[index]


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
        array_len = int(ceil(log2(integer_value + 1)))
        
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


    def add(self, right_operand, output_size=0, bytes_align=False):
        """Addition between a bitsarray and an integer value.

        Args:
            right_operand (int): Value to add.
            output_size (int, optional): The desired size of the resulting bitsarray. If the specified 
            size is smaller than the result of the addition, the result will be truncated. If 0, 
            pads to the current length of the bits array.
            bytes_align (bool, optional): Pad to the nearest multiple of 8. Defaults to False.

        Returns:
            bitsarray: The result is a new bitsarray representing the result of the operation.
        """
        max_size = output_size

        if output_size == 0:
            output_size = len(self)
            max_size = None

        return bitsarray(
            self.to_int() + right_operand, 
            pad_to=output_size, 
            bytes_align=bytes_align,
            max_bits=max_size
            )


    def sub(self, right_operand, output_size=0, bytes_align=False):
        """Substraction between a bitsarray and an integer value.

        Args:
            right_operand (int): Value to substract.
            output_size (int, optional): The desired size of the resulting bitsarray. If the specified 
            size is smaller than the result of the substraction, the result will be truncated. If 0, 
            pads to the current length of the bits array.
            bytes_align (bool, optional): Pad to the nearest multiple of 8. Defaults to False.

        Returns:
            bitsarray: The result is a new bitsarray representing the result of the operation.
        """

        if output_size == 0:
            output_size = len(self)

        return bitsarray(
            self.to_int() - right_operand, 
            pad_to=output_size, 
            bytes_align=bytes_align
            )


    def mul(self, right_operand, output_size=0, bytes_align=False):
        """Multiplication between a bitsarray and an integer value.

        Args:
            right_operand (int): Value to multiply.
            output_size (int, optional): The desired size of the resulting bitsarray. If the specified 
            size is smaller than the result of the multiplication, the result will be truncated. If 0, 
            pads to the current length of the bits array.
            bytes_align (bool, optional): Pad to the nearest multiple of 8. Defaults to False.

        Returns:
            bitsarray: The result is a new bitsarray representing the result of the operation.
        """

        if output_size == 0:
            output_size = len(self)
            
        return bitsarray(
            self.to_int() * right_operand, 
            pad_to=output_size, 
            bytes_align=bytes_align
            )

    
    def bit_and(self, right_operand, output_size=0, bytes_align=False):
        """Bitwise and operation between a bitsarray and an integer value.

        Args:
            right_operand (int): Value to and.
            output_size (int, optional): The desired size of the resulting bitsarray. If the specified 
            size is smaller than the result of the multiplication, the result will be truncated. If 0, 
            pads to the current length of the bits array.
            bytes_align (bool, optional): Pad to the nearest multiple of 8. Defaults to False.

        Returns:
            bitsarray: The result is a new bitsarray representing the result of the operation.
        """

        if output_size == 0:
            output_size = len(self)
            
        return bitsarray(
            self.to_int() & right_operand, 
            pad_to=output_size, 
            bytes_align=bytes_align
            )


    def bit_or(self, right_operand, output_size=0, bytes_align=False):
        """Bitwise or operation between a bitsarray and an integer value.

        Args:
            right_operand (int): Value to or.
            output_size (int, optional): The desired size of the resulting bitsarray. If the specified 
            size is smaller than the result of the multiplication, the result will be truncated. If 0, 
            pads to the current length of the bits array.
            bytes_align (bool, optional): Pad to the nearest multiple of 8. Defaults to False.

        Returns:
            bitsarray: The result is a new bitsarray representing the result of the operation.
        """

        if output_size == 0:
            output_size = len(self)
            
        return bitsarray(
            self.to_int() | right_operand, 
            pad_to=output_size, 
            bytes_align=bytes_align
            )


    def bit_xor(self, right_operand, output_size=0, bytes_align=False):
        """Bitwise xor operation between a bitsarray and an integer value.

        Args:
            right_operand (int): Value to xor.
            output_size (int, optional): The desired size of the resulting bitsarray. If the specified 
            size is smaller than the result of the multiplication, the result will be truncated. If 0, 
            pads to the current length of the bits array.
            bytes_align (bool, optional): Pad to the nearest multiple of 8. Defaults to False.

        Returns:
            bitsarray: The result is a new bitsarray representing the result of the operation.
        """

        if output_size == 0:
            output_size = len(self)
            
        return bitsarray(
            self.to_int() ^ right_operand, 
            pad_to=output_size, 
            bytes_align=bytes_align
            )


if __name__ == '__main__':
    print("*********bitsarray tests*********")
    a = bitsarray(255, pad_to=7)
    b = bitsarray(12, pad_to=7)
    c = bitsarray(113)
    d = bitsarray(113, max_bits=5)
    e = bitsarray(256, bytes_align=True)
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
    print(f'Test bytes_align: {e}')
    print(len(e))
    print(f'Test __getitem__: {e[6:9]}')
