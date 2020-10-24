# Terminal Color
import ipaddress
from colorama import init, Fore, Back, Style
init()

test = True
while test == True:
    try:
        IP_Static = input("Dia chi Ip tinh: ")
        if ipaddress.ip_address(IP_Static).is_private == True:
            test = True
            print(
                Fore.RED + "Dia chi ip la private, moi nhap lai dia chi public!" + Fore.RESET)
        else:
            test = False
    except ValueError:
        print(Fore.RED + "Sai cu phap dia chi ip!" + Fore.RESET)
