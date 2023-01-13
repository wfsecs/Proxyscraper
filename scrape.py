from colorama import Fore, init
import threading
import requests
import asyncio
import time

init()

# Variables
bad_status_codes = [403, 400, 500, 502]
proxies = []

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


async def check_proxy(proxy):
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
                # else:
                    # print(f'    [{ip_info.status_code}]{L_RED} Connected with IP{L_BLACK} {ip_info.json()["ip"]}{L_RED} [-]{F_RED} Invalid proxy >{RESET} "{proxy}"')
        except:
            pass


async def check_proxies():
    global proxies
    for proxy in proxies:
        Thread = threading.Thread(target=asyncio.run, args=(check_proxy(proxy),))  # Starts the scanning thread
        time.sleep(0.03) # Pause for a while to prevent crashing
        Thread.start()


async def get_proxies():
    urls = ['http://api.proxyscrape.com/v2/?request=displayproxies&protocol=http', 'https://www.proxy-list.download/api/v1/get?type=http']

    print(f'    [?] Scraping from {len(urls)} APIs')
    for url in urls:
        proxylist = requests.get(url).text

        for proxy in proxylist.splitlines():
            proxies.append(proxy)
            print(f'    {L_BLUE}[%]{F_BLUE} Added{RESET} {proxy}{F_BLUE} to proxies.')
    else:
        print(proxies)
        print(f'''{L_GREEN}    [+]{F_GREEN} Done scraping{RESET} {len(proxies)}{F_GREEN} proxies.
        
        {L_BLUE}[%]{F_BLUE} Checking proxies...{RESET}''')

        await check_proxies()


# Gets your IP. Proxies make your ip different so this script compares your IP to the Proxy IP
original_ip = get_original_ip()

# Start
asyncio.run(get_proxies())
