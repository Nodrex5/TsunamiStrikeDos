from colorama import Fore as F
import os

print(f'''
{F.GREEN}
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣾⣿⣦⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⣿⣿⣿⣿⣿⣽⣿⣷⣴⣤⣤⡄⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣀⣴⣿⣿⣿⣿⣿⣿⣿⣏⣛⣛⣉⣛⡛⠋⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠉⠙⠻⢿⣿⣿⣿⠟⠉⠉⠉⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                {F.CYAN} TsunamiStrikeDos {F.GREEN}V 3.1 {F.RESET}
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
        os.system('cmd /k "python tsd-http-proxies.py"' if os.name == 'nt' else 'python tsd-http-proxies.py')
    elif choiceMethod ==2:
        os.system('cmd /k "python tsd-udp.py"' if os.name == 'nt' else 'python tsd-udp.py')
    elif choiceMethod == 3:
        os.system('cmd /k "tsd-dns.py"' if os.name == 'nt' else 'python tsd-dns.py')
    else:
        print(f'{F.RED} Error! Choice 1 or 2 or 3 just!!')
        exit()


