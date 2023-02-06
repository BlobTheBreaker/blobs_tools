import socket
import threading

host_ip = "0.0.0.0"
host_port = 9998
EXIT = 'exit'


def main():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host_ip, host_port))
    server.listen(5)
    print(f'[*] Listening on {host_ip}:{host_port} ...')

    while True:
        client, address = server.accept()
        print(f'[+] Accepted connection from {address[0]}:{address[1]}')
        client_handler = threading.Thread(target=handle_client, args=(client, address))
        client_handler.start()


def handle_client(client_socket, client_address):

    while True:
        request = client_socket.recv(4096)
        req_str = request.decode('UTF-8')
        if req_str == EXIT:
            client_socket.send(b'Disconnecting')
            client_socket.close()
            print(f'[-] Client {client_address[0]}:{client_address[1]} disconnected')
            break

        print(f'[->] {client_address[0]}:{client_address[1]} says: {request.decode("UTF-8")}')
        client_socket.send(b'ACK')


if __name__ == '__main__':
    main()
