# Made By kxeuz1337
# github.com/kxeuz1337
# 5/9/2024

import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

def scrape_proxies():
    url = 'https://www.free-proxy-list.net/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    proxy_table = soup.find('table', {'id': 'proxylisttable'})
    proxies = []

    rows = proxy_table.find_all('tr')

    for row in rows[1:]:
        cols = row.find_all('td')
        if len(cols) > 1:
            ip = cols[0].text
            port = cols[1].text
            protocol = cols[6].text
            if protocol == 'yes': 
                proxies.append(f"http://{ip}:{port}")

    return proxies

def check_proxy(proxy):
    try:
        response = requests.get('http://httpbin.org/ip', proxies={'http': proxy, 'https': proxy}, timeout=5)
        return proxy if response.status_code == 200 else None
    except requests.RequestException:
        return None

def save_proxies(proxies, filename='proxies.txt'):
    with open(filename, 'w') as f:
        for proxy in proxies:
            f.write(f"{proxy}\n")
    print(f"Proxies saved to {filename}")

def load_proxies(filename='proxies.txt'):
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines()]

def main():
    while True:
        print("\nMenu:")
        print("1. Scrape proxies")
        print("2. Check proxies")
        print("3. Scrape and check proxies")
        print("4. Exit")
        choice = input("Choose an option (1-4): ")

        if choice == '1':
            print("Scraping proxies...")
            proxies = scrape_proxies()
            print(f"Found {len(proxies)} proxies.")
            save_proxies(proxies)
        
        elif choice == '2':
            print("Loading proxies from file...")
            proxies = load_proxies()
            print(f"Loaded {len(proxies)} proxies.")
            
            print("Checking proxies...")
            with ThreadPoolExecutor(max_workers=10) as executor:
                futures = [executor.submit(check_proxy, proxy) for proxy in proxies]
                working_proxies = [future.result() for future in as_completed(futures) if future.result()]

            print(f"Working proxies ({len(working_proxies)}):")
            for proxy in working_proxies:
                print(proxy)
        
        elif choice == '3':
            print("Scraping proxies...")
            proxies = scrape_proxies()
            print(f"Found {len(proxies)} proxies.")
            save_proxies(proxies)

            print("Loading proxies from file...")
            proxies = load_proxies()
            print(f"Loaded {len(proxies)} proxies.")
            
            print("Checking proxies...")
            with ThreadPoolExecutor(max_workers=10) as executor:
                futures = [executor.submit(check_proxy, proxy) for proxy in proxies]
                working_proxies = [future.result() for future in as_completed(futures) if future.result()]

            print(f"Working proxies ({len(working_proxies)}):")
            for proxy in working_proxies:
                print(proxy)
        
        elif choice == '4':
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == '__main__':
    main()
