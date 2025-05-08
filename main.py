from kasawa import console
import json
import tls_client
import random
import time
from pystyle import Colors, Colorate, Center, Anime, Write
import threading
import requests
from datetime import datetime, timezone, timedelta

session = tls_client.Session(
    client_identifier="chrome_120",
    random_tls_extension_order=True,
    ja3_string="771,4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53,0-23-65281-10-11-35-16-5-13-18-51-45-43-27-17513,29-23-24,0",
    h2_settings={
        "HEADER_TABLE_SIZE": 65536,
        "MAX_CONCURRENT_STREAMS": 1000,
        "INITIAL_WINDOW_SIZE": 6291456,
        "MAX_HEADER_LIST_SIZE": 262144
    },
    h2_settings_order=[
        "HEADER_TABLE_SIZE",
        "MAX_CONCURRENT_STREAMS",
        "INITIAL_WINDOW_SIZE",
        "MAX_HEADER_LIST_SIZE"
    ],
    supported_signature_algorithms=[
        "ECDSAWithP256AndSHA256",
        "PSSWithSHA256",
        "PKCS1WithSHA256",
        "ECDSAWithP384AndSHA384",
        "PSSWithSHA384",
        "PKCS1WithSHA384",
        "PSSWithSHA512",
        "PKCS1WithSHA512",
    ],
    supported_versions=["GREASE", "1.3", "1.2"],
    key_share_curves=["GREASE", "X25519"],
    cert_compression_algo="brotli",
    pseudo_header_order=[
        ":method",
        ":authority",
        ":scheme",
        ":path"
    ],
    connection_flow=15663105,
    header_order=[
        "accept",
        "user-agent",
        "accept-encoding",
        "accept-language"
    ]
)

with open("input/proxies.txt", encoding="utf-8") as f:
    proxies = f.read().splitlines()

with open("config.json", encoding="utf-8") as f:
    Config = json.load(f)

with open("input/tokens.txt", "r", encoding="utf-8") as f:
    tokens = f.read().splitlines()

proxy = Config["Proxies"]

def change_proxy():
    while True:
        selected_proxy = random.choice(proxies)
        session.proxies = {
            "http": f"http://{selected_proxy}",
            "https": f"http://{selected_proxy}"
        }
        time.sleep(5)

if Config.get("proxies") == True:
    proxy_thread = threading.Thread(target=change_proxy, daemon=True)
    proxy_thread.start()

def snowflake_to_datetime(snowflake_id: int) -> datetime:
    discord_epoch = 1420070400000
    timestamp = ((snowflake_id >> 22) + discord_epoch) / 1000
    return datetime.fromtimestamp(timestamp, tz=timezone.utc)

def convert_to_utc_plus7(dt: datetime) -> datetime:
    return dt.astimezone(timezone(timedelta(hours=7)))

def time_since(dt: datetime) -> str:
    now = datetime.now(timezone(timedelta(hours=7)))
    delta = now - dt
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes = remainder // 60
    return f"{days} Days {hours} Hours {minutes} Minutes Ago"

def format_time(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def headers(token):
    headers = {
        'accept': '*/*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,th;q=0.7',
        'authorization': token,
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://discord.com/channels/1358859535401488474/1358859536290811988',
        'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
        'x-debug-options': 'bugReporterEnabled',
        'x-discord-locale': 'th',
        'x-discord-timezone': 'Asia/Bangkok',
        'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLUdCIiwiaGFzX2NsaWVudF9tb2RzIjpmYWxzZSwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEzNS4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTM1LjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiJodHRwczovL2Rpc2NvcmQuY29tLz9kaXNjb3JkdG9rZW49TVRNMk5ERTRORFUzTVRZNE16UXdOVGd5TkEuRzJsV295LlgwN1I0WWhoY3drWmI3YnhRZi1IN2V2Z25RdHZYZzZ6WDM0VG5VIiwicmVmZXJyaW5nX2RvbWFpbiI6ImRpc2NvcmQuY29tIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjM5NzcyMCwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbCwiY2xpZW50X2xhdW5jaF9pZCI6ImM3ZDFhNjgyLTYzODMtNDAyYy1iZWJhLWY1MDA3OGY2ZWQzYiIsImNsaWVudF9oZWFydGJlYXRfc2Vzc2lvbl9pZCI6Ijg1M2YzMmJkLTVjMzQtNGJiNC1iZjg3LWJiYzUxYzMwZDU3ZiJ9',
    }
    return headers


def check_token(token, email=None, password=None):
    try:
        response = session.get(
            "https://discordapp.com/api/v9/users/@me",
            headers=headers(token)
        )
        r = response.json()
        id = int(r['id'])
        created_utc7 = convert_to_utc_plus7(snowflake_to_datetime(id))
        username = r['username']
        globalname = r['global_name']
        phone = r.get('phone')
        email_verified = r.get('verified')

        console.log.info(f"[Username] {username} ({id})")
        console.log.info(f"[GlobalName] {globalname}")
        console.log.info(f"[Phone] {phone if phone else '❌'}")
        console.log.info(f"[Email] {r.get('email') if email_verified else '❌'}")
        console.log.info(f"[Creation] {format_time(created_utc7)} ({time_since(created_utc7)})")
        console.log.success("═══════════════════════════════════════════════════════════════════")

        if email_verified and phone:
            with open("output/fv.txt", "a") as f:
                if email and password is None:
                    f.write(token + "\n")
                else:
                    f.write(f"{email}:{password}:{token}\n")
            return "fv"
        elif email_verified:
            with open("output/ev.txt", "a") as f:
                if email and password is None:
                    f.write(token + "\n")
                else:
                    f.write(f"{email}:{password}:{token}\n")
            return "ev"
        elif phone and not email_verified: 
            with open("output/reqmail.txt", "a") as f:
                if email and password is None:
                    f.write(token + "\n")
                else:
                    f.write(f"{email}:{password}:{token}\n")
            return "reqmail"
        elif email_verified and not phone: 
            with open("output/reqphone.txt", "a") as f:
                if email and password is None:
                    f.write(token + "\n")
                else:
                    f.write(f"{email}:{password}:{token}\n")
            return "reqphone"
        else:
            with open("output/failed.txt", "a") as f:
                if email and password is None:
                    f.write(token + "\n")
                else:
                    f.write(f"{email}:{password}:{token}\n")
            return "failed"

    except requests.RequestException as e:
        console.log.error(f"Request failed for token {token}: {e}")
    except Exception as e:
        console.log.error(f"Unexpected error for token {token}: {e}")

def TokensChecker():
    fv = []
    ev = []
    reqmail = []
    reqphone = []
    failed = []

    for line in tokens:
        try:
            token = line.split(":")[2]
            passw = line.split(":")[1]
            email = line.split(":")[0]
            result = check_token(token.strip(), email, passw)
            if result == "fv":
                fv.append(token)
            elif result == "ev":
                ev.append(token)
            elif result == "reqmail":
                reqmail.append(token)
            elif result == "reqphone":
                reqphone.append(token)
            else:
                failed.append(token)
        except:
            result = check_token(token.strip())
            if result == "fv":
                fv.append(token)
            elif result == "ev":
                ev.append(token)
            elif result == "reqmail":
                reqmail.append(token)
            elif result == "reqphone":
                reqphone.append(token)
            else:
                failed.append(token)
                
        console.title(f"FV : {len(fv)} EV:{len(ev)} Rm:{len(reqmail)} Rp:{len(reqphone)}, F:{len(failed)}")

def main():
    print(Colorate.Horizontal(Colors.cyan_to_blue, rf'''
 __  __    __   _  _  ____  ____     ___  _   _  ____  ___  _  _  ____  ____  
(  \/  )  /__\ ( \/ )(  _ \(_  _)   / __)( )_( )( ___)/ __)( )/ )( ___)(  _ \
 )    (  /(__)\ \  /  ) _ < _)(_   ( (__  ) _ (  )__)( (__  )  (  )__)  )   / 
(_/\/\_)(__)(__)(__) (____/(____)   \___)(_) (_)(____)\___)(_)\_)(____)(_)\_) 
Welcome to Token Checker by Maybi - No Skid my Programs plsss
                              
'''))
    console.title("Maybi - Checker")
    time.sleep(2)
    TokensChecker()
    input()

if __name__ == "__main__":
    console.clear()
    main()
