from colorama import Fore as F
import os
os.system('clear')
print(f'''
{F.GREEN}
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣾⣿⣦⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⣿⣿⣿⣿⣿⣽⣿⣷⣴⣤⣤⡄⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣀⣴⣿⣿⣿⣿⣿⣿⣿⣏⣛⣛⣉⣛⡛⠋⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠉⠙⠻⢿⣿⣿⣿⠟⠉⠉⠉⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                {F.CYAN} TsunamiStrikeDos {F.GREEN}V 3.2.1 {F.RESET}
                {F.WHITE} MAIN PAGE {F.RESET}
''')


def listMethod():

    print(f'''
1- HTTP-PROXIES.
2- UDP.
3- DNS
''')

    choiceMethod = (int(input(f'{F.CYAN}[⚡] {F.RESET}Choice Method >> {F.GREEN}')))

    if choiceMethod == 1:
        os.system('cmd /k "python3 tools/tsd-http-proxies.py"' if os.name == 'nt' else 'python3 tools/tsd-http-proxies.py')
    elif choiceMethod ==2:
        os.system('cmd /k "python3 tools/tsd-udp.py"' if os.name == 'nt' else 'python3 tools/tsd-udp.py')
    elif choiceMethod == 3:
        os.system('cmd /k "python3 tools/tsd-dns.py"' if os.name == 'nt' else 'python3 tools/tsd-dns.py')
    else:
        print(f'{F.RED}[ !!! ] {F.RESET}Error! Choice {F.CYAN}1{F.RESET} or {F.CYAN}2{F.RESET} or {F.CYAN}3{F.RESET} just!!')
        exit()

listMethod()
