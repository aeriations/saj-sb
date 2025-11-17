import binascii
import os
import requests
import json
import base64
import re
from Crypto.Cipher import AES
from win32crypt import CryptUnprotectData


def token():
    token_ids = get_tokens()
    for index, token in enumerate(token_ids):
        try:
            r = requests.get(
                "https://discordapp.com/api/v6/users/@me",
                headers={"Authorization": token},
            )
            user = r.json()
            user_info = user["username"]
            print(f"[{index}] user: {user_info}")
        except:
            pass
    
    response = input(f"specify which account: 0 -> {len(token_ids) - 1}: ")
    response = int(response)

    if token_ids[response]:
        return token_ids[response]
    else:
        print("invalid index.")
        exit()


def is_base64(s):
    try:
        return base64.b64encode(base64.b64decode(s)) == s.encode()
    except Exception:
        return False

def add_padding(s):
    while len(s) % 4 != 0:
        s += "="
    return s


def decrypt_val(buff, master_key):
    iv = buff[3:15]
    payload = buff[15:]
    cipher = AES.new(master_key, AES.MODE_GCM, iv)
    decrypted_pass = cipher.decrypt(payload)
    decrypted_pass = decrypted_pass[:-16].decode()

    return decrypted_pass


def get_key(path):
    if not os.path.exists(path):
        return

    if "os_crypt" not in open(path, "r", encoding="utf-8").read():
        return

    with open(path, "r", encoding="utf-8") as f:
        c = f.read()

    local_state = json.loads(c)
    master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    master_key = master_key[5:]
    master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
    return master_key


def get_tokens():
    all_tokens = []
    appdata = os.getenv("LOCALAPPDATA")
    roaming = os.getenv("APPDATA")
    encrypt_regex = r"dQw4w9WgXcQ:[^\"]*"
    normal_regex = r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}"
    paths = {
        "Discord": roaming + "\\discord\\Local Storage\\leveldb\\",
        "Discord Canary": roaming + "\\discordcanary\\Local Storage\\leveldb\\",
        "Lightcord": roaming + "\\Lightcord\\Local Storage\\leveldb\\",
        "Discord PTB": roaming + "\\discordptb\\Local Storage\\leveldb\\",
        "Opera": roaming + "\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\",
        "Opera GX": roaming
        + "\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb\\",
        "Amigo": appdata + "\\Amigo\\User Data\\Local Storage\\leveldb\\",
        "Torch": appdata + "\\Torch\\User Data\\Local Storage\\leveldb\\",
        "Kometa": appdata + "\\Kometa\\User Data\\Local Storage\\leveldb\\",
        "Orbitum": appdata + "\\Orbitum\\User Data\\Local Storage\\leveldb\\",
        "CentBrowser": appdata + "\\CentBrowser\\User Data\\Local Storage\\leveldb\\",
        "7Star": appdata + "\\7Star\\7Star\\User Data\\Local Storage\\leveldb\\",
        "Sputnik": appdata + "\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb\\",
        "Vivaldi": appdata + "\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb\\",
        "Chrome SxS": appdata
        + "\\Google\\Chrome SxS\\User Data\\Local Storage\\leveldb\\",
        "Chrome": appdata
        + "\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\",
        "Chrome1": appdata
        + "\\Google\\Chrome\\User Data\\Profile 1\\Local Storage\\leveldb\\",
        "Chrome2": appdata
        + "\\Google\\Chrome\\User Data\\Profile 2\\Local Storage\\leveldb\\",
        "Chrome3": appdata
        + "\\Google\\Chrome\\User Data\\Profile 3\\Local Storage\\leveldb\\",
        "Chrome4": appdata
        + "\\Google\\Chrome\\User Data\\Profile 4\\Local Storage\\leveldb\\",
        "Chrome5": appdata
        + "\\Google\\Chrome\\User Data\\Profile 5\\Local Storage\\leveldb\\",
        "Epic Privacy Browser": appdata
        + "\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb\\",
        "Microsoft Edge": appdata
        + "\\Microsoft\\Edge\\User Data\\Defaul\\Local Storage\\leveldb\\",
        "Uran": appdata
        + "\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb\\",
        "Yandex": appdata
        + "\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb\\",
        "Brave": appdata
        + "\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\",
        "Iridium": appdata + "\\Iridium\\User Data\\Default\\Local Storage\\leveldb\\",
    }
    for name, path in paths.items():
        if not os.path.exists(path):
            continue
        _discord = name.replace(" ", "").lower()
        if "cord" in path:
            if not os.path.exists(roaming + f"\\{_discord}\\Local State"):
                continue
            for file_stuff in os.listdir(path):
                if file_stuff[-3:] not in ["log", "ldb"]:
                    continue
                for line in [
                    x.strip()
                    for x in open(f"{path}\\{file_stuff}", errors="ignore").readlines()
                    if x.strip()
                ]:
                    for i in re.findall(encrypt_regex, line):
                        token = decrypt_val(
                            base64.b64decode(i.split("dQw4w9WgXcQ:")[1]),
                            get_key(roaming + f"\\{_discord}\\Local State"),
                        )
                        all_tokens.append(token)
        else:
            for file_stuff in os.listdir(path):
                if file_stuff[-3:] not in ["log", "ldb"]:
                    continue
                for line in [
                    x.strip()
                    for x in open(f"{path}\\{file_stuff}", errors="ignore").readlines()
                    if x.strip()
                ]:
                 for i in re.findall(normal_regex, line):
                    try:
                        if is_base64(i):
                            decoded_token = base64.b64decode(add_padding(i)).decode("utf-8")
                            all_tokens.append(decoded_token)
                    except (UnicodeDecodeError, binascii.Error):
                        print(f"{i}")

    if os.path.exists(roaming + "\\Mozilla\\Firefox\\Profiles"):
        for path, dirs, files in os.walk(roaming + "\\Mozilla\\Firefox\\Profiles"):
            for new_file in files:
                if not new_file.endswith(".sqlite"):
                    continue
                for line in [
                    x.strip()
                    for x in open(f"{path}\\{new_file}", errors="ignore").readlines()
                    if x.strip()
                ]:
                    for token in re.findall(encrypt_regex, line):
                        all_tokens.append(token)
    working = []
    for token in [*set(all_tokens)]:
        url = "https://discord.com/api/v9/users/@me"
        r = requests.get(url, headers={"Authorization": token})
        if r.status_code == 200:
            working.append(token)
    return working