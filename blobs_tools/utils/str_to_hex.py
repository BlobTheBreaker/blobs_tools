string = input('String to convert: ')

tmpInt = 0

hexString = ''

for char in string:
    tmpInt = ord(char)
    hexString += str(hex(tmpInt)).split('x')[1] + " "

print(hexString)
