import socket
import threading

def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode()
            if not message:
                break
            print(message)
        except:
            print("[!]服务异常你已被强制退出")
            break

try:
    s = socket.socket()
    host = input('input host name: ')
    port = 65533
    s.connect((host, port))
    username = input('Enter your username: ')
    s.send(username.encode())
    print(f'[*]多线程直接打字回车就是发送')

    receive_thread = threading.Thread(target=receive_messages, args=(s,))
    receive_thread.start()

    while True:
        try:
            message = input('')
            if message.lower() == '/exit':
                s.close()
                break
            s.send(message.encode())
        except Exception as e:
            print(e)
            s.close()
            break

except Exception as e:
    print(e)
