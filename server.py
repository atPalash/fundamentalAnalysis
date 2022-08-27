import socket  # Import socket module
import _thread

from conf.conf_editor import read

registered_features = {}


def parse_message(msg, clientsocket):
    try:
        msg = msg.strip().split(':')
        command = msg[0]
        if command == 'REGISTER':
            registered_features[msg[1]] = clientsocket
        elif command == 'CALL':
            args = msg[1].split(',')
            registered_features[args[0]].send(msg[1].encode())
        else:
            print("COMMAND unknown")
    except Exception as e:
        print(e.args)
        clientsocket.close()


def on_new_client(clientsocket, addr):
    while True:
        try:
            msg = clientsocket.recv(1024).decode('utf-8')
            parse_message(msg=msg, clientsocket=clientsocket)
        except ConnectionResetError as ce:
            continue
        except Exception as e:
            print(e.args)


s = socket.socket()  # Create a socket object
host = socket.gethostname()  # Get local machine name
port = read()['port_config']['server']  # Reserve a port for your service.
s.bind((host, port))  # Bind to the port
s.listen(5)  # Now wait for client connection.

# print 'Got connection from', addr
while True:
    c, addr = s.accept()  # Establish connection with client.
    _thread.start_new_thread(on_new_client, (c, addr))
    # Note it's (addr,) not (addr) because second parameter is a tuple
    # Edit: (c,addr)
    # that's how you pass arguments to functions when creating new threads using thread module.
s.close()
