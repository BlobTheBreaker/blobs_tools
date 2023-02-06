from ..utils.structs import bitsarray

# Basic implementation of a 32bits crc
# Requires the bitsarray module
# Generator polynomial
# From https://en.wikipedia.org/wiki/Cyclic_redundancy_check#Polynomial_representations_of_cyclic_redundancy_checks
# Using: x^32 + x^26 + x^23 + x^22 + x^16 + x^12 + x^11 + x^10 + x^8 + x^7 + x^5 + x^4 + x^2 + x + 1

def crc32(msg):

    poly = 0b100000100110000010001110110110111
    # Encode it
    msg = msg.encode('UTF-8')

    # Set the msg and poly to be xored.
    msg_bits = bitsarray(int.from_bytes(msg, 'big'))
    msg_bits.pad_right(len(msg_bits) + 32)
    poly_bits = bitsarray(int(poly))
    poly_bits.pad_right(len(msg_bits))

    # Start the division
    exit_next = False
    while True:
        if poly_bits.index(1) != msg_bits.index(1):
            # print(msg_bits)
            # print(poly_bits)
            poly_bits.shift_right()
            # print('No xor')
            # print(poly_bits)
            # print('\n')
        else:
            # print('Did xor')
            # print(msg_bits)
            msg_bits = bitsarray(msg_bits.to_int() ^ poly_bits.to_int(), pad_to=len(msg_bits))
            # print(poly_bits)
            # print(msg_bits)
            # print('\n')

        # Allows for possibly the last xor to happen
        if exit_next:
            break

        if poly_bits.bits_list[-1] == 1:
            exit_next = True


    return hex(msg_bits.to_int())


if __name__ == "__main__":
    # Original message
    msg = 'hi'
    print(crc32(msg))