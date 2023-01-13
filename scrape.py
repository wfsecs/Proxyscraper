from colorama import Fore, init
import threading
import requests
import time

init()

# Variables
bad_status_codes = [403, 400, 500, 502]
proxies = []
protocol = 'http'
timeout = '10000'
country = 'all'
ssl = 'all'
anonymity = 'all'

# Colors
F_RED = Fore.RED
F_GREEN = Fore.GREEN
F_BLUE = Fore.BLUE
RESET = Fore.RESET
F_YELLOW = Fore.YELLOW
L_BLACK = Fore.LIGHTBLACK_EX
L_GREEN = Fore.LIGHTGREEN_EX
L_RED = Fore.LIGHTRED_EX
L_BLUE = Fore.LIGHTBLUE_EX


# Functions
def get_original_ip():
    ip_info = requests.get('http://jsonip.com').json()
    return ip_info['ip']


def check_proxy(proxy):
    used_proxy = {"http": proxy}

    with open('working_proxies.txt', 'a+') as f:
        try:
            ip_info = requests.get('http://jsonip.com/', proxies=used_proxy)

            if ip_info.status_code == 429:
                print(f'    {F_YELLOW}[!] Rate limited!{RESET} Waiting 10 Seconds...')
                time.sleep(10)

            elif ip_info.status_code not in bad_status_codes:
                if ip_info.json()['ip'] != original_ip:
                    print(f'    [{ip_info.status_code}] {L_GREEN}[+]{F_GREEN} Working proxy found >{RESET} "{proxy}" ')
                    f.write(f'''{proxy}
''')
                else:
                    print(f'    [{ip_info.status_code}] {L_RED} Connected with IP{L_BLACK} {ip_info.json()["ip"]}{L_RED} [-]{F_RED} Invalid proxy >{RESET} "{proxy}"')
        except:
            pass


def check_proxies():
    global proxies
    for proxy in proxies:
        Thread = threading.Thread(target=check_proxy, args=(proxy,), daemon=True)  # Starts the scanning thread
        time.sleep(0.05) # Pause for a while to prevent crashing
        Thread.start()


def get_last_updated():
    information = requests.get('https://api.proxyscrape.com/v2/?request=proxyinfo').json()
    return information['last_updated']


def get_proxy_count():
    information = requests.get('https://api.proxyscrape.com/v2/?request=proxyinfo').json()
    return information['proxy_count']


def get_proxies():
    url = f'http://api.proxyscrape.com/v2/?request=displayproxies&protocol={protocol}&timeout={timeout}&country={country}&ssl={ssl}&anonymity={anonymity}'
    proxylist = requests.get(url).text

    for proxy in proxylist.splitlines():
        proxies.append(proxy)
        print(f'    {L_BLUE}[%]{F_BLUE} Added{RESET} {proxy}{F_BLUE} to proxies.')
    else:
        print(f'''{L_GREEN}    [+]{F_GREEN} Done scraping{RESET} {len(proxies)}{F_GREEN} proxies.
    
    {L_BLUE}[%]{F_BLUE} Checking proxies...{RESET}''')

        check_proxies()


# Tell about proxies
print(f'''
    There are {F_YELLOW}{get_proxy_count()}{RESET} proxies...
    Proxies were updated{F_YELLOW} {get_last_updated()}{RESET}
    
    Protocol: {F_YELLOW}{protocol}{RESET}
    Timeout: {F_YELLOW}{timeout}{RESET}
    Country: {F_YELLOW}{country}{RESET}
    SSL: {F_YELLOW}{ssl}{RESET}
    Anonymity: {F_YELLOW}{anonymity}{RESET}
''')

# Gets your IP. Proxies make your ip different so this script compares your IP to the Proxy IP
original_ip = get_original_ip()

# Start
get_proxies()
