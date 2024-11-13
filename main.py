import os
import time
import requests
from termcolor import colored
import pyfiglet
import inquirer
from threading import Thread
from datetime import datetime

def read_lines(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]

class Config:
    def __init__(self):
        self.base_url = 'https://nodepay.org'
        self.ping_url = 'http://52.77.10.116/api/network/ping'
        self.retry_interval = 30
        self.session_url = 'http://api.nodepay.ai/api/auth/session'

class Logger:
    @staticmethod
    def info(message, data=None):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(colored(f"[{timestamp}] [INFO] {message}: {data}", 'green'))

    @staticmethod
    def error(message, data=None):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(colored(f"[{timestamp}] [ERROR] {message}: {data}", 'red'))

class Bot:
    def __init__(self, config, logger, proxy=None):
        self.config = config
        self.logger = logger
        self.proxy = proxy

    def connect(self, token):
        try:
            user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            account_info = self.get_session(token, user_agent)
            print(colored(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Session initiated successfully for token: {token[:10]}...!", 'cyan'))
            self.logger.info('Session info', {'status': 'success', 'token': token[:10] + '...'})

            while True:
                try:
                    self.send_ping(account_info, token, user_agent)
                except Exception as error:
                    print(colored(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Ping error for token {token[:10]}...: {error}", 'yellow'))
                    self.logger.error('Ping error', {'error': str(error), 'token': token[:10] + '...'})

                time.sleep(self.config.retry_interval)
        except Exception as error:
            print(colored(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Connection error for token {token[:10]}...: {error}", 'red'))
            self.logger.error('Connection error', {'error': str(error), 'token': token[:10] + '...'})

    def get_session(self, token, user_agent):
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'User-Agent': user_agent,
            'Accept': 'application/json'
        }

        if self.proxy:
            response = requests.post(self.config.session_url, headers=headers, proxies=self.proxy)
        else:
            response = requests.post(self.config.session_url, headers=headers)

        return response.json()['data']

    def send_ping(self, account_info, token, user_agent):
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

        if self.proxy:
            response = requests.post(self.config.ping_url, json=ping_data, headers=headers, proxies=self.proxy)
        else:
            response = requests.post(self.config.ping_url, json=ping_data, headers=headers)

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(colored(f"[{timestamp}] Ping sent successfully for token {token[:10]}...", 'magenta'))
        self.logger.info('Ping sent', {'status': 'success', 'token': token[:10] + '...'})

def display_welcome():
    ascii_art = pyfiglet.figlet_format("Nodepay Bot")
    print(colored(ascii_art, 'yellow'))
    print(colored("========================================", 'cyan'))
    print(colored("=        Welcome to Miwe Airdrop       =", 'cyan'))
    print(colored("=       Automated & Powerful Bot       =", 'cyan'))
    print(colored("========================================", 'cyan'))

def ask_proxy_mode():
    questions = [
        inquirer.List('proxy_mode',
                      message="Do you want to use a proxy?",
                      choices=['No Proxy', 'Use Proxy'],
                      default='No Proxy',
        ),
    ]
    answer = inquirer.prompt(questions)
    return answer['proxy_mode']

def configure_proxy():
    proxies = read_lines('proxy.txt')
    if not proxies:
        print(colored("No proxies found in proxy.txt", 'red'))
        return None

    proxy = proxies[0].split(':')
    if len(proxy) == 4:
        host, port, username, password = proxy
        return {
            'http': f'http://{username}:{password}@{host}:{port}',
            'https': f'http://{username}:{password}@{host}:{port}'
        }
    return None

def main():
    display_welcome()

    tokens = read_lines('token.txt')
    config = Config()
    logger = Logger()

    proxy_mode = ask_proxy_mode()

    proxy = None
    if proxy_mode == 'Use Proxy':
        proxy = configure_proxy()
        if proxy:
            print(colored(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Proxy enabled: {proxy['http'][:30]}...", 'green'))
        else:
            print(colored("No valid proxy configured, using direct connection.", 'yellow'))

    bot = Bot(config, logger, proxy)

    threads = []
    for token in tokens:
        # Run each connection in a separate thread to handle multiple accounts simultaneously
        thread = Thread(target=bot.connect, args=(token,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

if __name__ == '__main__':
    main()
