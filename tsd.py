from colorama import Fore as F
import os
from halo import Halo

os.system('clear')



__version__ = '5.0'
__author__ = "AlMu7mdy"

print(f'''
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
print(F.WHITE+'_'*40)
def listMethod():

    print(f'''
{F.GREEN}1- {F.RESET}HTTP-PROXIES.
{F.GREEN}2- {F.RESET}UDP.
{F.GREEN}3- {F.RESET}DNS.
{F.GREEN}4- {F.RESET}SLOWLORIS.
''')

    choiceMethod = int(input(f'''{F.CYAN}┌─({F.GREEN}TSD-Attack{F.CYAN})─({F.YELLOW}~ Method{F.CYAN})
└──╼ {F.YELLOW}~#{F.GREEN}'''))

    if choiceMethod == 1:
        os.system('cmd /k "python3 tools/tsd-http-proxies.py"' if os.name == 'nt' else 'python3 tools/tsd-http-proxies.py')
    elif choiceMethod ==2:
        os.system('cmd /k "python3 tools/tsd-udp.py"' if os.name == 'nt' else 'python3 tools/tsd-udp.py')
    elif choiceMethod == 3:
        os.system('cmd /k "python3 tools/tsd-dns.py"' if os.name == 'nt' else 'python3 tools/tsd-dns.py')
    elif choiceMethod == 4:
        os.system('cmd /k "python3 tools/tsd-slowloris.py"' if os.name == 'nt' else 'python3 tools/tsd-slowloris.py')
    else:
        print(f'{F.RED}( !!! ) {F.RESET}Error! Choice {F.CYAN}1{F.RESET} or {F.CYAN}2{F.RESET} or {F.CYAN}3{F.RESET} just!!')
        exit()

listMethod()
