import socket
import threading

clients = {}
usernames = {}
banned_users = set()
blocked_ips = set()
lock = threading.Lock()


def handle_client(client_socket, addr):
    ip_address = addr[0]
    if ip_address in blocked_ips:
        client_socket.send('[!]你的IP已被封禁'.encode())
        client_socket.close()
        return

    username = client_socket.recv(1024).decode()
    if username in banned_users:
        client_socket.send('[!]你已被封禁'.encode())
        client_socket.close()
        return

    with lock:
        clients[client_socket] = (username, ip_address)
        usernames[username] = client_socket
        with open('user.txt', 'a') as f:
            f.write(username + '\n')

    welcome_message = f'[*]{username} 已登录'
    broadcast(welcome_message, client_socket)
    log_chat(welcome_message)

    while True:
        try:
            message = client_socket.recv(1024).decode()
            full_message = f'{username}: {message}'
            print(full_message)
            broadcast(full_message, client_socket)
            log_chat(full_message)
        except:
            remove_client(client_socket)
            break


def broadcast(message, client_socket=None):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message.encode())
            except:
                remove_client(client)


def remove_client(client_socket):
    with lock:
        if client_socket in clients:
            username, ip_address = clients[client_socket]
            disconnect_message = f'[*]{username} 已离开.'
            broadcast(disconnect_message, client_socket)
            log_chat(disconnect_message)
            del usernames[username]
            del clients[client_socket]
            client_socket.close()


def handle_server_commands():
    while True:
        command = input('')
        if command.startswith('/'):
            handle_admin_command('SERVER', command)
        else:
            server_message = f'SERVER: {command}'
            broadcast(server_message)
            log_chat(server_message)


def handle_admin_command(username, command):
    parts = command.split(' ', 2)
    cmd = parts[0]
    target = parts[1] if len(parts) > 1 else ''

    if cmd == '/kick' and target in usernames:
        kick_user(usernames[target])
    elif cmd == '/ban':
        ban_user(target)
    elif cmd == '/unban':
        unban_user(target)
    elif cmd == '/block':
        block_ip(target)
    elif cmd == '/unblock':
        unblock_ip(target)
    elif cmd == '/list':
        list_command = target
        if list_command == 'user':
            list_users()
        elif list_command == 'alluser':
            list_all_users()
        elif list_command == 'ban':
            list_banned_users()
        elif list_command == 'block':
            list_blocked_ips()


def kick_user(client_socket):
    if client_socket in clients:
        username, ip_address = clients[client_socket]
        client_socket.send('[!]你已被服务器踢出'.encode())
        remove_client(client_socket)
        print(f'[*]{username} 被服务器踢出')


def ban_user(username):
    banned_users.add(username)
    with open('black.txt', 'a') as f:
        f.write(username + '\n')
    if username in usernames:
        kick_user(usernames[username])
    print(f'[*]{username} 被封禁')


def unban_user(username):
    if username in banned_users:
        banned_users.remove(username)
        with open('black.txt', 'w') as f:
            f.writelines('\n'.join(banned_users))
        print(f'[*]{username} 解封')


def block_ip(ip_address):
    blocked_ips.add(ip_address)
    with open('blocked_ips.txt', 'a') as f:
        f.write(ip_address + '\n')
    for client_socket in list(clients):
        if client_socket.getpeername()[0] == ip_address:
            kick_user(client_socket)
    print(f'[*]{ip_address} 已封禁')


def unblock_ip(ip_address):
    if ip_address in blocked_ips:
        blocked_ips.remove(ip_address)
        with open('blocked_ips.txt', 'w') as f:
            f.writelines('\n'.join(blocked_ips))
        print(f'[*]{ip_address} 解封')


def list_users():
    print("当前在线用户:")
    for username, ip_address in clients.values():
        print(f'[*]{username} - {ip_address}')


def list_all_users():
    with open('user.txt', 'r') as f:
        all_users = f.read().strip()
    print(f"[*]登录记录:\n{all_users}")


def list_banned_users():
    print("[*]封禁列表:")
    for user in banned_users:
        print(user)


def list_blocked_ips():
    print("[*]封禁IP列表")
    for ip in blocked_ips:
        print(ip)


def log_chat(message):
    with open('chat.txt', 'a') as f:
        f.write(message + '\n')


try:
    with open('black.txt', 'r') as f:
        banned_users = set(line.strip() for line in f)
except FileNotFoundError:
    pass

try:
    with open('blocked_ips.txt', 'r') as f:
        blocked_ips = set(line.strip() for line in f)
except FileNotFoundError:
    pass

try:
    s = socket.socket()
    host = '0.0.0.0'
    port = 65533
    s.bind((host, port))
    s.listen()
    print(f'[*]{host} open on port {port}')
    print(f'/list user: 列出在线用户和IP地址')
    print(f'/list alluser: 列出所有用户')
    print(f'/list ban: 列出封禁用户')
    print(f'/list block: 列出封禁ip')
    print(f'/ban username: 封禁用户')
    print(f'/unban username: 解禁用户')
    print(f'/kick username: 踢出用户')
    print(f'/block ip: 封禁ip')
    print(f'/unblock ip: 解禁ip')

    threading.Thread(target=handle_server_commands, daemon=True).start()

    while True:
        client_socket, addr = s.accept()
        print(f'[*]{addr} 连接成功')
        threading.Thread(target=handle_client, args=(client_socket, addr)).start()

except Exception as e:
    print(e)
finally:
    s.close()
