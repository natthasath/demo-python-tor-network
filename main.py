import requests
from stem import Signal
from stem.control import Controller

# Tor proxy settings
TOR_PROXY_HOST = '127.0.0.1'
TOR_PROXY_PORT = 9150

# The website you want to access anonymously
TARGET_URL = 'https://example.com'

def set_tor_proxy(session):
    session.proxies = {
        'http': f'socks5://{TOR_PROXY_HOST}:{TOR_PROXY_PORT}',
        'https': f'socks5://{TOR_PROXY_HOST}:{TOR_PROXY_PORT}'
    }

def renew_tor_identity():
    with Controller.from_port(address=TOR_PROXY_HOST, port=TOR_PROXY_PORT) as controller:
        controller.authenticate(password=None)
        controller.signal(Signal.NEWNYM)

def fetch_webpage_via_tor(target_url):
    session = requests.session()
    set_tor_proxy(session)

    try:
        response = session.get(target_url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return None
    finally:
        session.close()

if __name__ == "__main__":
    # Connect to the Tor network and fetch the webpage anonymously
    webpage = fetch_webpage_via_tor(TARGET_URL)

    if webpage:
        print("Successfully fetched the webpage anonymously:")
        print(webpage)
    else:
        print("Failed to fetch the webpage anonymously.")
