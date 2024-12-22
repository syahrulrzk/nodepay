import time
import requests
from termcolor import colored
import pyfiglet
from threading import Thread
from datetime import datetime
import itertools

class Config:
    def __init__(self):
        self.base_url = 'https://nodepay.org'
        self.ping_url = 'http://nw.nodepay.ai/api/network/ping'
        self.retry_interval = 30
        self.session_url = 'http://api.nodepay.ai/api/auth/session'

class Logger:
    @staticmethod
    def info(message, data=None):
        print(colored(f"[INFO] {message}: {data}", 'green'))

    @staticmethod
    def error(message, data=None):
        print(colored(f"[ERROR] {message}: {data}", 'red'))

class Bot:
    def __init__(self, config, logger, proxies=None):
        self.config = config
        self.logger = logger
        self.proxies = proxies or []
        self.proxy_cycle = itertools.cycle(self.proxies)

    def connect(self, token):
        try:
            user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            account_info = self.get_session(token, user_agent)
            print(colored(f"Connected to session successfully for token {token[:10]}...", 'cyan'))
            self.logger.info('Session info', {'status': 'success', 'token': token[:10] + '...'})

            while True:
                try:
                    proxy = next(self.proxy_cycle)
                    self.send_ping(account_info, token, user_agent, proxy)
                except Exception as error:
                    print(colored(f"Ping error for token {token[:10]}...: {error}", 'yellow'))
                    self.logger.error('Ping error', {'error': str(error), 'token': token[:10] + '...'})

                time.sleep(self.config.retry_interval)
        except Exception as error:
            print(colored(f"Connection error for token {token[:10]}...: {error}", 'red'))
            self.logger.error('Connection error', {'error': str(error), 'token': token[:10] + '...'})

    def get_session(self, token, user_agent):
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'User-Agent': user_agent,
            'Accept': 'application/json'
        }

        if self.proxies:
            response = requests.post(self.config.session_url, headers=headers, proxies=self.proxies[0])
        else:
            response = requests.post(self.config.session_url, headers=headers)

        return response.json()['data']

    def send_ping(self, account_info, token, user_agent, proxy):
        ping_data = {
            'id': account_info.get('uid', 'Unknown'),
            'browser_id': account_info.get('browser_id', 'random_browser_id'),
            'timestamp': int(time.time()),
            'version': '2.2.7'
        }

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'User-Agent': user_agent,
            'Accept': 'application/json'
        }

        try:
            start_time = time.time()

            response = requests.post(self.config.ping_url, json=ping_data, headers=headers, proxies=proxy)

            end_time = time.time()

            ping_duration = end_time - start_time

            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(colored(f"[{timestamp}] Ping sent successfully for token {token[:10]}... using proxy {proxy['http'][:30]}... | Duration: {ping_duration:.2f} seconds", 'magenta'))
            self.logger.info('Ping sent', {'status': 'success', 'token': token[:10] + '...', 'proxy': proxy['http'][:30], 'duration': f'{ping_duration:.2f} seconds'})
        except Exception as error:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(colored(f"[{timestamp}] Ping error for token {token[:10]}... using proxy {proxy['http'][:30]}: {error}", 'yellow'))
            self.logger.error('Ping error', {'error': str(error), 'token': token[:10] + '...', 'proxy': proxy['http'][:30]})

def display_welcome():
    ascii_art = pyfiglet.figlet_format("Nodepay Bot")
    print(colored(ascii_art, 'yellow'))
    print(colored("========================================", 'cyan'))
    print(colored("=        Welcome to MiweAirdrop        =", 'cyan'))
    print(colored("=       Automated & Powerful Bot       =", 'cyan'))
    print(colored("========================================", 'cyan'))

def main():
    display_welcome()

    # Masukkan token Anda di sini
    tokens = [
        'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzIwMDY2NDQwMTMzMDM4MDgwIiwiaWF0IjoxNzM0ODAzOTM1LCJleHAiOjE3MzYwMTM1MzV9.fd72DJAMXEoNE2kNrhhNA2LC1jvxW3LqfDVPhuNRjPPD5BvzJfvbXOhOXyVZCiOVREcY8jNZ30lu4pSqq0pfSg'
    ]

    # Masukkan daftar proxy Anda di sini
    proxy_data = [
        '107.172.163.27:6543:boxmbdve:baod4wb9c9d6',
        '64.137.42.112:5157:boxmbdve:baod4wb9c9d6',
        '173.211.0.148:6641:boxmbdve:baod4wb9c9d6',
        '161.123.152.115:6360:boxmbdve:baod4wb9c9d6',
        '167.160.180.203:6754:boxmbdve:baod4wb9c9d6',
        '154.36.110.199:6853:boxmbdve:baod4wb9c9d6',
        '173.0.9.70:5653:boxmbdve:baod4wb9c9d6',
        '173.0.9.209:5792:boxmbdve:baod4wb9c9d6'
    ]

    proxies = []
    for proxy in proxy_data:
        host, port, username, password = proxy.split(':')
        proxy_dict = {
            'http': f'http://{username}:{password}@{host}:{port}',
            'https': f'http://{username}:{password}@{host}:{port}'
        }
        proxies.append(proxy_dict)

    config = Config()
    logger = Logger()
    bot = Bot(config, logger, proxies)

    threads = []
    for token in tokens:
        thread = Thread(target=bot.connect, args=(token,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

if __name__ == '__main__':
    main()
