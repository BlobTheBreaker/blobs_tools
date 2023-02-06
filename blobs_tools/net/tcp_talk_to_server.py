import socket

host_address = input('Target host: ')
host_port = int(input('Target port: '))
EXIT = 'exit'

def main():

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client.connect((host_address, host_port))
    print(f'[+] Connected to {host_address}:{host_port}')
    print(f'[*] Enter "{EXIT}" to close the connection')

    while True:
        message = input('[->] Send to host: ')
        client.sendall(message.encode())
        response = client.recv(4096)
        print(f'[<-] Host sent: {response.decode("UTF-8")}\r\n')
        if message == EXIT:
            print(f'[-] Successfully disconnected from {host_address}:{host_port}')
            client.close()
            break


if __name__ == '__main__':
    main()
