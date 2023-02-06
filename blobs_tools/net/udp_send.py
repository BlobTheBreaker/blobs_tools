import socket

target_host = "127.0.0.1"
target_port = 9997

# Create socket object
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# No connection, this is udp

# Send data
client.sendto(b"AAABBBCCC", (target_host, target_port))

client.close()
