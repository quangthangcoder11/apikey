



from pathlib import Path
import subprocess
import sys
import json
import time
import re
import random
import threading
import queue
import os
import socket
import base64
import marshal
import uuid
from datetime import datetime, timezone
try:
    import winreg
except ImportError:
    winreg = None
from concurrent.futures import ThreadPoolExecutor
try:
    import httpx
    from bs4 import BeautifulSoup
except Exception:
    httpx = None
    BeautifulSoup = None

try:
    import requests
except Exception:
    requests = None

try:
    import tls_client
except Exception:
    tls_client = None
HotmailGraphClient = None
decorateDisplayName = None
check_token = None
try:
    from pystyle import Colorate, Colors, Center
except ImportError:
    Colorate = None
    Colors = None
    Center = None
try:
    import pyperclip
except ImportError:
    pyperclip = None
try:
    import pyautogui
except ImportError:
    pyautogui = None
try:
    import keyboard
except ImportError:
    keyboard = None
browserRotationList = []
isRotationMode = False
tgian = time.strftime("%H:%M:%S")
askEach: bool = True
warpStatus: bool = False
lastToggledAccount: int = 0
tgian = time.strftime("%H:%M:%S")
pythonver = ".".join(map(str, sys.version_info[:3]))
author = "Hoang Gia Kiet"
version = "6.1"
facebook = "https://www.facebook.com/hoanggiakiet.it"
discord = "https://discord.gg/thick1minh"
zalo = "+84382073843"
inviteUrlsGlobal: list[str] = []
browserExePath: str = ""
tokenSaveFilename: str = "tokens.txt"
selectedBrowser: str = "firefox" 
edgePrivateWindowOpened: bool = False

PROGRAMSTARTTS = time.time()

class client:
    def __init__(self, token=None):
        self.token = token
        if tls_client:
            self.sess = tls_client.Session(client_identifier='chrome_120')
        else:
            self.sess = None
        self.headers = {
            'Accept': '*/*',
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
            'X-Super-Properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MTczIiwib3NfdmVyc2lvbiI6IjEwLjAuMjYxMDAiLCJvc19hcmNoIjoieDY0IiwiYXBwX2FyY2giOiJ4NjQiLCJzeXN0ZW1fbG9jYWxlIjoiZW4tVVMiLCJicm93c2VyX3VzZXJfYWdlbnQiOiJNb3ppbGxhLzUuMCAoV2luZG93cyBOVCAxMC4wOyBXaW42NDsgeDY0KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBkaXNjb3JkLzEuMC45MTczIENocm9tZS8xMjguMC42NjEzLjE4NiBFbGVjdHJvbi8zMi4yLjIgU2FmYXJpLzUzNy4zNiIsImJyb3dzZXJfdmVyc2lvbiI6IjMyLjIuMiIsIm9zX3Nka192ZXJzaW9uIjoiMjYxMDAiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjozNTE2NjIsIm5hdGl2ZV9idWlsZF9udW1iZXIiOjU1OTkzLCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ=='
        }
        self.cookies = {'locale': 'en-US'}

class thread:
    def __init__(self, thread_amt, func, tokens, args):
        self.maxworkers = int(thread_amt)
        self.func = func
        self.tokens = tokens
        self.args = args
        self.work()
    def work(self):
        with ThreadPoolExecutor(max_workers=self.maxworkers) as exe:
            for token in self.tokens:
                args = [token] + self.args
                exe.submit(self.func, *args)

class setbio:
    def __init__(self):
        self.newbio = None
    def change(self, token, bio=None):
        if not tls_client:
            return False
        cl = client(token)
        cl.headers['Authorization'] = token
        payload = {'bio': bio or ''}
        try:
            r = cl.sess.patch(
                'https://discord.com/api/v10/users/@me/profile',
                headers=cl.headers,
                cookies=cl.cookies,
                json=payload
            )
            if r.status_code == 200:
                return True
        except Exception:
            pass
        return False

class pronouns:
    def __init__(self):
        self.newpron = None
    def change(self, token, pronouns=None):
        if not tls_client:
            return False
        cl = client(token)
        cl.headers['Authorization'] = token
        payload = {'pronouns': pronouns or ''}
        try:
            r = cl.sess.patch(
                'https://discord.com/api/v10/users/@me/profile',
                headers=cl.headers,
                cookies=cl.cookies,
                json=payload
            )
            if r.status_code == 200:
                return True
        except Exception:
            pass
        return False

def loadBioFromFile() -> str:
    try:
        if getattr(sys, 'frozen', False):
            scriptDir = Path(sys.executable).parent
        else:
            scriptDir = Path(__file__).resolve().parent
            
        bio_file = scriptDir / "other" / "bio.txt"
        if bio_file.exists():
            with bio_file.open("r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    return content
    except Exception:
        pass
    return ""

def loadPronounsFromFile() -> str:
    try:
        if getattr(sys, 'frozen', False):
            scriptDir = Path(sys.executable).parent
        else:
            scriptDir = Path(__file__).resolve().parent
            
        pronouns_file = scriptDir / "other" / "pronouns.txt"
        if pronouns_file.exists():
            with pronouns_file.open("r", encoding="utf-8") as f:
                lines = [line.strip() for line in f.readlines() if line.strip()]
                if lines:
                    return random.choice(lines)
    except Exception:
        pass
    return ""

def isVpnEnabled() -> bool:
    try:
        if getattr(sys, 'frozen', False):
            scriptDir = Path(sys.executable).parent
        else:
            scriptDir = Path(__file__).resolve().parent
            
        config_file = scriptDir / "config.json"
        if config_file.exists():
            with config_file.open("r", encoding="utf-8") as f:
                config_data = json.load(f)
                vpn_enabled = config_data.get("vpns", "true")
                if isinstance(vpn_enabled, str):
                    vpn_enabled = vpn_enabled.strip()
                    if not vpn_enabled:
                        return True
                    if vpn_enabled.lower() in ("false", "0", "no", "off"):
                        return False
                    return True
                else:
                    return bool(vpn_enabled)
        return True 
    except Exception:
        return True 

def setTokenBioAndPronouns(token: str) -> None:
    try:
        if not tls_client:
            print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Thiếu thư viện tls_client, bỏ qua set bio/pronouns"))
            return
        if getattr(sys, 'frozen', False):
            scriptDir = Path(sys.executable).parent
        else:
            scriptDir = Path(__file__).resolve().parent
            
        config_file = scriptDir / "config.json"
        set_bio_enabled = False
        set_pronouns_enabled = False
        
        if config_file.exists():
            try:
                with config_file.open("r", encoding="utf-8") as f:
                    config_data = json.load(f)
                    set_bio_enabled = config_data.get("setBio", "false")
                    set_pronouns_enabled = config_data.get("setPronouns", "false")
                    if isinstance(set_bio_enabled, str):
                        set_bio_enabled = set_bio_enabled.lower() in ("true", "1", "yes", "on")
                    else:
                        set_bio_enabled = bool(set_bio_enabled)
                        
                    if isinstance(set_pronouns_enabled, str):
                        set_pronouns_enabled = set_pronouns_enabled.lower() in ("true", "1", "yes", "on")
                    else:
                        set_pronouns_enabled = bool(set_pronouns_enabled)
            except Exception as e:
                print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Lỗi đọc config: {e}"))
                return
        
        if not set_bio_enabled and not set_pronouns_enabled:
            print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Set bio/pronouns đã tắt trong config"))
            return
            
        bio_text = ""
        pronouns_text = ""
        
        if set_bio_enabled:
            bio_text = loadBioFromFile()
        if set_pronouns_enabled:
            pronouns_text = loadPronounsFromFile()
        
        if bio_text or pronouns_text:
            bio_setter = setbio()
            pronouns_setter = pronouns()
            if set_bio_enabled and bio_text:
                print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Đang set bio cho token..."))
                if bio_setter.change(token, bio_text):
                    print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Đã set bio: \"{bio_text}\""))
                else:
                    print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Không thể set bio"))
            elif set_bio_enabled and not bio_text:
                print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Không có bio để set"))
            if set_pronouns_enabled and pronouns_text:
                print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Đang set pronouns cho token..."))
                if pronouns_setter.change(token, pronouns_text):
                    print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Đã set pronouns: \"{pronouns_text}\""))
                else:
                    print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Không thể set pronouns"))
            elif set_pronouns_enabled and not pronouns_text:
                print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Không có pronouns để set"))
        else:
            print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Không có bio/pronouns để set"))
        
        set_guild_tag_enabled = False
        guild_tag_link = ""
        
        if config_file.exists():
            try:
                with config_file.open("r", encoding="utf-8") as f:
                    config_data = json.load(f)
                    set_guild_tag_enabled = config_data.get("setGuildTag", "false")
                    guild_tag_link = config_data.get("linkGuildTagServer", "")
                    
                    if isinstance(set_guild_tag_enabled, str):
                        set_guild_tag_enabled = set_guild_tag_enabled.lower() in ("true", "1", "yes", "on")
                    else:
                        set_guild_tag_enabled = bool(set_guild_tag_enabled)
            except Exception as e:
                print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Lỗi đọc config cho guild tag: {e}"))
        
        if set_guild_tag_enabled and guild_tag_link:
            try:
                print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Đang set guild tag cho token..."))
                guild_id = getGuildIdFromInvite(guild_tag_link)
                if guild_id:
                    setGuildTag(token, guild_id, guild_tag_link)
                else:
                    print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Không thể lấy guild ID từ link: {guild_tag_link}"))
            except Exception as e:
                print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Lỗi khi set guild tag: {e}"))
            
    except Exception as e:
        print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Lỗi khi set bio/pronouns: {e}"))

def getServerNameFromInvite(invite_code: str) -> str:
    try:
        if not tls_client:
            return "Unknown"
        
        cl = client()
        
        r = cl.sess.get(
            f'https://discord.com/api/v10/invites/{invite_code}',
            headers=cl.headers,
            cookies=cl.cookies
        )
        
        if r.status_code == 200:
            data = r.json()
            guild_name = data.get('guild', {}).get('name', 'Unknown')
            return guild_name
        else:
            return "Unknown"
    except Exception:
        return "Unknown"

def getGuildIdFromInvite(invite_link: str) -> str | None:
    try:
        if not invite_link:
            return None
        
        invite_code = invite_link.split('/')[-1]
        if not invite_code:
            return None
        
        if not tls_client:
            if requests:
                cl = requests.Session()
                headers = {
                    'Accept': '*/*',
                    'Content-Type': 'application/json',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'
                }
                r = cl.get(
                    f'https://discord.com/api/v10/invites/{invite_code}?inputValue={invite_code}',
                    headers=headers,
                    timeout=10
                )
            else:
                return None
        else:
            cl = client()
            r = cl.sess.get(
                f'https://discord.com/api/v10/invites/{invite_code}?inputValue={invite_code}',
                headers=cl.headers,
                cookies=cl.cookies
            )
        
        if r.status_code == 200:
            try:
                if hasattr(r, 'json'):
                    data = r.json()
                elif hasattr(r, 'text'):
                    data = json.loads(r.text)
                else:
                    return None
                guild_id = data.get('guild', {}).get('id')
                return str(guild_id) if guild_id else None
            except Exception:
                return None
        else:
            return None
    except Exception:
        return None

class joiner:
    def __init__(self):
        self.invite = None
        self.serverid = None
        self.servername = None
        self.invchannelid = None
        self.invchanneltype = None

    def extract_invite(self, invite):
        try:
            match = re.search(r'(?:(?:http:\/\/|https:\/\/)?discord\.gg\/|discordapp\.com\/invite\/|discord\.com\/invite\/)?([a-zA-Z0-9-]+)', invite)
            if match:
                invite = match.group(1)
            return invite
        except Exception:
            return invite

    def get_invite_info(self, invite_code, token=None):
        try:
            if not tls_client:
                if not requests:
                    return {}
                headers = {
                    'Accept': '*/*',
                    'Content-Type': 'application/json',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'
                }
                if token:
                    headers['Authorization'] = token
                r = requests.get(
                    f'https://discord.com/api/v10/invites/{invite_code}?inputValue={invite_code}',
                    headers=headers,
                    timeout=10
                )
            else:
                cl = client()
                if token:
                    cl.headers['Authorization'] = token
                r = cl.sess.get(
                    f'https://discord.com/api/v10/invites/{invite_code}?inputValue={invite_code}',
                    headers=cl.headers,
                    cookies=cl.cookies
                )
            
            if r.status_code == 200:
                try:
                    if hasattr(r, 'json'):
                        return r.json()
                    elif hasattr(r, 'text'):
                        return json.loads(r.text)
                except Exception:
                    pass
            return {}
        except Exception:
            return {}

    def join(self, token, invite_link=None):
        try:
            if not invite_link:
                invite_link = self.invite
            if not invite_link:
                return False
            
            invite_code = self.extract_invite(invite_link)
            if not invite_code:
                return False
            
            if not tls_client and not requests:
                print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Thiếu thư viện tls_client hoặc requests, bỏ qua join server"))
                return False
            
            if not self.serverid or not self.invchannelid:
                invinfo = self.get_invite_info(invite_code, token)
                if invinfo:
                    self.serverid = invinfo.get('guild', {}).get('id')
                    self.servername = invinfo.get('guild', {}).get('name', 'Unknown Server')
                    self.invchannelid = invinfo.get('channel', {}).get('id')
                    self.invchanneltype = invinfo.get('channel', {}).get('type')
            
            if not self.serverid or not self.invchannelid:
                print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Không thể lấy thông tin server từ invite"))
                return False
            
            if tls_client:
                cl = client(token)
                cl.headers['Authorization'] = token
            else:
                if not requests:
                    return False
                cl = None
            
            payload = {
                'session_id': uuid.uuid4().hex,
            }
            
            xcontent = {
                'location': 'Join Guild',
                'location_guild_id': self.serverid,
                'location_channel_id': self.invchannelid,
                'location_channel_type': self.invchanneltype
            }
            xcontent = json.dumps(xcontent)
            xcontent = xcontent.encode('utf-8')
            xcontent = base64.b64encode(xcontent).decode('utf-8')
            
            if tls_client:
                cl.headers['X-Context-Properties'] = xcontent
                cl.headers['Content-Type'] = 'application/json'
                cl.headers['Accept'] = '*/*'
                
                response = cl.sess.post(
                    f'https://discord.com/api/v10/invites/{invite_code}',
                    headers=cl.headers,
                    cookies=cl.cookies,
                    json=payload
                )
            else:
                headers = {
                    'Authorization': token,
                    'Content-Type': 'application/json',
                    'Accept': '*/*',
                    'X-Context-Properties': xcontent,
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'
                }
                response = requests.post(
                    f'https://discord.com/api/v10/invites/{invite_code}',
                    headers=headers,
                    json=payload,
                    timeout=10
                )
            
            try:
                if hasattr(response, 'json'):
                    response_data = response.json()
                elif hasattr(response, 'text'):
                    response_data = json.loads(response.text) if response.text else {}
                else:
                    response_data = {}
                response_text = response.text if hasattr(response, 'text') else str(response_data)
            except Exception:
                response_data = {}
                response_text = str(response.status_code)
            
            if response.status_code == 200:
                print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Đã join server thành công: {self.servername[:30] if self.servername else 'Unknown'} ({self.serverid})"))
                time.sleep(1)
                return True, False
            elif 'retry_after' in response_text:
                try:
                    limit = response_data.get('retry_after', 1.5)
                    print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Rate limit, đợi {limit}s..."))
                    time.sleep(float(limit))
                    return self.join(token, invite_link)
                except Exception:
                    return False, False
            elif 'Cloudflare' in response_text:
                print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Bị Cloudflare block, thử lại sau 5s..."))
                time.sleep(5)
                return self.join(token, invite_link)
            elif 'captcha_key' in response_text:
                print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Phát hiện HCAPTCHA, sẽ mở trình duyệt để join thủ công"))
                return False, True
            elif 'You need to verify' in response_text or response.status_code == 403:
                print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Token cần verify hoặc không có quyền join server"))
                return False, False
            else:
                error_msg = response_data.get('message', f'Status code: {response.status_code}')
                print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Không thể join server: {error_msg}"))
                return False, False
                
        except Exception as e:
            print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Lỗi khi join server: {e}"))
            return False, False

def setGuildTag(token: str, guild_id: str, invite_link: str = None) -> bool:
    try:
        if not tls_client and not requests:
            print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Thiếu thư viện tls_client hoặc requests, bỏ qua set guild tag"))
            return False
        
        headers = {
            "Authorization": token,
            "Content-Type": "application/json",
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.607 Chrome/134.0.6998.179 Electron/35.1.5 Safari/537.36",
            "Origin": "https://canary.discord.com",
            "Referer": "https://canary.discord.com/discovery/quests",
        }
        
        if tls_client:
            cl = client(token)
            cl.headers['Authorization'] = token
            cl.headers.update(headers)
            
            response = cl.sess.get(
                'https://discord.com/api/v9/users/@me/guilds',
                headers=cl.headers,
                cookies=cl.cookies
            )
        else:
            if not requests:
                return False
            response = requests.get(
                'https://discord.com/api/v9/users/@me/guilds',
                headers=headers,
                timeout=10
            )
        
        if response.status_code != 200:
            print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Lỗi khi lấy guilds: {response.status_code}"))
            return False
        
        try:
            if hasattr(response, 'json'):
                guilds = response.json()
            elif hasattr(response, 'text'):
                guilds = json.loads(response.text)
            else:
                guilds = []
        except Exception:
            guilds = []
        
        target_guild = None
        for guild in guilds:
            if str(guild.get("id", "")) == str(guild_id):
                target_guild = guild
                break
        
        if not target_guild:
            if invite_link:
                print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Token chưa join server, đang join server trước..."))
                joiner_instance = joiner()
                joiner_instance.invite = invite_link
                success, hcaptcha_detected = joiner_instance.join(token, invite_link)
                
                if hcaptcha_detected:
                    print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Phát hiện HCAPTCHA, mở trình duyệt để join thủ công..."))
                    _open_browser_for_join(invite_link)
                    print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Đã join server thủ công, đang tắt trình duyệt..."))
                    _kill_browser_processes()
                    print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Sau khi join xong, sẽ tiếp tục set guild tag..."))
                    time.sleep(2)
                    
                    if tls_client:
                        cl = client(token)
                        cl.headers['Authorization'] = token
                        cl.headers.update(headers)
                        response = cl.sess.get(
                            'https://discord.com/api/v9/users/@me/guilds',
                            headers=cl.headers,
                            cookies=cl.cookies
                        )
                    else:
                        if not requests:
                            return False
                        response = requests.get(
                            'https://discord.com/api/v9/users/@me/guilds',
                            headers=headers,
                            timeout=10
                        )
                    
                    if response.status_code == 200:
                        try:
                            if hasattr(response, 'json'):
                                guilds = response.json()
                            elif hasattr(response, 'text'):
                                guilds = json.loads(response.text)
                            else:
                                guilds = []
                        except Exception:
                            guilds = []
                        
                        for guild in guilds:
                            if str(guild.get("id", "")) == str(guild_id):
                                target_guild = guild
                                break
                    
                    if not target_guild:
                        print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Token vẫn chưa join server sau khi mở trình duyệt"))
                        return False
                elif success:
                    print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Đã join server thành công, đang tắt trình duyệt..."))
                    _kill_browser_processes()
                    time.sleep(2)
                    if tls_client:
                        cl = client(token)
                        cl.headers['Authorization'] = token
                        cl.headers.update(headers)
                        response = cl.sess.get(
                            'https://discord.com/api/v9/users/@me/guilds',
                            headers=cl.headers,
                            cookies=cl.cookies
                        )
                    else:
                        if not requests:
                            return False
                        response = requests.get(
                            'https://discord.com/api/v9/users/@me/guilds',
                            headers=headers,
                            timeout=10
                        )
                    
                    if response.status_code == 200:
                        try:
                            if hasattr(response, 'json'):
                                guilds = response.json()
                            elif hasattr(response, 'text'):
                                guilds = json.loads(response.text)
                            else:
                                guilds = []
                        except Exception:
                            guilds = []
                        
                        for guild in guilds:
                            if str(guild.get("id", "")) == str(guild_id):
                                target_guild = guild
                                break
                    
                    if not target_guild:
                        print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Không thể join server hoặc server không tồn tại"))
                        if invite_link:
                            print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Mở trình duyệt để join thủ công..."))
                            _open_browser_for_join(invite_link)
                            _kill_browser_processes()
                            time.sleep(2)
                            
                            if tls_client:
                                cl = client(token)
                                cl.headers['Authorization'] = token
                                cl.headers.update(headers)
                                response = cl.sess.get(
                                    'https://discord.com/api/v9/users/@me/guilds',
                                    headers=cl.headers,
                                    cookies=cl.cookies
                                )
                            else:
                                if not requests:
                                    return False
                                response = requests.get(
                                    'https://discord.com/api/v9/users/@me/guilds',
                                    headers=headers,
                                    timeout=10
                                )
                            
                            if response.status_code == 200:
                                try:
                                    if hasattr(response, 'json'):
                                        guilds = response.json()
                                    elif hasattr(response, 'text'):
                                        guilds = json.loads(response.text)
                                    else:
                                        guilds = []
                                except Exception:
                                    guilds = []
                                
                                for guild in guilds:
                                    if str(guild.get("id", "")) == str(guild_id):
                                        target_guild = guild
                                        break
                            
                            if not target_guild:
                                print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Token vẫn chưa join server sau khi mở trình duyệt"))
                                return False
                        else:
                            return False
                else:
                    if invite_link:
                        print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Không thể join server qua API, mở trình duyệt để join thủ công..."))
                        _open_browser_for_join(invite_link)
                        _kill_browser_processes()
                        print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Sau khi join xong, sẽ tiếp tục set guild tag..."))
                        time.sleep(2)
                        
                        if tls_client:
                            cl = client(token)
                            cl.headers['Authorization'] = token
                            cl.headers.update(headers)
                            response = cl.sess.get(
                                'https://discord.com/api/v9/users/@me/guilds',
                                headers=cl.headers,
                                cookies=cl.cookies
                            )
                        else:
                            if not requests:
                                return False
                            response = requests.get(
                                'https://discord.com/api/v9/users/@me/guilds',
                                headers=headers,
                                timeout=10
                            )
                        
                        if response.status_code == 200:
                            try:
                                if hasattr(response, 'json'):
                                    guilds = response.json()
                                elif hasattr(response, 'text'):
                                    guilds = json.loads(response.text)
                                else:
                                    guilds = []
                            except Exception:
                                guilds = []
                            
                            for guild in guilds:
                                if str(guild.get("id", "")) == str(guild_id):
                                    target_guild = guild
                                    break
                        
                        if not target_guild:
                            print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Token vẫn chưa join server sau khi mở trình duyệt"))
                            return False
                    else:
                        print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Không thể join server và không có invite link, bỏ qua set guild tag"))
                        return False
            else:
                print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Token không ở trong server với ID: {guild_id}"))
                return False
        
        if "GUILD_TAGS" not in target_guild.get("features", []):
            print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Server này không có guild tag"))
            return False
        
        payload = {
            "identity_guild_id": guild_id,
            "identity_enabled": True
        }
        
        if tls_client:
            cl = client(token)
            cl.headers['Authorization'] = token
            cl.headers.update(headers)
            
            put_response = cl.sess.put(
                "https://discord.com/api/v9/users/@me/clan",
                headers=cl.headers,
                cookies=cl.cookies,
                json=payload
            )
        else:
            if not requests:
                return False
            put_response = requests.put(
                "https://discord.com/api/v9/users/@me/clan",
                headers=headers,
                json=payload,
                timeout=10
            )
        
        if put_response.status_code == 200:
            guild_name = target_guild.get("name", "Unknown")
            print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Đã set guild tag thành công: {guild_name} ({guild_id})"))
            return True
        elif put_response.status_code == 403:
            print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Server cần verify, hãy verify trước"))
            return False
        else:
            guild_name = target_guild.get("name", "Unknown")
            print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Lỗi khi set guild tag: {guild_name} ({guild_id}): {put_response.status_code}"))
            return False
            
    except Exception as e:
        print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Lỗi khi set guild tag: {e}"))
        return False

def saveInviteLinks(links: list) -> None:
    try:
        if getattr(sys, 'frozen', False):
            scriptDir = Path(sys.executable).parent
        else:
            scriptDir = Path(__file__).resolve().parent
            
        config_file = scriptDir / "config.json"
        
        if config_file.exists():
            with config_file.open("r", encoding="utf-8") as f:
                config_data = json.load(f)
        else:
            config_data = {}
        
        existing_links = config_data.get("savedInviteLinks", [])
        
        for link in links:
            invite_code = link.split('/')[-1]
            server_name = getServerNameFromInvite(invite_code)
            
            link_exists = False
            for existing_link in existing_links:
                if existing_link.get('link') == link:
                    link_exists = True
                    break
            
            if not link_exists:
                existing_links.append({
                    "link": link,
                    "server_name": server_name,
                    "invite_code": invite_code,
                    "type": "single"
                })
        
        config_data["savedInviteLinks"] = existing_links
        
        with config_file.open("w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)
            
    except Exception as e:
        print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Lỗi khi lưu invite links: {e}"))

def saveInviteLinksWithType(links: list) -> None:
    try:
        if getattr(sys, 'frozen', False):
            scriptDir = Path(sys.executable).parent
        else:
            scriptDir = Path(__file__).resolve().parent
            
        config_file = scriptDir / "config.json"
        
        if config_file.exists():
            with config_file.open("r", encoding="utf-8") as f:
                config_data = json.load(f)
        else:
            config_data = {}
        
        config_data["savedInviteLinks"] = links
        
        with config_file.open("w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)
            
    except Exception as e:
        print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Lỗi khi lưu invite links: {e}"))

def loadSavedInviteLinks() -> list:
    try:
        if getattr(sys, 'frozen', False):
            scriptDir = Path(sys.executable).parent
        else:
            scriptDir = Path(__file__).resolve().parent
            
        config_file = scriptDir / "config.json"
        
        if config_file.exists():
            with config_file.open("r", encoding="utf-8") as f:
                config_data = json.load(f)
                links = config_data.get("savedInviteLinks", [])
                
                for link in links:
                    if 'type' not in link:
                        link['type'] = 'single'
                
                return links
        return []
    except Exception:
        return []

def checkTokenInfo(token: str) -> None:
    try:
        if not tls_client:
            print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Thiếu thư viện tls_client, bỏ qua kiểm tra token"))
            return
        
        cl = client(token)
        cl.headers['Authorization'] = token
        
        try:
            r = cl.sess.get(
                'https://discord.com/api/v10/users/@me',
                headers=cl.headers,
                cookies=cl.cookies
            )
            
            if r.status_code == 200:
                user_data = r.json()
                
                username = user_data.get('username', 'N/A')
                discriminator = user_data.get('discriminator', 'N/A')
                display_name = user_data.get('global_name', 'N/A')
                
                flags = user_data.get('flags', 0)
                verified = user_data.get('verified', False)
                phone = user_data.get('phone', None)
                
                user_info = f"{username}#{discriminator}"
                if display_name and display_name != username:
                    user_info += f" ({display_name})"
                
                print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» User: {user_info}"))
                
                try:
                    is_mode_2 = len(inviteUrlsGlobal) > 0
                    if is_mode_2:
                        r = cl.sess.get(
                            'https://discord.com/api/v10/users/@me/guilds',
                            headers=cl.headers,
                            cookies=cl.cookies
                        )
                        
                        if r.status_code == 200:
                            guilds_data = r.json()
                            guild_count = len(guilds_data)
                            if guild_count > 0:
                                server_names = [guild.get('name', 'Unknown') for guild in guilds_data]
                                servers_text = ', '.join(server_names)
                                print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Server: {servers_text}"))
                            else:
                                print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Server: None"))
                        else:
                            print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Server: ERROR"))
                except Exception:
                    pass
                
                flag_messages = []
                warning_flags = []
                
                if flags & 1:
                    flag_messages.append("Discord Employee")
                if flags & 2:
                    flag_messages.append("Partnered Server Owner")
                if flags & 4:
                    flag_messages.append("HypeSquad Events")
                if flags & 8:
                    flag_messages.append("Bug Hunter Level 1")
                if flags & 64:
                    flag_messages.append("House Bravery")
                if flags & 128:
                    flag_messages.append("House Brilliance")
                if flags & 256:
                    flag_messages.append("House Balance")
                if flags & 512:
                    flag_messages.append("Early Supporter")
                if flags & 16384:
                    flag_messages.append("Bug Hunter Level 2")
                if flags & 131072:
                    flag_messages.append("Verified Developer")
                if flags & 4194304:
                    flag_messages.append("Active Developer")
                
                if flags & 1048576:
                    warning_flags.append("SPAMMER FLAG")
                if flags & 2097152:
                    warning_flags.append("DISABLE_PREMIUM FLAG")
                
                if warning_flags:
                    print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Flags: WARNING - {', '.join(warning_flags)}"))
                elif flag_messages:
                    print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Flags: {', '.join(flag_messages)}"))
                else:
                    print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Flags: None"))
                
                if phone:
                    print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Phone: Verified"))
                elif verified:
                    print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Phone: Not verified (Email verified)"))
                else:
                    print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Phone: Not verified (Email not verified)"))
                
            elif r.status_code == 401:
                print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Token: DIE"))
            else:
                print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Token: ERROR ({r.status_code})"))
                
        except Exception as e:
            print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Lỗi khi kiểm tra token: {e}"))
            
    except Exception as e:
        print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Lỗi khi kiểm tra thông tin token: {e}"))

def formatUptime() -> str:
    try:
        elapsed = int(time.time() - PROGRAMSTARTTS)
        hours, rem = divmod(elapsed, 3600)
        mins, secs = divmod(rem, 60)
        if hours > 0:
            return f"{hours:02d}:{mins:02d}:{secs:02d}"
        return f"{mins:02d}:{secs:02d}"
    except Exception:
        return "00:00"

def consoletitle(title: str) -> None:
    try:
        if os.name == "nt":
            try:
                import ctypes
                ctypes.windll.kernel32.SetConsoleTitleW(title)
            except Exception:
                os.system(f"title {title}")
        else:
            try:
                sys.stdout.write(f"\33]0;{title}\a")
                sys.stdout.flush()
            except Exception:
                pass
    except Exception:
        pass

def uptimeTitle() -> None:
    verTitle = f"v{version}"
    while True:
        try:
            consoletitle(f"Uptime: {formatUptime()} | {verTitle} ")
        except Exception:
            pass
        time.sleep(1)

def startUptimeTitle() -> None:
    try:
        threading.Thread(target=uptimeTitle, daemon=True).start()
    except Exception:
        pass

mầu = [
    Colors.DynamicMIX([Colors.cyan, Colors.white, Colors.pink])
]

mauu = random.choice(mầu)
def màu(text: str) -> str:
    if Colorate and Colors:
        try:
            return Colorate.Horizontal(mauu, text)
        except Exception:
            return text
    return text
Icon = [
    "⭐","✨","🌟","💫","🔥","⚡","💥","🌈","❄️","☄️","🌪️","🌊","💎","🧿","🔮","🪄",
    "🎯","🚀","🌀","🌙","🍀","🎉","🧩","🛡️","🧠","💡","🎭","💭","🫧","🪩",
    "❤️","🧡","💛","💚","💙","💜","🖤","🤍","🤎","💖","💗","💓","💞","💕","💘","💝","💟",
    "💔","💌","💋","💑","💏","💍","💎",
    "🌸","🌺","🌻","🌼","🌷","🌹","🌱","🌿","🍃","🍁","🌾","🌵","🪴","🪷","🪻","💐","🏵️",
    "🌲","🌳","🌴","🌹‍🌾","🌷‍🌾","🌸‍🌾",
    "🍎","🍏","🍐","🍊","🍋","🍌","🍉","🍇","🍓","🫐","🍈","🍒","🍑","🥭","🍍","🥥",
    "🥝","🍅","🍆","🥑","🥦","🥬","🥕","🌽","🧄","🧅","🍠","🥔",
    "🍞","🥐","🥖","🥯","🥞","🧇","🧀","🍖","🍗","🥩","🍔","🍟","🍕",
    "🌭","🥪","🌮","🌯","🥙","🧆","🍳","🥚","🍚","🍛","🍜","🍝","🍣",
    "🍤","🍱","🥗","🥣","🍲","🍥","🍡","🍢","🍦","🍧","🍨","🍩","🍪",
    "🎂","🍰","🧁","🍫","🍬","🍭","🍮","🍯","🧃","🥤","🧋","☕","🍵","🍾","🍷","🍸","🍹","🍺","🍻",
    "🐶","🐱","🐭","🐹","🐰","🦊","🐻","🐼","🐨","🐯","🦁","🐮","🐷","🐸","🐵",
    "🐔","🐧","🐦","🕊️","🦅","🦆","🦢","🦉","🦩","🦚","🦜","🦇",
    "🐺","🐗","🐴","🦄","🐝","🐞","🪲","🪳","🕷️","🕸️","🐢","🐍","🦎",
    "🐙","🦑","🦐","🦞","🦀","🐡","🐠","🐟","🐬","🐳","🐋","🦈","🪼",
    "🐊","🦧","🦍","🦓","🦒","🦘","🦥","🦦","🦨","🦡","🐘","🦏","🦛",
    "🐪","🐫","🦙","🦌","🐃","🐄","🐏","🐑","🐖","🐐","🐓","🦃","🐕‍🦺","🐈‍⬛",
    "🚗","🚕","🚙","🛻","🚓","🚑","🚒","🚐","🚚","🚛","🚜","🏎️","🏍️","🛵","🚲",
    "🛴","🛹","🛼","🚂","🚆","🚄","🚅","🚈","🚊","🚝","🚋","🚎",
    "🚌","🚍","🚉","🚠","🚡","🚟","✈️","🛫","🛬","🚁","🛩️","🚀","🛸","🛰️","🚤","⛵","🛶","🚢",
    "🗿","🏰","🏯","🏠","🏡","🏙️","🌆","🌇","🗽","🗼","🪩","💈","🎡","🎢","🎠","⛩️",
    "🎵","🎶","🎼","🎤","🎧","🎷","🎸","🎺","🎻","🥁","🎹","🎭","🎨","🩰","🎬","🎮","🎰","🎲",
    "💻","🖥️","🖱️","📱","⌚","📷","🎥","📸","📹","💾","💿","📀","🕹️","📡",
    "🪫","🔋","🔌","💡","🔦","🪔","🔮","🧿","⚙️","🧰","🧱","🔧","🔩","🔨","⚒️","🪓",
    "🌌","🌠","🪐","🌞","🌜","🌛","☀️","🌤️","🌧️","🌈","🌩️","🌊","🌫️"
]

def randomIcon() -> str:
    try:
        return random.choice(Icon)
    except Exception:
        return ""

def normalizeStyle(style: str | None) -> str:
    try:
        if not style:
            return "both"
        s = style.strip().lower()
        if s in ("both", "prefix", "suffix"):
            return s
        if s in ("truoc ten", "truoc_ten", "dau", "truoc", "trước tên"):
            return "prefix"
        if s in ("sau ten", "sau_ten", "cuoi", "sau", "sau tên"):
            return "suffix"
        if s in ("hai ben", "hai_ben", "cahai", "cả hai", "hai phía", "ca hai"):
            return "both"
        return "both"
    except Exception:
        return "both"

def decorateDisplayName(name: str, style: str | None = None) -> str:
    try:
        icon = randomIcon()
        if not icon:
            return name
        norm = normalizeStyle(style)
        if norm == "prefix":
            return f"{icon} {name}"
        if norm == "suffix":
            return f"{name} {icon}"
        return f"{icon} {name} {icon}"
    except Exception:
        return name

def isExeMode() -> bool:
    return getattr(sys, 'frozen', False)

def getScriptDir() -> Path:
    if isExeMode():
        return Path(sys.executable).parent
    else:
        return Path(__file__).resolve().parent

def getSystemDeviceId() -> str:
    try:
        if os.name == "nt":
            try:
                import winreg
                key_sqm = winreg.OpenKey(
                    winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\SQMClient", 0, winreg.KEY_READ
                )
                device_id_tuple = winreg.QueryValueEx(key_sqm, "MachineId")
                winreg.CloseKey(key_sqm)
                clean_id = device_id_tuple[0].replace('{', '').replace('}', '').strip()
                return clean_id
            except Exception:
                pass
    except Exception:
        pass
    return ""

def getSystemProductId() -> str:
    try:
        if os.name == "nt":
            try:
                import winreg
                key_win = winreg.OpenKey(
                    winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion", 0, winreg.KEY_READ
                )
                product_id_tuple = winreg.QueryValueEx(key_win, "ProductId")
                winreg.CloseKey(key_win)
                return product_id_tuple[0].strip()
            except Exception:
                pass
    except Exception:
        pass
    return ""

def loadEncryptedModule(module_name: str):
    try:
        scriptDir = getScriptDir()
        modulePath = scriptDir / "modules" / f"{module_name}.py"
        
        if not modulePath.exists():
            print(màu(f"[>] Không tìm thấy module: {module_name}.py"))
            return None
        try:
            if module_name == "hotmail":
                from modules.hotmail import HotmailGraphClient
                return HotmailGraphClient
        except ImportError:
            pass
        import importlib.util
        spec = importlib.util.spec_from_file_location(module_name, modulePath)
        if spec is None:
            return None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if module_name == "hotmail":
            return getattr(module, "HotmailGraphClient", None)
        if module_name == "apimail":
            return getattr(module, "TempmailClient", None)
        
            
        return module
        
    except Exception as e:
        print(màu(f"[>] Lỗi khi load module {module_name}: {e}"))
        return None

def checkModuleExists(module_name: str) -> bool:
    try:
        scriptDir = getScriptDir()
        modulePath = scriptDir / "modules" / f"{module_name}.py"
        return modulePath.exists()
    except Exception:
        return False

def getModuleInfo() -> dict:
    modules_info = {}
    module_names = ["hotmail", "rdusername", "tmail", "apimail"]
    
    for module_name in module_names:
        modules_info[module_name] = {
            "exists": checkModuleExists(module_name),
            "loaded": False
        }
    
    return modules_info

def clearScreen() -> None:
    try:
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")
    except Exception:
        pass

def getLocalIp() -> str:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
        return local_ip
    except Exception:
        return "Không xác định"

def getPublicIp() -> str:
    try:
        if httpx:
            response = httpx.get("https://api.ipify.org", timeout=5)
            if response.status_code == 200:
                return response.text.strip()
    except Exception:
        pass
    try:
        import urllib.request
        with urllib.request.urlopen("https://api.ipify.org", timeout=5) as response:
            return response.read().decode().strip()
    except Exception:
        return "Không xác định"

def getComputerName() -> str:
    try:
        if os.name == "nt":
            computer_name = os.environ.get('COMPUTERNAME', '')
            if computer_name:
                return computer_name
        return socket.gethostname()
    except Exception:
        return "Unknown"
MAIL_API_BASE = "https://tempmail.id.vn/api"
MAIL_URL_REGEX = re.compile(r"https?://[\w\-._~:/?#\[\]@!$&'()*+,;=%]+", re.IGNORECASE)
MAIL_VERIFY_URL_REGEX = re.compile(r"^https://(?:www\.)?discord\.com/verify[?#][^\s]+$", re.IGNORECASE)
MAIL_AUTH_TOKEN = None
MAIL_AUTH_EMAIL = "quangthangnehihihi@gmail.com"
MAIL_AUTH_PASSWORD = "Quangthang2007@"

def _mail_headers_json() -> dict:
    h = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    if MAIL_AUTH_TOKEN:
        h["Authorization"] = f"Bearer {MAIL_AUTH_TOKEN}"
    return h

def _mail_post(path: str, payload: dict, timeout: int = 20):
    if not requests:
        raise RuntimeError("requests library not available")
    url = f"{MAIL_API_BASE}{path}"
    return requests.post(url, json=payload, headers=_mail_headers_json(), timeout=timeout)

def _mail_get(path: str, timeout: int = 20):
    if not requests:
        raise RuntimeError("requests library not available")
    url = f"{MAIL_API_BASE}{path}"
    h = {"Accept": "application/json"}
    if MAIL_AUTH_TOKEN:
        h["Authorization"] = f"Bearer {MAIL_AUTH_TOKEN}"
    return requests.get(url, headers=h, timeout=timeout)

def _mail_auth_login(email: str, password: str):
    if not requests:
        return None
    try:
        r = requests.post(
            f"{MAIL_API_BASE}/auth/login",
            json={"email": email, "password": password},
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            timeout=20,
        )
        data = r.json()
        if not isinstance(data, dict) or not data.get("success"):
            return None
        d = data.get("data") or {}
        token = d.get("token") or d.get("access_token") or data.get("token") or data.get("access_token")
        if not token:
            return None
        return str(token)
    except Exception:
        return None

def _mail_generate_random_user() -> str:
    import string
    PREFERRED_PREFIXES = [
        "hoanggiakiet", "giakiet", "giakiethoang", "kiethoanggia", "gjakiet", "gjakjet",
        "gjakiethoang", "kietok", "giakietdev", "giakietcoder", "hoangkiet", "kietsiumanh",
        "gjakje1siuba", "gjakje1siumanh", "gjakje1hoanq", "kiethihi", "gjakje1ok",
        "hoanqgiakiet", "hoanqkiet", "hoanqkietdev", "hoanqrakietcoder", "hoanqkietok",
        "hoanqkietcoder", "kietbadao", "quangthangdev", "gjakie1siuba", "truongquangthang",
        "thangtruong", "thangdev", "thangcoder", "thangok", "giakiet07", "quangthang07"
    ]
    def generate_random_name() -> str:
        patterns = [
            lambda: "".join(random.choice(string.ascii_lowercase) for _ in range(random.randint(4, 8))) +
                str(random.randint(10, 9999)) +
                "".join(random.choice(string.ascii_lowercase) for _ in range(random.randint(2, 4))),
            lambda: str(random.randint(100, 9999)) +
                "".join(random.choice(string.ascii_lowercase) for _ in range(random.randint(5, 10))) +
                str(random.randint(10, 999)),
            lambda: "".join(random.choice(string.ascii_lowercase) for _ in range(random.randint(6, 12))),
            lambda: "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(random.randint(8, 15))),
        ]
        return random.choice(patterns)()
    if PREFERRED_PREFIXES and random.random() < 0.85:
        base = random.choice(PREFERRED_PREFIXES)
    else:
        base = generate_random_name()
    rand_len_1 = random.randint(2, 6)
    rand_len_2 = random.randint(1, 4)
    letters = string.ascii_lowercase + string.digits
    suffix1 = "".join(random.choice(letters) for _ in range(rand_len_1))
    suffix2 = "".join(random.choice(letters) for _ in range(rand_len_2))
    variants = [
        f"{base}{suffix1}{suffix2}",
        f"{base}{suffix1}",
        f"{suffix1}{base}{suffix2}",
        f"{base}{random.randint(100,9999)}{suffix2}",
        f"{base}{random.randint(10,99)}",
        f"{suffix1}{base}",
    ]
    pick = random.choice(variants)
    safe = []
    for ch in pick.lower():
        if ch.isalnum():
            safe.append(ch)
    username = "".join(safe).strip()
    if not username:
        username = "".join(random.choice(letters) for _ in range(random.randint(8, 12)))
    username = username[:20]
    if len(username) < 8:
        username += "".join(random.choice(letters) for _ in range(8 - len(username)))
    return username

def _mail_create_email(domain: str = "hoanggiakiet.com", user: str = None):
    payload = {
        "user": user or _mail_generate_random_user(),
        "domain": domain,
        "generate_guest_link": True,
        "guest_link_expiration_days": 1,
    }
    r = _mail_post("/email/create", payload)
    data = r.json()
    if not data.get("success"):
        raise RuntimeError(f"Create email failed: {data}")
    d = data.get("data") or {}
    email = d.get("email")
    ident = d.get("id")
    if not email or not ident:
        raise RuntimeError(f"Invalid create response: {data}")
    return email, int(ident)

def _mail_list_messages_by_email_id(email_id: int, page: int = 1):
    r = _mail_get(f"/email/{email_id}?page={page}")
    data = r.json()
    if not data.get("success"):
        raise RuntimeError(f"List messages failed: {data}")
    return data.get("data") or {}

def _mail_get_message(message_id: int):
    r = _mail_get(f"/message/{message_id}")
    data = r.json()
    if not data.get("success"):
        raise RuntimeError(f"Get message failed: {data}")
    return data.get("data") or {}

def _mail_collect_links_from_html_and_text(html: str, text: str):
    links = []
    try:
        if BeautifulSoup and html:
            try:
                soup = BeautifulSoup(html, "html.parser")
                for a in soup.find_all("a", href=True):
                    href = a.get("href")
                    if href and href.startswith("http"):
                        links.append(href)
            except Exception:
                pass
        links.extend(MAIL_URL_REGEX.findall(html or ""))
        links.extend(MAIL_URL_REGEX.findall(text or ""))
    except Exception:
        pass
    seen = set()
    out = []
    for lnk in links:
        if lnk not in seen:
            seen.add(lnk)
            out.append(lnk)
    return out

def _mail_extract_exact_verify_url(candidates):
    for c in candidates:
        if MAIL_VERIFY_URL_REGEX.match(c.strip()):
            return c.strip()
    return None

def _mail_resolve_click_redirect(url: str, max_hops: int = 10, timeout: int = 15) -> str:
    if not requests:
        return url
    try:
        session = requests.Session()
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        })
        current = url
        visited = set()
        for hop in range(max_hops):
            if current in visited:
                break
            visited.add(current)
            if MAIL_VERIFY_URL_REGEX.match(current):
                return current
            if current.lower().rstrip("/") == "https://discord.com" or current.lower().rstrip("/") == "http://discord.com":
                break
            try:
                r = session.get(current, allow_redirects=False, timeout=timeout)
                location = r.headers.get("Location") or r.headers.get("location")
                if location:
                    from urllib.parse import urljoin
                    if location.startswith("/"):
                        next_url = urljoin(current, location)
                    else:
                        next_url = location
                    current = next_url
                    if MAIL_VERIFY_URL_REGEX.match(current):
                        return current
                    if current.lower().rstrip("/") in ("https://discord.com", "http://discord.com"):
                        break
                    continue
                if r.status_code == 200:
                    try:
                        html = r.text or ""
                    except Exception:
                        html = ""
                    if html:
                        meta_refresh = re.search(
                            r'<meta[^>]*http-equiv=["\']refresh["\'][^>]*content=["\'][^;]*;\s*url=([^"\']+)["\']',
                            html,
                            re.IGNORECASE
                        )
                        if meta_refresh:
                            from urllib.parse import urljoin
                            next_url = meta_refresh.group(1).strip()
                            if not next_url.startswith("http"):
                                next_url = urljoin(current, next_url)
                            current = next_url
                            if MAIL_VERIFY_URL_REGEX.match(current):
                                return current
                            continue
                        js_redirects = re.findall(
                            r'(?:window\.location|location\.href|location\.replace)\s*[=:]\s*["\']([^"\']+)["\']',
                            html,
                            re.IGNORECASE
                        )
                        if js_redirects:
                            from urllib.parse import urljoin
                            next_url = js_redirects[0].strip()
                            if not next_url.startswith("http"):
                                next_url = urljoin(current, next_url)
                            current = next_url
                            if MAIL_VERIFY_URL_REGEX.match(current):
                                return current
                            continue
                        if BeautifulSoup:
                            try:
                                soup = BeautifulSoup(html, "html.parser")
                                all_links = []
                                for a in soup.find_all("a", href=True):
                                    href = a.get("href", "").strip()
                                    if href.startswith("http"):
                                        all_links.append(href)
                                    elif href.startswith("/"):
                                        from urllib.parse import urljoin
                                        all_links.append(urljoin(current, href))
                                for link in all_links:
                                    if MAIL_VERIFY_URL_REGEX.match(link):
                                        return link
                                    if "discord.com/verify" in link.lower() and link.lower().rstrip("/") != "https://discord.com/verify":
                                        current = link
                                        break
                            except Exception:
                                pass
                        urls_in_html = MAIL_URL_REGEX.findall(html)
                        for found_url in urls_in_html:
                            if MAIL_VERIFY_URL_REGEX.match(found_url):
                                return found_url
                            low_url = found_url.lower()
                            if "discord.com/verify" in low_url and low_url.rstrip("/") not in ("https://discord.com/verify", "http://discord.com/verify"):
                                current = found_url
                                break
                break
            except requests.exceptions.TooManyRedirects:
                try:
                    r = session.get(current, allow_redirects=True, timeout=timeout)
                    final_url = getattr(r, "url", None) or current
                    if MAIL_VERIFY_URL_REGEX.match(final_url):
                        return final_url
                    current = final_url
                except Exception:
                    break
            except Exception:
                break
        if current.lower().rstrip("/") in ("https://discord.com", "http://discord.com"):
            return url
        if "click.discord.com" in current.lower() and not MAIL_VERIFY_URL_REGEX.match(current):
            try:
                r = session.get(current, allow_redirects=True, timeout=timeout)
                final_url = getattr(r, "url", None) or current
                if final_url.lower().rstrip("/") in ("https://discord.com", "http://discord.com"):
                    return url
                if MAIL_VERIFY_URL_REGEX.match(final_url):
                    return final_url
                return final_url
            except Exception:
                pass
        if current.lower().rstrip("/") not in ("https://discord.com", "http://discord.com"):
            return current
        return url
    except Exception as e:
        return url

def _mail_delete_emails(emails):
    try:
        r = _mail_post("/email/delete", {"emails": emails})
        return r.json()
    except Exception:
        return {}

def _mail_wait_for_first_message_id(email_id: int, timeout_seconds: int = 120, poll_interval: float = 2.0):
    deadline = time.time() + max(5, timeout_seconds)
    while time.time() < deadline:
        data = _mail_list_messages_by_email_id(email_id)
        items = data.get("items") or []
        if items:
            def score(item):
                score_val = 0
                frm = (item.get("from") or "").lower()
                sub = (item.get("subject") or "").lower()
                if "discord" in frm:
                    score_val += 50
                if "noreply@discord.com" in frm:
                    score_val += 80
                if "discord" in sub:
                    score_val += 40
                return score_val
            best = sorted(items, key=score, reverse=True)[0]
            return int(best.get("id"))
        time.sleep(poll_interval)
    return None

def _mail_create_email_only():
    global MAIL_AUTH_TOKEN
    try:
        if MAIL_AUTH_EMAIL and MAIL_AUTH_PASSWORD:
            tok = _mail_auth_login(MAIL_AUTH_EMAIL, MAIL_AUTH_PASSWORD)
            if tok:
                MAIL_AUTH_TOKEN = tok
        email, email_id = _mail_create_email(domain="hoanggiakiet.com")
        return email, email_id
    except Exception as e:
        return None, None

def get_email_and_verify_link_mail(email_id: int, wait_seconds: int = 100):
    verify_url = None
    try:
        msg_id = _mail_wait_for_first_message_id(email_id=email_id, timeout_seconds=wait_seconds)
        if not msg_id:
            return None
        msg = _mail_get_message(msg_id)
        body_html = msg.get("body") or ""
        body_text = ""
        links = _mail_collect_links_from_html_and_text(body_html, body_text)
        verify = _mail_extract_exact_verify_url(links)
        if verify:
            print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Link Very = {verify}"))
            verify_url = verify
            return verify_url
        verify = None
        for lnk in links:
            low = lnk.lower()
            if "click.discord.com" in low:
                final = _mail_resolve_click_redirect(lnk)
                if final and MAIL_VERIFY_URL_REGEX.match(final):
                    verify = final
                    break
                if final and final.lower().rstrip("/") in ("https://discord.com", "http://discord.com"):
                    continue
        if verify:
            print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Link Very = {verify}"))
            verify_url = verify
            return verify_url
        return verify_url
    except KeyboardInterrupt:
        return None
    except Exception as e:
        return None

def getLocationInfo() -> dict:
    try:
        if httpx:
            response = httpx.get("https://ipapi.co/json/", timeout=10)
            if response.status_code == 200:
                data = response.json()
                return {
                    "city": data.get("city", "Không xác định"),
                    "country": data.get("country_name", "Không xác định"),
                    "timezone": data.get("timezone", "Không xác định"),
                    "ip": data.get("ip", "Không xác định"),
                    "org": data.get("org", "Không xác định")
                }
    except Exception:
        pass
    
    try:
        import urllib.request
        import json
        with urllib.request.urlopen("http://ip-api.com/json/", timeout=10) as response:
            data = json.loads(response.read().decode())
            return {
                "city": data.get("city", "Không xác định"),
                "country": data.get("country", "Không xác định"),
                "timezone": data.get("timezone", "Không xác định"),
                "ip": data.get("query", "Không xác định"),
                "org": data.get("isp", "Không xác định")
            }
    except Exception:
        return {
            "city": "Không xác định",
            "country": "Không xác định", 
            "timezone": "Không xác định",
            "ip": "Không xác định",
            "org": "Không xác định"
        }
    
def reversea85Layers(data: bytes, layers: int) -> bytes:
    try:
        result = data
        for _ in range(int(layers)):
            result = base64.a85decode(result)
        return result
    except Exception:
        raise

def reverseb85Layers(data: bytes, layers: int) -> bytes:
    try:
        result = data
        for _ in range(int(layers)):
            result = base64.b85decode(result)
        return result
    except Exception:
        raise

def reverseMarshalLayers(data: bytes, layers: int) -> bytes:
    try:
        result = data
        for _ in range(int(layers)):
            result = base64.b85decode(result)
            result = marshal.loads(result)
        return result
    except Exception:
        raise

def decodeEncodedKeyV1(encoded_text: str, a85_layers: int = 3, b85_layers: int = 3, marshal_layers: int = 2) -> bytes:
    data = base64.b64decode(encoded_text.encode())
    data = reverseMarshalLayers(data, marshal_layers)
    data = reverseb85Layers(data, b85_layers)
    data = reversea85Layers(data, a85_layers)
    sha256_bytes = base64.b64decode(data)
    return sha256_bytes

def decodeEncodedKeyHexV1(encoded_text: str, a85_layers: int = 3, b85_layers: int = 3, marshal_layers: int = 2) -> str:
    try:
        return decodeEncodedKeyV1(encoded_text, a85_layers, b85_layers, marshal_layers).hex()
    except Exception:
        return ""

def encodeDeviceProductId(text: str) -> str:
    try:
        data = text.encode('utf-8')
        data = base64.b64encode(data)
        data = base64.b64encode(data)
        data = base64.b85encode(data)
        encoded = data.decode()
        return encoded
    except Exception:
        return text

def decodeDeviceProductId(encoded_text: str) -> str:
    try:
        data = base64.b85decode(encoded_text.encode())
        data = base64.b64decode(data)
        decoded = base64.b64decode(data).decode('utf-8')
        return decoded
    except Exception:
        return ""

def runWarpCommand(cmd_args):
    try:
        result = subprocess.run(
            ["warp-cli"] + cmd_args,
            capture_output=True, text=True, timeout=15
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return -1, "", str(e)

def getWarpStatus() -> str:
    try:
        code, out, err = runWarpCommand(["status"])
        if code != 0:
            return "unknown"
        if "Connected" in out:
            return "connected"
        elif "Disconnected" in out:
            return "disconnected"
        else:
            return "unknown"
    except Exception:
        return "unknown"

def checkWarpInstallation() -> bool:
    try:
        code, out, err = runWarpCommand(["--version"])
        return code == 0
    except Exception:
        return False

def initWarp() -> bool:
    try:
        code, out, err = runWarpCommand(["status"])
        if code != 0:
            return False
        
        if "not registered" in out.lower() or "not logged in" in out.lower():
            return False
        
        return True
    except Exception:
        return False

def killWarProcess():
    try:
        subprocess.run(["taskkill", "/f", "/im", "warp-cli.exe"], 
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(0.5)
    except Exception:
        pass

def flushDns():
    try:
        subprocess.run(["ipconfig", "/flushdns"], 
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(0.3)
    except Exception:
        pass

def forceConnectWarp() -> bool:
    try:
        code, out, err = runWarpCommand(["disconnect"])
        time.sleep(1)
        killWarProcess()
        flushDns()
        
        code, out, err = runWarpCommand(["connect"])
        if code == 0:
            time.sleep(3)
            status = getWarpStatus()
            return status == "connected"
        return False
    except Exception:
        return False

def vpnRotate(wait=5, max_retry=2) -> bool:
    for attempt in range(1, max_retry + 1):
        vpnDisconnect()
        killWarProcess()
        flushDns()
        
        if attempt == 2:
            code, out, err = runWarpCommand(["registration", "delete"])
            code, out, err = runWarpCommand(["registration", "new"])
        
        if vpnConnect(wait):
            return True
        
        time.sleep(1)
    return False

def manageWarp() -> None:
    global warpStatus
    if warpStatus:
        vpnDisconnect()
        warpStatus = False
    else:
        if not vpnConnect():
            vpnDisconnect()
            time.sleep(1)
            vpnConnect()
        warpStatus = True

def vpnConnect(wait=5) -> bool:
    status = getWarpStatus()
    if status == "connected":
        return True
    
    for attempt in range(2):
        code, out, err = runWarpCommand(["connect"])
        if code == 0:
            time.sleep(wait)
            status = getWarpStatus()
            if status == "connected":
                return True
        if attempt == 0:
            time.sleep(1)
    
    return False

def vpnDisconnect() -> bool:
    status = getWarpStatus()
    if status != "connected":
        return True
    
    code, out, err = runWarpCommand(["disconnect"])
    if code == 0:
        time.sleep(1)
        return getWarpStatus() == "disconnected"
    else:
        return False

def toggleWarp(enable: bool) -> bool:
    try:
        if not checkWarpInstallation():
            return False
            
        if not initWarp():
            return False
        
        if enable:
            return vpnConnect()
        else:
            return vpnDisconnect()
    except Exception:
        return False

def inputWthTimeout(prompt: str, timeout_sec: int) -> str | None:
    try:
        userInputQueue: "queue.Queue[str]" = queue.Queue()

        def reader() -> None:
            try:
                val = input(màu(prompt))
                userInputQueue.put(val)
            except Exception:
                pass

        t = threading.Thread(target=reader, daemon=True)
        t.start()
        try:
            return userInputQueue.get(timeout=timeout_sec)
        except queue.Empty:
            return None
    except Exception:
        return None

def waitForF2() -> bool:
    try:
        if keyboard is None:
            print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Thiếu thư viện keyboard, tự động tiếp tục sau 3 giây..."))
            time.sleep(3)
            return True
        
        print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Nhấn F2 để tiếp tục..."))
        
        keyboard.wait('f2')
        return True
    except Exception as e:
        print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Lỗi khi chờ phím F2: {e}, tự động tiếp tục..."))
        time.sleep(2)
        return True
def verifyKey() -> None:
    if httpx is None:
        print(màu("[>] Thiếu thư viện httpx, thoát chương trình"))
        sys.exit(1)
    
    key_url = "https://raw.githubusercontent.com/quangthangcoder11/apikey/refs/heads/master/apikey/api/key/regtoken/key.txt"
    try:
        key_resp = httpx.get(key_url, timeout=10, verify=False)
        if key_resp.status_code != 200:
            print(màu("[>] Không thể tải key"))
            sys.exit(1)
    except Exception as e:
        pass
        sys.exit(1)
    
    remote_text = key_resp.text.strip()
    if not remote_text:
        print(màu("[>] Không tìm thấy key"))
        sys.exit(1)
    
    print()
    user_key = input(màu("[>] Nhập key: ")).strip()
    if not user_key:
        print(màu("[>] Chưa nhập key, thoát chương trình"))
        sys.exit(1)
    
    import base64, hashlib
    md5 = hashlib.md5(user_key.encode()).digest()
    sha256 = hashlib.sha256(md5).digest()
    sha256 = hashlib.sha256(sha256).digest()
    sha256 = hashlib.sha256(sha256).digest()
    b64 = base64.b64encode(sha256)
    data = b64
    for _ in range(3):
        data = base64.a85encode(data)
    for _ in range(3):
        data = base64.b85encode(data)
    for _ in range(2):
        data = marshal.dumps(data)
        data = base64.b85encode(data)
    userKeyEncoded = base64.b64encode(data).decode()
    
    if userKeyEncoded not in remote_text:
        print(màu(f"[ {tgian} ] > Key không hợp lệ, thoát chương trình"))
        sys.exit(1)
    
    print(màu(f"[ {tgian} ] > Key hợp lệ, đang kiểm tra part 2..."))
    
    uuid_url = "https://raw.githubusercontent.com/quangthangcoder11/apikey/refs/heads/master/apikey/api/key/uuid/uuid.json"
    
    try:
        uuid_resp = httpx.get(uuid_url, timeout=10, verify=False)
        if uuid_resp.status_code != 200:
            sys.exit(1)
    except Exception as e:
        sys.exit(1)
    
    try:
        uuid_data = uuid_resp.json()
        if not isinstance(uuid_data, list):
            sys.exit(1)
    except Exception as e:
        sys.exit(1)
    
    system_device_id = getSystemDeviceId()
    system_product_id = getSystemProductId()
    
    if not system_device_id or not system_product_id:
        print(màu("[>] Không thể lấy Device ID hoặc Product ID từ hệ thống"))
        sys.exit(1)
    encoded_system_device_id = encodeDeviceProductId(system_device_id)
    encoded_system_product_id = encodeDeviceProductId(system_product_id)
    
    matched_entry = None
    for entry in uuid_data:
        if isinstance(entry, dict):
            entry_key = entry.get("key", "").strip()
            if entry_key == userKeyEncoded:
                matched_entry = entry
                break
    
    if not matched_entry:
        print(màu(f"[ {tgian} ] > Bố Hoàng Gia Kiệt Đẹp Trai"))
        print(màu(f"[ {tgian} ] > Tuổi lồn mà leak ok :))))"))
        print(màu(f"[ {tgian} ] > Thoát chương trình"))
        sys.exit(1)
    
    entry_device_id = matched_entry.get("device_id", "").strip()
    entry_product_id = matched_entry.get("product_id", "").strip()
    
    if entry_device_id != encoded_system_device_id or entry_product_id != encoded_system_product_id:
        print(màu(f"[ {tgian} ] > Bố Hoàng Gia Kiệt Đẹp Trai"))
        print(màu(f"[ {tgian} ] > Tuổi lồn mà leak ok :))))"))
        print(màu(f"[ {tgian} ] > Thoát chương trình"))
        sys.exit(1)
    print(màu(f"[ {tgian} ] > Xác thực thành công, tiếp tục chương trình"))
    
    clearScreen()
    ShowMainBanner()

def ShowMainBanner() -> None:
    banner = f"""
    ███           █████████            █████     █████     ███                             
   ░░░███        ███░░░░░███          ░░███     ░░███     ░░░                              
     ░░░███     ░███    ░░░   ██████  ███████   ███████   ████  ████████    ███████  █████ 
       ░░░███   ░░█████████  ███░░███░░░███░   ░░░███░   ░░███ ░░███░░███  ███░░███ ███░░  
        ███░     ░░░░░░░░███░███████   ░███      ░███     ░███  ░███ ░███ ░███ ░███░░█████ 
      ███░       ███    ░███░███░░░    ░███ ███  ░███ ███ ░███  ░███ ░███ ░███ ░███ ░░░░███
    ███░        ░░█████████ ░░██████   ░░█████   ░░█████  █████ ████ █████░░███████ ██████ 
   ░░░           ░░░░░░░░░   ░░░░░░     ░░░░░     ░░░░░  ░░░░░ ░░░░ ░░░░░  ░░░░░███░░░░░░  
                                                                           ███ ░███        
                                                                          ░░██████         
                                                                           ░░░░░░          

[>] [ User: {getComputerName()} ]
[>] [ Author: {author} ]
[>] [ Time: {tgian} ]
[>] [ Zalo: {zalo} ]
[>] [ Discord: {discord} ]
[>] [ Facebook: {facebook} ]
"""
    print(Colorate.Horizontal(mauu, banner))

def selectTokenFileForCheck() -> str:
    try:
        if getattr(sys, 'frozen', False):
            scriptDir = Path(sys.executable).parent
        else:
            scriptDir = Path(__file__).resolve().parent
            
        token_dir = scriptDir / "token"
        existing_files = []
        
        for file_path in token_dir.glob("*.txt"):
            if file_path.is_file():
                existing_files.append(file_path.name)
        
        if not existing_files:
            print(màu("[>] Không tìm thấy file token nào trong thư mục token/"))
            return ""
        
        print(màu("\n" + "="*70))
        print(màu(" " * 20 + "CHỌN FILE TOKEN ĐỂ KIỂM TRA" + " " * 20))
        print(màu("="*70))
        print(màu(""))
        print(màu("Các file token hiện có:"))
        print(màu(""))
        
        for i, filename in enumerate(existing_files, 1):
            try:
                file_path = token_dir / filename
                with file_path.open("r", encoding="utf-8") as f:
                    line_count = len([line for line in f if line.strip()])
                print(màu(f"{i}. {filename} ({line_count} tokens)"))
            except Exception:
                print(màu(f"{i}. {filename}"))
        
        print(màu("="*70))
        print(màu(""))
        
        while True:
            try:
                choice = input(màu(f"[>] Chọn file token để kiểm tra (1-{len(existing_files)}): ")).strip()
                if not choice:
                    continue
                    
                if choice.isdigit():
                    choice_num = int(choice)
                    if 1 <= choice_num <= len(existing_files):
                        selected_file = existing_files[choice_num - 1]
                        print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Đã chọn file: {selected_file}"))
                        return selected_file
                    else:
                        print(màu(f"Vui lòng chọn từ 1 đến {len(existing_files)}!"))
                else:
                    print(màu("Vui lòng nhập số hợp lệ!"))
            except KeyboardInterrupt:
                print(màu("\n[>] Hủy chọn file"))
                return ""
            except Exception as e:
                print(màu(f"Lỗi nhập liệu: {e}"))
                
    except Exception as e:
        print(màu(f"[>] Lỗi khi chọn file token: {e}"))
        return ""
def checkVerification() -> None:
    try:
        if getattr(sys, 'frozen', False):
            scriptDir = Path(sys.executable).parent
        else:
            scriptDir = Path(__file__).resolve().parent
        selected_file = selectTokenFileForCheck()
        if not selected_file:
            print(màu("[>] Không có file token nào được chọn"))
            return
            
        tokensFile = scriptDir / "token" / selected_file
        if not tokensFile.exists():
            print(màu(f"[>] Không tìm thấy file {selected_file}"))
            return
        print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Đang kiểm tra token trong {selected_file}..."))

        try:
            with tokensFile.open("r", encoding="utf-8") as f:
                lines = [line.strip() for line in f.readlines() if line.strip()]
        except Exception:
            lines = []
        if not lines:
            print(màu(f"[>] File {selected_file} trống"))
            return

        def discordGet(path: str, token: str):
            url = f"https://discord.com/api/v10{path}"
            headers = {
                "Authorization": token,
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0"
            }
            try:
                if httpx:
                    r = httpx.get(url, headers=headers, timeout=10)
                    try:
                        return r.status_code, (r.json() if r.headers.get("content-type", "").startswith("application/json") else None)
                    except Exception:
                        return r.status_code, None
                else:
                    import urllib.request, json as _json
                    req = urllib.request.Request(url, headers=headers, method="GET")
                    with urllib.request.urlopen(req, timeout=10) as resp:
                        status = resp.getcode()
                        body = resp.read().decode("utf-8", errors="ignore")
                        try:
                            return status, _json.loads(body)
                        except Exception:
                            return status, None
            except Exception:
                return -1, None

        tokenLive: list[str] = []
        tokenDie: list[str] = []
        tokenVerified: list[str] = []
        tokenVerifiedPhone: list[str] = []
        untokenVerifiedPhone: list[str] = []
        detailsLines: list[str] = []

        DISCORD_EPOCH = 1420070400000 

        def snowflake_to_datetime_str(sf: str) -> str:
            try:
                ts_ms = (int(sf) >> 22) + DISCORD_EPOCH
                return datetime.fromtimestamp(ts_ms / 1000, timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
            except Exception:
                return ""

        def public_flags_to_badges(flags_val: int) -> str:
            try:
                flags = int(flags_val)
            except Exception:
                return ""
            mapping = [
                (1 << 0, "STAFF"),
                (1 << 1, "PARTNER"),
                (1 << 2, "HYPESQUAD"),
                (1 << 3, "BUG_HUNTER_L1"),
                (1 << 6, "HYPESQUAD_BRAVERY"),
                (1 << 7, "HYPESQUAD_BRILLIANCE"),
                (1 << 8, "HYPESQUAD_BALANCE"),
                (1 << 9, "EARLY_SUPPORTER"),
                (1 << 10, "TEAM_USER"),
                (1 << 14, "BUG_HUNTER_L2"),
                (1 << 16, "VERIFIED_BOT"),
                (1 << 17, "VERIFIED_DEVELOPER"),
                (1 << 18, "CERTIFIED_MOD"),
                (1 << 19, "BOT_HTTP_INTERACTIONS"),
                (1 << 22, "ACTIVE_DEVELOPER"),
            ]
            badges = [name for bit, name in mapping if (flags & bit) != 0]
            return ",".join(badges)

        print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Bắt đầu kiểm tra {len(lines)} token...\n"))
        for line in lines:
            if "|" not in line:
                continue
            token = line.split("|")[0]
            status, data = discordGet("/users/@me", token)
            if status == 200 and isinstance(data, dict):
                tokenLive.append(line)
                if bool(data.get("verified", False)):
                    tokenVerified.append(line)
                if data.get("phone"):
                    tokenVerifiedPhone.append(line)
                else:
                    untokenVerifiedPhone.append(line)
                try:
                    uid = str(data.get("id") or "")
                    uname = data.get("username") or "unknown"
                    global_name = data.get("global_name") or ""
                    verified_email = bool(data.get("verified", False))
                    email_addr = data.get("email") or ""
                    phone_num = data.get("phone") or ""
                    created_at = snowflake_to_datetime_str(uid) if uid else ""

                    r_status, r_data = discordGet("/users/@me/relationships", token)
                    friend_count = len([r for r in (r_data or []) if isinstance(r, dict) and r.get("type") == 1]) if r_status == 200 and isinstance(r_data, list) else 0

                    print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Display: {global_name or uname} | User: {uname} | ID: {uid} | Created: {created_at} | Verified: {verified_email} | Email: {email_addr or 'N/A'} | Phone: {phone_num or 'N/A'}"))
                    detailsLines.append(
                        "|".join([
                            (global_name or uname),
                            uname,
                            uid,
                            created_at,
                            str(friend_count),
                            str(verified_email),
                            email_addr,
                            phone_num,
                        ])
                    )
                except Exception:
                    pass
            elif status == 401:
                tokenDie.append(line)
            else:
                tokenDie.append(line)

        out_dir = scriptDir / "output"
        try:
            out_dir.mkdir(parents=True, exist_ok=True)
            with (out_dir / "live.txt").open("w", encoding="utf-8") as f:
                f.write("\n".join(tokenLive))
            with (out_dir / "die.txt").open("w", encoding="utf-8") as f:
                f.write("\n".join(tokenDie))
            with (out_dir / "verified.txt").open("w", encoding="utf-8") as f:
                f.write("\n".join(tokenVerified))
            with (out_dir / "phone_verified.txt").open("w", encoding="utf-8") as f:
                f.write("\n".join(tokenVerifiedPhone))
            with (out_dir / "phone_unverified.txt").open("w", encoding="utf-8") as f:
                f.write("\n".join(untokenVerifiedPhone))
            try:
                header = "|".join([
                    "display_name",
                    "username",
                    "id",
                    "created_at",
                    "friends",
                    "verified",
                    "email",
                    "phone",
                ])
                with (out_dir / "details.txt").open("w", encoding="utf-8") as f:
                    if detailsLines:
                        f.write(header + "\n" + "\n".join(detailsLines))
            except Exception:
                pass
        except Exception:
            pass

        print(màu(f"\n[ {time.strftime('%H:%M:%S')} ] »» Hoàn thành!"))
        print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Live: {len(tokenLive)}"))
        print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Die: {len(tokenDie)}"))
        print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Verified: {len(tokenVerified)}"))
        print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Phone Verified: {len(tokenVerifiedPhone)} | Phone Unverified: {len(untokenVerifiedPhone)}"))

    except Exception as e:
        print(màu(f"[>] Lỗi khi kiểm tra token: {e}"))

def setupConfig() -> None:
    try:
        if getattr(sys, 'frozen', False):
            scriptDir = Path(sys.executable).parent
        else:
            scriptDir = Path(__file__).resolve().parent
            
        configFile = scriptDir / "config.json"
        
        default_config = {
            "FireFoxPath": r"C:\\Program Files\\Mozilla Firefox\\private_browsing.exe",
            "urlRegisterDiscord": "https://discord.com/register",
            "displayName": "",
            "userName": "",
            "password": "hoanggiakiet0507",
            "mailverify": "tmail.py",
            "rdIcon": True,
            "rdIconStyle": "sau",
            "webhookLog": "true",
            "webhookUrl": "",
            "autoAcceptInvite": "true",
            "setBio": "true",
            "setPronouns": "true",
            "setGuildTag": "false",
            "linkGuildTagServer": "",
            "vpns": "true"
            
        }
        
        current_config = default_config.copy()
        if configFile.exists():
            try:
                with configFile.open("r", encoding="utf-8") as f:
                    existingConfig = json.load(f)
                    current_config.update(existingConfig)
            except Exception:
                pass
        
        print(màu("\n" + "="*70))
        print(màu(" " * 28 + "SETUP CONFIG" + " " * 28))
        print(màu("="*70))
        print(màu(""))
        print(màu("Nhấn Enter để giữ nguyên giá trị hiện tại"))
        print(màu(""))
        print(màu("="*70))
        
        config_fields = [
            ("FireFoxPath", "Đường dẫn Firefox", "Ví dụ: C:\\Program Files\\Mozilla Firefox\\private_browsing.exe"),
            ("urlRegisterDiscord", "URL đăng ký Discord", "Ví dụ: https://discord.com/register"),
            ("displayName", "Tên hiển thị mặc định", "Để trống nếu không muốn đặt"),
            ("userName", "Tên người dùng mặc định", "Để trống nếu không muốn đặt"),
            ("password", "Mật khẩu mặc định", "Ví dụ: hoanggiakiet0507"),
            ("mailverify", "Module xác thực email", "tmail.py hoặc hotmail.py, apimail.py"),
            ("rdIcon", "Bật random icon cho DisplayName (true/false)", "true hoặc false"),
            ("rdIconStyle", "Kiểu chèn icon (both/prefix/suffix)", "both, prefix hoặc suffix"),
            ("webhookLog", "Bật/tắt gửi webhook log (true/false)", "true hoặc false"),
            ("webhookUrl", "Discord Webhook URL để gửi log", "Để trống nếu không muốn gửi webhook"),
            ("autoAcceptInvite", "Bật/tắt tự động ấn nút Accept Invite bằng Tab+Enter (true/false)", "true hoặc false"),
            ("setBio", "Bật/tắt tự động set bio cho token (true/false)", "true hoặc false"),
            ("setPronouns", "Bật/tắt tự động set pronouns cho token (true/false)", "true hoặc false"),
            ("setGuildTag", "Bật/tắt tự động set guild tag cho token (true/false)", "true hoặc false"),
            ("linkGuildTagServer", "Link invite server để set guild tag", "Ví dụ: https://discord.gg/trunggianstore"),
            ("vpns", "Bật/tắt tự động quản lý VPN 1.1.1.1 WARP (true/false)", "true hoặc false")
            
        ]
        
        for field_key, field_name, example in config_fields:
            current_value = current_config.get(field_key, "")
            print(màu(f"\n[{field_name}]"))
            print(màu(f"Giá trị hiện tại: {current_value if current_value else '(trống)'}"))
            print(màu(f"Hướng dẫn: {example}"))
            
            try:
                new_value = input(màu(f"[>] Nhập giá trị mới: ")).strip()
                if new_value:
                    if field_key == "inviteLinks":
                        links = [u.strip() for u in new_value.split(",") if u.strip()]
                        current_config[field_key] = links
                    else:
                        current_config[field_key] = new_value
                    print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Đã cập nhật {field_name}"))
                else:
                    print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Giữ nguyên giá trị cũ"))
            except KeyboardInterrupt:
                print(màu("\n[>] Hủy setup config"))
                return
            except Exception as e:
                print(màu(f"[>] Lỗi nhập liệu: {e}"))
        
        with configFile.open("w", encoding="utf-8") as f:
            json.dump(current_config, f, indent=4, ensure_ascii=False)
        
        print(màu(f"\n[ {time.strftime('%H:%M:%S')} ] »» Đã lưu config.json thành công!"))
        print(màu(""))
        print(màu("="*70))
        print(màu(" " * 25 + "CONFIG HIỆN TẠI" + " " * 25))
        print(màu("="*70))
        print(màu(""))
        for field_key, field_name, _ in config_fields:
            value = current_config.get(field_key, "")
            print(màu(f"  {field_name}: {value if value else '(trống)'}"))
        print(màu(""))
        print(màu("="*70))
        
    except Exception as e:
        print(màu(f"[>] Lỗi khi setup config: {e}"))

def showMenu() -> str:
    print(màu("\n" + "="*70))
    print(màu(" " * 25 + "MENU CONSOLE" + " " * 25))
    print(màu("="*70))
    print(màu(""))
    print(màu("  1. Reg Token"))
    print(màu("  2. Reg Token + Join Server"))
    print(màu("  3. Check Verification"))
    print(màu("  4. Setup Config"))
    print(màu("  5. Exit"))
    print(màu(""))
    print(màu("="*70))
    
    while True:
        try:
            choice = input(màu("[>] Chọn chức năng (1-5): ")).strip()
            if choice in ['1', '2', '3', '4', '5']:
                return choice
            else:
                print(màu("Vui lòng chọn từ 1-5!"))
        except KeyboardInterrupt:
            print(màu("\n[>] Thoát chương trình"))
            return '5'
        except Exception:
            print(màu("Lỗi nhập liệu, vui lòng thử lại!"))

def selectBrowser() -> str:
    global browserRotationList, isRotationMode
    browsers = {
        '1': "firefox",
        '2': "edge",
        '3': "brave",
        '4': "coccoc",
        '5': "opera",
        '6': "chrome"
    }

    print(màu("\n" + "="*70))
    print(màu(" " * 25 + "CHỌN TRÌNH DUYỆT" + " " * 25))
    print(màu("="*70))
    print(màu(""))
    print(màu("  1. Firefox Private"))
    print(màu("  2. Edge Private"))
    print(màu("  3. Brave Private"))
    print(màu("  4. Cốc Cốc Private"))
    print(màu("  5. Opera Private"))
    print(màu("  6. Chrome Private"))
    print(màu("  7. Nhiều trình duyệt (xoay vòng)"))
    print(màu(""))
    print(màu("="*70))
    
    while True:
        try:
            browser_choice = input(màu("[>] Chọn trình duyệt (1-7): ")).strip()
            if browser_choice in browsers:
                isRotationMode = False
                return browsers[browser_choice]
            elif browser_choice == '7':
                isRotationMode = True
                while True:
                    rotation_input = input(màu("[>] Chọn trình duyệt (1,2,3,4,5,6 hoặc all) ")).strip().lower()
                    if rotation_input == 'all':
                        browserRotationList = list(browsers.values())
                        print(màu(f"[+] Ok Done Cbi running tool: {', '.join(browserRotationList)}"))
                        return "rotation"
                    else:
                        selected_indices = [s.strip() for s in rotation_input.split(',')]
                        temp_list = []
                        valid_input = True
                        for index in selected_indices:
                            if index in browsers:
                                temp_list.append(browsers[index])
                            else:
                                print(màu(f"[!] Lựa chọn không hợp lệ: '{index}'. Vui lòng chỉ nhập các số từ 1 đến 6."))
                                valid_input = False
                                break
                        if valid_input and temp_list:
                            browserRotationList = temp_list
                            print(màu(f"[+] Ok Done Cbi running tool: {', '.join(browserRotationList)}"))
                            return "rotation"
                        elif valid_input:
                            print(màu("[!] Danh sách trống. Vui lòng nhập lựa chọn."))
            else:
                print(màu("Vui lòng chọn từ 1-7!"))
        except KeyboardInterrupt:
            print(màu("\n[>] Hủy chọn trình duyệt"))
            isRotationMode = False
            return "firefox"
        except Exception as e:
            print(màu(f"Lỗi nhập liệu, vui lòng thử lại: {e}"))

def selectTokenFile() -> str:
    try:
        if getattr(sys, 'frozen', False):
            scriptDir = Path(sys.executable).parent
        else:
            scriptDir = Path(__file__).resolve().parent
            
        token_dir = scriptDir / "token"
        if not token_dir.exists():
            token_dir.mkdir(parents=True, exist_ok=True)
        
        existing_files = []
        for file_path in token_dir.glob("*.txt"):
            if file_path.is_file():
                existing_files.append(file_path.name)
        
        if not existing_files:
            print(màu("[>] Không tìm thấy file token nào trong thư mục token/"))
            print(màu("[>] Sẽ tạo file mới: tokeninvite.txt"))
            return "tokeninvite.txt"
        
        print(màu("\n" + "="*70))
        print(màu(" " * 22 + "CHỌN FILE LƯU TOKEN" + " " * 22))
        print(màu("="*70))
        print(màu(""))
        print(màu("Các file token hiện có:"))
        print(màu(""))
        
        for i, filename in enumerate(existing_files, 1):
            try:
                file_path = token_dir / filename
                with file_path.open("r", encoding="utf-8") as f:
                    line_count = len([line for line in f if line.strip()])
                print(màu(f"{i}. {filename} ({line_count} tokens)"))
            except Exception:
                print(màu(f"{i}. {filename}"))
        
        print(màu(""))
        print(màu(f"  {len(existing_files) + 1}. Tạo file mới"))
        print(màu(""))
        print(màu("="*70))
        
        while True:
            try:
                choice = input(màu(f"[>] Chọn file (1-{len(existing_files) + 1}): ")).strip()
                if not choice:
                    continue
                    
                if choice.isdigit():
                    choice_num = int(choice)
                    if 1 <= choice_num <= len(existing_files):
                        selected_file = existing_files[choice_num - 1]
                        print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Đã chọn file: {selected_file}"))
                        return selected_file
                    elif choice_num == len(existing_files) + 1:
                        while True:
                            new_filename = input(màu("[>] Nhập tên file mới (không cần .txt): ")).strip()
                            if not new_filename:
                                print(màu("Tên file không được để trống!"))
                                continue
                            if not new_filename.endswith('.txt'):
                                new_filename += '.txt'
                            if new_filename in existing_files:
                                print(màu(f"File {new_filename} đã tồn tại! Vui lòng chọn tên khác."))
                                continue
                            
                            print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Sẽ tạo file mới: {new_filename}"))
                            return new_filename
                    else:
                        print(màu(f"Vui lòng chọn từ 1 đến {len(existing_files) + 1}!"))
                else:
                    print(màu("Vui lòng nhập số hợp lệ!"))
            except KeyboardInterrupt:
                print(màu("\n[>] Hủy chọn file, sử dụng file mặc định"))
                return "tokeninvite.txt"
            except Exception as e:
                print(màu(f"Lỗi nhập liệu: {e}"))
                
    except Exception as e:
        print(màu(f"[>] Lỗi khi chọn file token: {e}"))
        return "tokeninvite.txt"

def bannerkey() -> None:
    banner = f"""
    ███          ██████   ██████            ███                ███████████                   ████         
   ░░░███       ░░██████ ██████            ░░░                ░█░░░███░░░█                  ░░███         
     ░░░███      ░███░█████░███   ██████   ████  ████████     ░   ░███  ░   ██████   ██████  ░███   █████ 
       ░░░███    ░███░░███ ░███  ░░░░░███ ░░███ ░░███░░███        ░███     ███░░███ ███░░███ ░███  ███░░  
        ███░     ░███ ░░░  ░███   ███████  ░███  ░███ ░███        ░███    ░███ ░███░███ ░███ ░███ ░░█████ 
      ███░       ░███      ░███  ███░░███  ░███  ░███ ░███        ░███    ░███ ░███░███ ░███ ░███  ░░░░███
    ███░         █████     █████░░████████ █████ ████ █████       █████   ░░██████ ░░██████  █████ ██████ 
   ░░░          ░░░░░     ░░░░░  ░░░░░░░░ ░░░░░ ░░░░ ░░░░░       ░░░░░     ░░░░░░   ░░░░░░  ░░░░░ ░░░░░░  

[>] [ User: {getComputerName()} ]
[>] [ Author: {author} ]
[>] [ Time: {tgian} ]
[>] [ Zalo: {zalo} ]
[>] [ Discord: {discord} ]
[>] [ Facebook: {facebook} ]
"""
    print(Colorate.Horizontal(mauu, banner))

def _banner() -> None:
    title = r"""
    ███          ███████████                     ███████████          █████                         
   ░░░███       ░░███░░░░░███                   ░█░░░███░░░█         ░░███                          
     ░░░███      ░███    ░███   ██████   ███████░   ░███  ░   ██████  ░███ █████  ██████  ████████  
       ░░░███    ░██████████   ███░░███ ███░░███    ░███     ███░░███ ░███░░███  ███░░███░░███░░███ 
        ███░     ░███░░░░░███ ░███████ ░███ ░███    ░███    ░███ ░███ ░██████░  ░███████  ░███ ░███ 
      ███░       ░███    ░███ ░███░░░  ░███ ░███    ░███    ░███ ░███ ░███░░███ ░███░░░   ░███ ░███ 
    ███░         █████   █████░░██████ ░░███████    █████   ░░██████  ████ █████░░██████  ████ █████
   ░░░          ░░░░░   ░░░░░  ░░░░░░   ░░░░░███   ░░░░░     ░░░░░░  ░░░░ ░░░░░  ░░░░░░  ░░░░ ░░░░░ 
                                        ███ ░███                                                    
                                       ░░██████                                                     
                                        ░░░░░░                                                                                                                                                                                                                                                         
"""

    python = f"[ {tgian} ] »» Running With Python: {pythonver}"
    tacgia = f"[ {tgian} ] »» Author: {author}"
    tgianok = f"[ {tgian} ] »» Start At: {tgian}"
    subtitle = f"[ {tgian} ] »» Reg Token - Discord Register"
    
    modules_info = getModuleInfo()
    modules_status = []
    for module_name, info in modules_info.items():
        status = "✓" if info["exists"] else "✗"
        modules_status.append(f"{module_name}: {status}")
    
    modules_text = f"[ {tgian} ] »» Modules Loaded: {' | '.join(modules_status)}"
    
    banner_text = f"\n{title}\n{python}\n{tacgia}\n{tgianok}\n{subtitle}\n{modules_text}\n"
    try:
        print(màu(banner_text))
    except Exception:
        print(banner_text)


def _check_and_calibrate_button() -> bool:
    try:
        if getattr(sys, 'frozen', False):
            scriptDir = Path(sys.executable).parent
        else:
            scriptDir = Path(__file__).resolve().parent
        configFile = scriptDir / "config.json"
        
        if not configFile.exists():
            print(màu("[>] Không tìm thấy config.json"))
            return False
        
        with configFile.open("r", encoding="utf-8") as f:
            config_data = json.load(f)
        auto_accept = config_data.get("autoAcceptInvite", "true")
        if isinstance(auto_accept, str):
            auto_accept = auto_accept.lower() in ("true", "1", "yes", "on")
        else:
            auto_accept = bool(auto_accept)
        
        if not auto_accept:
            print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Auto accept tắt, người dùng tự click"))
            return False
        
        print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Chuẩn bị click Accept invite"))
        return True
            
    except Exception as e:
        print(màu(f"[>] Lỗi khi kiểm tra config: {e}"))
        return True  

def _kill_browser_processes() -> None:
    try:
        processes_to_kill = [
            "firefox.exe",
            "private_browsing.exe",
            "msedge.exe",
            "brave.exe",
            "browser.exe", 
            "opera.exe",
            "chrome.exe"
        ]
        for process_name in processes_to_kill:
            try:
                os.system(f"taskkill /f /im {process_name} >nul 2>&1")
            except Exception:
                pass
        time.sleep(0.5)
    except Exception:
        pass

def _open_browser_for_join(invite_link: str) -> None:
    try:
        global browserExePath, selectedBrowser
        print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Đang mở trình duyệt để join server thủ công (HCAPTCHA)..."))
        try:
            if browserExePath:
                browser_type = selectedBrowser
                browser_args = [browserExePath]
                if browser_type == "edge":
                    browser_args.append("--inprivate")
                elif browser_type in ["brave", "coccoc", "chrome"]:
                    browser_args.append("--incognito")
                elif browser_type == "opera":
                    browser_args.append("--private")
                browser_args.append(invite_link.strip())
                subprocess.Popen(browser_args, shell=False)
            else:
                os.startfile(invite_link.strip())
        except Exception as e:
            print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Lỗi khi mở trình duyệt: {e}"))
            try:
                os.startfile(invite_link.strip())
            except Exception:
                pass
        print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Đã mở trình duyệt, vui lòng join server thủ công và nhấn F2 để tiếp tục..."))
        waitForF2()
    except Exception as e:
        print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Lỗi khi mở trình duyệt: {e}"))

def _auto_click_accept_invite() -> bool:
    try:
        if pyautogui is None:
            print(màu("[>] Không thể tự động ấn nút: thiếu thư viện pyautogui"))
            return False
        
        print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Đang ấn nút Accept Invite"))
        time.sleep(2)
        
        try:
            screen_width, screen_height = pyautogui.size()
            center_x, center_y = screen_width // 2, screen_height // 2
            offset_x = random.randint(-10, 10)
            offset_y = random.randint(-10, 10)
            click_x = max(0, min(screen_width, center_x + offset_x))
            click_y = max(0, min(screen_height, center_y + offset_y))
            
            pyautogui.click(click_x, click_y)
            pyautogui.press('tab')
            
            pyautogui.press('enter')
            
            print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Đã ấn nút Accept Invite"))
            return True
            
        except Exception as e:
            print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Lỗi khi ấn Tab + Enter: {e}"))
            return False
        
    except Exception as e:
        print(màu(f"[>] Lỗi khi tự động ấn nút: {e}"))
        return False

def _copy_token_from_popup(email_addr: str, password: str, display_name: str = "", user_name: str = "") -> bool:
    try:
        if pyautogui is None or pyperclip is None:
            print(màu("Không thể copy token: thiếu thư viện pyautogui hoặc pyperclip"))
            return
        
        print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Loadding get tokens discord..."))
        
        time.sleep(2)
        
        try:
            popup_found = False
            
            for i in range(20):
                try:
                    screen_width, screen_height = pyautogui.size()
                    center_x, center_y = screen_width // 2, screen_height // 2
                    pyautogui.click(center_x, center_y)
                    
                    pyautogui.hotkey("ctrl", "a")
                    
                    pyautogui.hotkey("ctrl", "c")
                    
                    
                    clipboard_content = pyperclip.paste()
                    
                    if clipboard_content:
                        lines = clipboard_content.split('\n')
                        null_detected = False
                        for line in lines:
                            clean_line = line.strip().strip('"').strip("'")
                            lower_val = clean_line.lower()
                            is_nullish = lower_val in ("null", "undefined", "none", '""', "''") or clean_line == ""
                            has_two_dots = clean_line.count('.') >= 2
                            try:
                                token_pattern = re.compile(r'^(mfa\.[\w\-]{20,}|[\w\-]{20,}\.[\w\-]{5,}\.[\w\-]{15,})$')
                            except Exception:
                                token_pattern = None
                            looks_like_token = (
                                len(clean_line) > 20 and (
                                    has_two_dots or
                                    clean_line.startswith('mfa.') or
                                    (token_pattern.match(clean_line) if token_pattern else False)
                                )
                            )
                            
                            if (looks_like_token and not is_nullish and
                                not clean_line.startswith('Your token:') and
                                not clean_line.startswith('discord.com')):
                                
                                if not email_addr:
                                    email_addr = "unknown@email.com"
                                if not password:
                                    password = "quangthang0507"
                                masked_token = clean_line
                                try:
                                    if len(clean_line) >= 12:
                                        import random
                                        start_idx = random.randint(0, len(clean_line) - 12)
                                        masked_token = clean_line[:start_idx] + '************' + clean_line[start_idx+12:]
                                except Exception:
                                    masked_token = clean_line
                                
                                print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Token tìm thấy: {masked_token}"))
                                print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Email: {email_addr}"))
                                print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Password: {password}"))
                                
                                try:
                                    _save_token_with_info(clean_line, email_addr, password, display_name, user_name)
                                    print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Token đã được lưu thành công!"))
                                    try:
                                        global inviteUrlsGlobal
                                        if isinstance(inviteUrlsGlobal, list) and inviteUrlsGlobal:
                                            for idx, url in enumerate(inviteUrlsGlobal):
                                                if not isinstance(url, str) or not url.strip():
                                                    continue
                                                print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Đang join server #{idx+1}/{len(inviteUrlsGlobal)}..."))
                                                
                                                joiner_instance = joiner()
                                                joiner_instance.invite = url.strip()
                                                success, hcaptcha_detected = joiner_instance.join(clean_line, url.strip())
                                                
                                                if success:
                                                    print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Đã join server #{idx+1} thành công!"))
                                                    _kill_browser_processes()
                                                elif hcaptcha_detected:
                                                    print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Phát hiện HCAPTCHA, mở trình duyệt để join thủ công..."))
                                                    _open_browser_for_join(url.strip())
                                                    _kill_browser_processes()
                                                else:
                                                    print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Không thể join server #{idx+1} qua API, mở trình duyệt để join thủ công..."))
                                                    _open_browser_for_join(url.strip())
                                                    _kill_browser_processes()
                                                
                                                if idx < len(inviteUrlsGlobal) - 1:
                                                    time.sleep(1)
                                    except Exception as e:
                                        print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Lỗi khi join server: {e}"))
                                        pass
                                    try:
                                        if not inviteUrlsGlobal and isVpnEnabled():
                                            toggleWarp(True)
                                    except Exception:
                                        pass
                                    popup_found = True
                                    return True
                                except Exception as e:
                                    print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Không thể lưu token: {e}"))
                                    popup_found = True
                                    return False
                            elif is_nullish:
                                try:
                                    print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Token null/undefined, bỏ qua..."))
                                except Exception:
                                    pass
                                return False
                        
                        if popup_found:
                            break
                    
                except Exception:
                    pass
                
                time.sleep(0.5)
            
            if not popup_found:
                print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Không tìm thấy popup token"))
                return False
                
        except Exception as e:
            print(màu(f"Lỗi khi tìm popup: {e}"))
            return False
        
    except Exception as e:
        print(màu(f"Lỗi khi copy token từ popup: {e}"))
        return False


def _send_webhook_log(token: str, email: str, password: str, display_name: str, user_name: str, creation_time: str) -> None:
    try:
        if getattr(sys, 'frozen', False):
            scriptDir = Path(sys.executable).parent
        else:
            scriptDir = Path(__file__).resolve().parent
            
        configFile = scriptDir / "config.json"
        if not configFile.exists():
            return
            
        with configFile.open("r", encoding="utf-8") as f:
            config_data = json.load(f)
        webhook_log_enabled = config_data.get("webhookLog", "false")
        if isinstance(webhook_log_enabled, str):
            webhook_log_enabled = webhook_log_enabled.lower() in ("true", "1", "yes", "on")
        elif isinstance(webhook_log_enabled, bool):
            webhook_log_enabled = webhook_log_enabled
        else:
            webhook_log_enabled = False
            
        if not webhook_log_enabled:
            return
            
        webhook_url = config_data.get("webhookUrl", "").strip()
        if not webhook_url or not webhook_url.startswith("http"):
            return
        rd_icon_value = config_data.get("rdIcon", True)
        if isinstance(rd_icon_value, str):
            rd_icon_enabled = rd_icon_value.lower() in ("true", "1", "yes", "on")
        else:
            rd_icon_enabled = bool(rd_icon_value)
        display_name_value = display_name or "Không có"
        if rd_icon_enabled and display_name and any(ord(char) > 127 for char in display_name):
            display_name_value = f"```{display_name}```"
            
        embed = {
            "title": "🎉 Tài khoản Discord đã được tạo thành công!",
            "color": 0x00ff00, 
            "fields": [
                {
                    "name": "📧 Email",
                    "value": email,
                    "inline": True
                },
                {
                    "name": "👤 Display Name",
                    "value": display_name_value,
                    "inline": True
                },
                {
                    "name": "🏷️ Username",
                    "value": user_name,
                    "inline": True
                },
                {
                    "name": "🔑 Password",
                    "value": password,
                    "inline": True
                },
                {
                    "name": "🎫 Token",
                    "value": f"``{token}``",
                    "inline": False
                },
                {
                    "name": "📅 Ngày tạo",
                    "value": creation_time,
                    "inline": True
                },
                {
                    "name": "⏰ Thời gian",
                    "value": time.strftime("%H:%M:%S"),
                    "inline": True
                },
                {
                    "name": "🌐 IP Public",
                    "value": getPublicIp(),
                    "inline": True
                }
            ],
            "footer": {
                "text": f"Reg Token Discord v{version} - {author} | Copyright © 2025",
                "icon_url": "https://cdn.discordapp.com/attachments/1380919270052986983/1424118555745587210/standard_5.gif"
            }
        }
        
        payload = {
            "embeds": [embed]
        }
        if httpx:
            response = httpx.post(webhook_url, json=payload, timeout=10)
            if response.status_code in [200, 204]:
                pass
            else:
                pass
        else:
            import urllib.request
            import json as _json
            req = urllib.request.Request(
                webhook_url,
                data=_json.dumps(payload).encode('utf-8'),
                headers={'Content-Type': 'application/json'},
                method='POST'
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.getcode() in [200, 204]:
                    pass
                else:
                    pass
                    
    except Exception as e:
        pass

def _save_token_with_info(token: str, email: str, password: str, display_name: str = "", user_name: str = "") -> None:
    try:
        if getattr(sys, 'frozen', False):
            scriptDir = Path(sys.executable).parent
        else:
            scriptDir = Path(__file__).resolve().parent
            
        token_dir = scriptDir / "token"
        try:
            token_dir.mkdir(parents=True, exist_ok=True)
        except Exception:
            pass
        target_name = tokenSaveFilename if tokenSaveFilename else "tokens.txt"
        token_file = token_dir / target_name
        creation_time = time.strftime("%Y-%m-%d")
        file_has_content = False
        if token_file.exists():
            with token_file.open("r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    file_has_content = True
        
        with token_file.open("a", encoding="utf-8") as f:
            if file_has_content:
                f.write(f"\n{token}|{email}|{password}|{creation_time}")
            else:
                f.write(f"{token}|{email}|{password}|{creation_time}")

        try:
            _send_webhook_log(token, email, password, display_name, user_name, creation_time)
        except Exception as e:
            pass
        try:
            if getattr(sys, 'frozen', False):
                scriptDir = Path(sys.executable).parent
            else:
                scriptDir = Path(__file__).resolve().parent
        except Exception:
            pass
        
    except Exception as e:
        print(màu(f"Lỗi khi lưu token: {e}"))

def _save_token(token: str) -> None:
    try:
        if getattr(sys, 'frozen', False):
            scriptDir = Path(sys.executable).parent
        else:
            scriptDir = Path(__file__).resolve().parent
            
        token_dir = scriptDir / "token"
        try:
            token_dir.mkdir(parents=True, exist_ok=True)
        except Exception:
            pass
        target_name = tokenSaveFilename if tokenSaveFilename else "tokens.txt"
        token_file = token_dir / target_name
        creation_time = time.strftime("%Y-%m-%d")
        
        with token_file.open("a", encoding="utf-8") as f:
            f.write(f"{token}|||{creation_time}\n")
        
        print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Token đã được lưu: {token[:20]}..."))
            
        try:
            configFile = scriptDir / "config.json"
            display_name = ""
            user_name = ""
            email = "unknown@email.com"
            password = "hoanggiakiet0507"
            if configFile.exists():
                with configFile.open("r", encoding="utf-8") as f:
                    config_data = json.load(f)
                    display_name = config_data.get("displayName", "")
                    user_name = config_data.get("userName", "")
                    password = config_data.get("password", "hoanggiakiet0507")
            
            _send_webhook_log(token, email, password, display_name, user_name, creation_time)
        except Exception as e:
            pass
        try:
            pass
        except Exception:
            pass
        
    except Exception as e:
        print(màu(f"Lỗi khi lưu token: {e}"))
result_queue = queue.Queue()

def _pop_first_email_cred(scriptDir: Path):
    try:
        email_path = scriptDir / "email.txt"
        if not email_path.exists():
            return None
        lines = email_path.read_text(encoding="utf-8").splitlines()
        remaining = []
        picked = None
        for ln in lines:
            line = ln.strip()
            if not line or line.startswith("#"):
                remaining.append(ln)
                continue
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 4 and picked is None:
                email, passmail, refresh_token, client_id = parts[:4]
                if email and refresh_token and client_id:
                    picked = (email, passmail, refresh_token, client_id)
                    continue
            remaining.append(ln)
        if picked is not None:
            email_path.write_text("\n".join(remaining), encoding="utf-8")
        return picked
    except Exception:
        return None

def main(account_number: int = 1) -> str:
    global warpStatus, edgePrivateWindowOpened
    clearScreen()
    _banner()
    edgePrivateWindowOpened = False
    
    if account_number == 1:
        if isVpnEnabled():
            vpnDisconnect()
            try:
                warpStatus = False
            except Exception:
                pass
        else:
            pass
            try:
                warpStatus = False
            except Exception:
                pass
    
    if getattr(sys, 'frozen', False):
        scriptDir = Path(sys.executable).parent
    else:
        scriptDir = Path(__file__).resolve().parent
        
    config = scriptDir / "config.json"
    token_dir = scriptDir / "token"
    try:
        token_dir.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass
    target_name = tokenSaveFilename if tokenSaveFilename else "tokens.txt"
    token_file = token_dir / target_name
    
    token_count = 0
    if token_file.exists():
        try:
            with token_file.open("r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    token_count = len([line for line in content.splitlines() if line.strip()])
        except Exception:
            pass
    
    try:
        shown_name = str(token_file.name)
    except Exception:
        shown_name = "tokens.txt"
    print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Hiện tại có {token_count} token trong file {shown_name}"))
    print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» IP Local: {getLocalIp()}"))
    print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» IP Public: {getPublicIp()}"))
    try:
        location_info = getLocationInfo()
        print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Location Info: {location_info['city']}, {location_info['country']} | {location_info['timezone']} | {location_info['org']}"))
    except Exception:
        print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Không thể lấy thông tin địa chỉ"))
    print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Đang tạo tài khoản thứ #{account_number}"))
    print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Uptime: {formatUptime()}"))

    defaultFirefoxPath = r"C:\\Program Files\\Mozilla Firefox\\private_browsing.exe"
    defaultEdgePath = r"C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
    defaultBravePath = r"C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
    defaultCocCocPath = r"C:\\Program Files\\CocCoc\\Browser\\Application\\browser.exe"
    defaultOperaPath = r"C:\\Users\\kiet0\\AppData\\Local\\Programs\\Opera\\opera.exe"
    defaultChromePath = r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    defaultUrl = "https://discord.com/register"

    configValue: str | None = None
    edgeConfigValue: str | None = None
    braveConfigValue: str | None = None
    coccocConfigValue: str | None = None
    operaConfigValue: str | None = None
    chromeConfigValue: str | None = None
    url_to_open: str = defaultUrl
    
    if not config.exists():
        print(màu("[>] Không tìm thấy file config.json, thoát chương trình"))
        sys.exit(1)
    
    try:
        with config.open("r", encoding="utf-8") as f:
            data = json.load(f)
            configValue = data.get("FireFoxPath")
            edgeConfigValue = data.get("edgePath")
            braveConfigValue = data.get("bravePath")
            coccocConfigValue = data.get("coccocPath")
            operaConfigValue = data.get("operaPath")
            chromeConfigValue = data.get("chromePath")
            url_to_open = data.get("urlRegisterDiscord", defaultUrl)
                
    except json.JSONDecodeError:
        print(màu("[>] File config.json không hợp lệ"))
        sys.exit(1)
    except Exception as e:
        print(màu(f"[>] Lỗi khi đọc config.json: {e}"))
        sys.exit(1)

    global selectedBrowser, isRotationMode, browserRotationList
    
    if isRotationMode:
        if not browserRotationList:
            print(màu("[!] Lỗi: Chế độ xoay vòng được bật nhưng không có trình duyệt nào được chọn. Quay lại Firefox."))
            browser_type = "firefox"
        else:
            browser_index = (account_number - 1) % len(browserRotationList)
            browser_type = browserRotationList[browser_index]
            print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Sử dụng trình duyệt {browser_type} cho tài khoản #{account_number}"))
    else:
        browser_type = selectedBrowser
    
    browser_name = ""
    browser_args = []
    
    if browser_type == "firefox":
        BrowserPath = Path(configValue or defaultFirefoxPath)
        browser_name = "Firefox Private"
        browser_args = [str(BrowserPath), url_to_open]
    elif browser_type == "edge":
        BrowserPath = Path(edgeConfigValue or defaultEdgePath)
        browser_name = "Edge Private"
        browser_args = [str(BrowserPath), "--inprivate", url_to_open]
    elif browser_type == "brave":
        BrowserPath = Path(braveConfigValue or defaultBravePath)
        browser_name = "Brave Private"
        browser_args = [str(BrowserPath), "--incognito", url_to_open]
    elif browser_type == "coccoc":
        BrowserPath = Path(coccocConfigValue or defaultCocCocPath)
        browser_name = "CocCoc Private"
        browser_args = [str(BrowserPath), "--incognito", url_to_open]
    elif browser_type == "opera":
        BrowserPath = Path(operaConfigValue or defaultOperaPath)
        browser_name = "Opera Private"
        browser_args = [str(BrowserPath), "--private", url_to_open]
    elif browser_type == "chrome":
        BrowserPath = Path(chromeConfigValue or defaultChromePath)
        browser_name = "Chrome Private"
        browser_args = [str(BrowserPath), "--incognito", url_to_open]
    else:
        BrowserPath = Path(configValue or defaultFirefoxPath)
        browser_name = "Firefox Private"
        browser_args = [str(BrowserPath), url_to_open]
    
    try:
        global browserExePath
        browserExePath = str(BrowserPath)
    except Exception:
        pass

    if not BrowserPath.exists():
        print(màu(f"Không tìm thấy tệp thực thi: {BrowserPath}"))
        return

    try:
        now = time.strftime("%H:%M:%S")
        print(màu(f"[ {now} ] »» Đang mở {browser_name}..."))
        subprocess.Popen(browser_args, shell=False)
        if browser_type == "edge":
            edgePrivateWindowOpened = True
        if url_to_open == "https://discord.com/register":
            global creation_start_ts
            creation_start_ts = time.time()
            time.sleep(8)
            display_name = ""
            user_name = ""
            password = ""
            email_addr = ""
            try:
                random_script = str((scriptDir / "modules" / "rdusername.py").resolve())
                
                if not Path(random_script).exists():
                    print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Module rdusername.py không tồn tại"))
                    try:
                        rand_num = random.randint(1010, 99999)
                        user_name = f"user{rand_num}"
                        print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Generated fallback username: {user_name}"))
                    except Exception:
                        pass
                else:
                    if getattr(sys, 'frozen', False):
                        python_exe = scriptDir / "python.exe"
                        if python_exe.exists():
                            python_cmd = str(python_exe)
                        else:
                            python_cmd = "python"
                    else:
                        python_cmd = sys.executable
                        
                    result = subprocess.run(
                        [python_cmd, random_script],
                        shell=False,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        encoding="utf-8",
                        timeout=30
                    )
                if result.returncode == 0 and result.stdout.strip():
                    try:
                        new_username = result.stdout.strip()
                        print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Generated username: {new_username}"))
                    except Exception:
                        pass
            except subprocess.TimeoutExpired:
                print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Timeout khi tạo username"))
            except Exception as e:
                print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Lỗi khi tạo username: {e}"))
            if config.exists():
                try:
                    with config.open("r", encoding="utf-8") as f:
                        cfg = json.load(f)
                        if isinstance(cfg.get("displayName"), str):
                            display_name = cfg.get("displayName")
                        if isinstance(cfg.get("userName"), str):
                            user_name = cfg.get("userName")
                        if isinstance(cfg.get("password"), str):
                            password = cfg.get("password")
                        try:
                            rd_icon_value = cfg.get("rdIcon", True)
                            if isinstance(rd_icon_value, str):
                                rd_icon_enabled = rd_icon_value.lower() in ("true", "1", "yes", "on")
                            else:
                                rd_icon_enabled = bool(rd_icon_value)
                            rd_icon_style = cfg.get("rdIconStyle", "both")
                        except Exception:
                            rd_icon_enabled = True
                            rd_icon_style = "both"
                except Exception:
                    pass
            if not user_name:
                try:
                    rand_num = random.randint(1010, 99999)
                    user_name = f"user{rand_num}"
                except Exception:
                    pass

            try:
                now_user = time.strftime("%H:%M:%S")
                print(màu(f"[ {now_user} ] »» Using UserName: {user_name}"))
            except Exception:
                pass
            mailverify_choice = None
            try:
                with config.open("r", encoding="utf-8") as f:
                    cfg_mv = json.load(f)
                    mv_val = cfg_mv.get("mailverify")
                    if isinstance(mv_val, str) and mv_val.strip():
                        mailverify_choice = mv_val.strip()
                    elif mv_val is None:
                        mailverify_choice = None
            except Exception:
                pass

            if mailverify_choice and mailverify_choice.lower() == "hotmail.py":
                _HotmailGraphClient = HotmailGraphClient or loadEncryptedModule("hotmail")
                if _HotmailGraphClient is not None:
                    picked = _pop_first_email_cred(scriptDir)
                    if picked is None:
                        print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Không có dòng hợp lệ trong email.txt"))
                        result_queue.put("continue")
                    else:
                        email_addr, password, refresh_token, client_id = picked
                        try:
                            client = _HotmailGraphClient(email_addr, refresh_token, client_id)
                        except Exception as e:
                            print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Khởi tạo HotmailGraphClient thất bại: {e}"))
                            result_queue.put("continue")
                            client = None
                        if client is not None:
                            wait_printed_flag = False
                            def _monitor_hotmail_graph() -> None:
                                opened = False
                                deadline = time.time() + 300
                                while time.time() < deadline and not opened:
                                    try:
                                        url = client.find_verification_link()
                                    except Exception:
                                        url = None
                                    if url:
                                        try:
                                            ts = time.strftime("%H:%M:%S")
                                            print(màu(f"[ {ts} ] »» Open Verify link: {url}"))
                                            global edgePrivateWindowOpened
                                            browser_args = [str(BrowserPath)]
                                            if browser_type == "edge":
                                                browser_args.append("--inprivate")
                                            elif browser_type in ["brave", "coccoc", "chrome"]:
                                                browser_args.append("--incognito")
                                            elif browser_type == "opera":
                                                browser_args.append("--private")
                                            browser_args.append(url)
                                            subprocess.Popen(browser_args, shell=False)
                                            opened = True
                                            verify_delay = 10 if inviteUrlsGlobal else 17
                                            time.sleep(verify_delay)
                                            
                                            try:
                                                print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Mở Discord để lấy token"))
                                                browser_args = [str(BrowserPath)]
                                                if browser_type == "edge":
                                                    browser_args.append("--inprivate")
                                                elif browser_type in ["brave", "coccoc", "chrome"]:
                                                    browser_args.append("--incognito")
                                                elif browser_type == "opera":
                                                    browser_args.append("--private")
                                                browser_args.append("https://discord.com/channels/@me")
                                                subprocess.Popen(browser_args, shell=False)
                                            except Exception:
                                                pass
                                            time.sleep(7)
                                            try:
                                                token_saved = _copy_token_from_popup(email_addr, password, display_name, user_name)
                                                if not token_saved:
                                                    print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Token không được lưu"))
                                            except Exception as e:
                                                print(màu(f"Lỗi khi copy token: {e}"))
                                            try:
                                                global lastToggledAccount
                                                if not inviteUrlsGlobal and isVpnEnabled():
                                                    if lastToggledAccount != account_number:
                                                        desired_on = (account_number % 2) == 1
                                                        current_status = getWarpStatus()
                                                        if desired_on:
                                                            if current_status != "connected":
                                                                print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Đang bật 1.1.1.1 WARP..."))
                                                                vpnConnect()
                                                                current_status = getWarpStatus()
                                                            if current_status == "connected":
                                                                warpStatus = True
                                                                print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Đã bật 1.1.1.1 WARP thành công!"))
                                                        else:
                                                            if current_status == "connected":
                                                                print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Đang tắt 1.1.1.1 WARP..."))
                                                                vpnDisconnect()
                                                                current_status = getWarpStatus()
                                                            if current_status != "connected":
                                                                warpStatus = False
                                                                print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Đã tắt 1.1.1.1 WARP thành công!"))
                                                        lastToggledAccount = account_number
                                            except Exception:
                                                pass
                                            try:
                                                
                                                prompt = f"[ {time.strftime('%H:%M:%S')} ] »» Tiếp tục reg token? (y/n): "
                                                ans = inputWthTimeout(prompt, 300)
                                                if ans is None:
                                                    print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Hết thời gian chờ (5 phút), dừng chương trình."))
                                                    result_queue.put("exit")
                                                    
                                                else:
                                                    ans_l = ans.strip().lower()
                                                    if ans_l in ['y', 'yes', 'có', 'c']:
                                                        print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Tiếp tục tạo tài khoản mới..."))
                                                        result_queue.put("continue")
                                                    else:
                                                        print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Dừng chương trình"))
                                                        result_queue.put("exit")
                                            except Exception:
                                                print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Tiếp tục tạo tài khoản mới..."))
                                                result_queue.put("continue")
                                        except Exception as e:
                                            print(màu(f"Failed to open verify link: {e}"))
                                            result_queue.put("error")
                                            break
                                    time.sleep(2)
                                if not opened:
                                    print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Không tìm thấy link verify trong thời gian chờ"))
                                    result_queue.put("continue")
                            def _start_hotmail_monitor_later() -> None:
                                nonlocal wait_printed_flag
                                while not wait_printed_flag:
                                    time.sleep(0.2)
                                threading.Thread(target=_monitor_hotmail_graph, daemon=True).start()
                            threading.Thread(target=_start_hotmail_monitor_later, daemon=True).start()
            elif mailverify_choice and mailverify_choice.lower() in ("tmail.py", "apimail.py"):
                try:
                    chosen_module = mailverify_choice.lower()
                    email_script_path = (scriptDir / "modules" / chosen_module).resolve()
                    email_script = str(email_script_path)
                    
                    if not Path(email_script).exists():
                        print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Module {chosen_module} không tồn tại"))
                        result_queue.put("continue")
                    else:
                        if getattr(sys, 'frozen', False):
                            python_exe = scriptDir / "python.exe"
                            if python_exe.exists():
                                python_cmd = str(python_exe)
                            else:
                                python_cmd = "python"
                        else:
                            python_cmd = sys.executable
                            
                        proc = subprocess.Popen(
                            [python_cmd, "-u", email_script, "100"],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            text=True,
                            encoding="utf-8",
                            shell=False,
                        )

                    lines_q: "queue.Queue[str]" = queue.Queue()

                    def reader(p: subprocess.Popen) -> None:
                        try:
                            assert p.stdout is not None
                            for line in p.stdout:
                                lines_q.put(line)
                        except Exception:
                            pass

                    threading.Thread(target=reader, args=(proc,), daemon=True).start()

                    ansi_re = re.compile(r"\x1B\[[0-9;]*[mK]")
                    deadline = time.time() + 15
                    while time.time() < deadline and not email_addr:
                        try:
                            line = lines_q.get(timeout=0.5)
                        except queue.Empty:
                            continue
                        clean = ansi_re.sub("", line)
                        m = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", clean)
                        if m:
                            email_addr = m.group(0)
                            break

                    def _monitor_verify_links() -> None:
                        opened = False
                        url_pattern = re.compile(r"https?://[\w\-._~:/?#\[\]@!$&'()*+,;=%]+", re.IGNORECASE)
                        priorities = ("discord.com", "click.discord.com", "discordapp.com")
                        deadline = time.time() + 300
                        while time.time() < deadline and not opened:
                            try:
                                line2 = lines_q.get(timeout=1)
                            except queue.Empty:
                                continue
                            try:
                                clean2 = ansi_re.sub("", line2).strip()
                                url: str | None = None
                                if "Link Very =" in clean2:
                                    try:
                                        url = clean2.split("=", 1)[1].strip()
                                    except Exception:
                                        url = None
                                if not url:
                                    m2 = url_pattern.search(clean2)
                                    if m2:
                                        u = m2.group(0)
                                        if any(p in u.lower() for p in priorities):
                                            url = u
                                if url and not opened:
                                    try:
                                        ts = time.strftime("%H:%M:%S")
                                        print(màu(f"[ {ts} ] »» Open Verify link: {url}"))
                                        global edgePrivateWindowOpened
                                        browser_args = [str(BrowserPath)]
                                        if browser_type == "edge":
                                            browser_args.append("--inprivate")
                                        elif browser_type in ["brave", "coccoc", "chrome"]:
                                            browser_args.append("--incognito")
                                        elif browser_type == "opera":
                                            browser_args.append("--private")
                                        browser_args.append(url)
                                        subprocess.Popen(browser_args, shell=False)
                                        opened = True
                                        verify_delay = 10 if inviteUrlsGlobal else 17
                                        time.sleep(verify_delay)
                                        
                                        try:
                                            print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Mở Discord để lấy token"))
                                            browser_args = [str(BrowserPath)]
                                            if browser_type == "edge":
                                                browser_args.append("--inprivate")
                                            elif browser_type in ["brave", "coccoc", "chrome"]:
                                                browser_args.append("--incognito")
                                            elif browser_type == "opera":
                                                browser_args.append("--private")
                                            browser_args.append("https://discord.com/channels/@me")
                                            subprocess.Popen(browser_args, shell=False)
                                        except Exception:
                                            pass
                                        time.sleep(7)

                                        try:
                                            token_saved = _copy_token_from_popup(email_addr, password, display_name, user_name)
                                            if token_saved:
                                                if not inviteUrlsGlobal and isVpnEnabled():
                                                    manageWarp()
                                            else:
                                                print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Token không được lưu"))
                                        except Exception as e:
                                            print(màu(f"Lỗi khi copy token: {e}"))
                                        
                                        try:
                                            global lastToggledAccount
                                            if isVpnEnabled() and lastToggledAccount != account_number:
                                                desired_on = (account_number % 2) == 1
                                                current_status = getWarpStatus()
                                                if desired_on:
                                                    if current_status != "connected":
                                                        print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Đang bật 1.1.1.1 WARP..."))
                                                        vpnConnect()
                                                        current_status = getWarpStatus()
                                                    if current_status == "connected":
                                                        warpStatus = True
                                                        print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Đã bật 1.1.1.1 WARP thành công!"))
                                                else:
                                                    if current_status == "connected":
                                                        print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Đang tắt 1.1.1.1 WARP..."))
                                                        vpnDisconnect()
                                                        current_status = getWarpStatus()
                                                    if current_status != "connected":
                                                        warpStatus = False
                                                        print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Đã tắt 1.1.1.1 WARP thành công!"))
                                                lastToggledAccount = account_number
                                        except Exception:
                                            pass
                                        time.sleep(2)
                                        
                                        try:
                                            if not askEach:
                                                result_queue.put("continue")
                                            else:
                                                prompt = f"[ {time.strftime('%H:%M:%S')} ] »» Tiếp tục reg token? (y/n): "
                                                ans = inputWthTimeout(prompt, 300)
                                                if ans is None:
                                                    print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Hết thời gian chờ, dừng chương trình."))
                                                    result_queue.put("exit")
                                                else:
                                                    ans_l = ans.strip().lower()
                                                    if ans_l in ['y', 'yes', 'có', 'c']:
                                                        print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Tiếp tục tạo tài khoản mới..."))
                                                        result_queue.put("continue")
                                                    else:
                                                        print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Dừng chương trình"))
                                                        result_queue.put("exit")
                                        except Exception:
                                            print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Tiếp tục tạo tài khoản mới..."))
                                            result_queue.put("continue")
                                    except Exception as e:
                                        print(màu(f"Failed to open verify link: {e}"))
                                        result_queue.put("error")
                            except Exception:
                                continue
                        if not opened:
                            result_queue.put("continue")
                    
                    threading.Thread(target=_monitor_verify_links, daemon=True).start()
                except Exception:
                    pass
            else:
                try:
                    email_result, email_id_result = _mail_create_email_only()
                    if email_result:
                        email_addr = email_result
                    else:
                        result_queue.put("continue")
                        return
                    
                    def _monitor_mail_verify() -> None:
                        nonlocal email_addr
                        opened = False
                        try:
                            if not email_id_result:
                                result_queue.put("continue")
                                return
                            verify_url_result = get_email_and_verify_link_mail(email_id_result, 100)
                            if verify_url_result and not opened:
                                try:
                                    ts = time.strftime("%H:%M:%S")
                                    print(màu(f"[ {ts} ] »» Open Verify link: {verify_url_result}"))
                                    global edgePrivateWindowOpened
                                    browser_args = [str(BrowserPath)]
                                    if browser_type == "edge":
                                        browser_args.append("--inprivate")
                                    elif browser_type in ["brave", "coccoc", "chrome"]:
                                        browser_args.append("--incognito")
                                    elif browser_type == "opera":
                                        browser_args.append("--private")
                                    browser_args.append(verify_url_result)
                                    subprocess.Popen(browser_args, shell=False)
                                    opened = True
                                    verify_delay = 10 if inviteUrlsGlobal else 17
                                    time.sleep(verify_delay)
                                    
                                    try:
                                        print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Mở Discord để lấy token"))
                                        browser_args = [str(BrowserPath)]
                                        if browser_type == "edge":
                                            browser_args.append("--inprivate")
                                        elif browser_type in ["brave", "coccoc", "chrome"]:
                                            browser_args.append("--incognito")
                                        elif browser_type == "opera":
                                            browser_args.append("--private")
                                        browser_args.append("https://discord.com/channels/@me")
                                        subprocess.Popen(browser_args, shell=False)
                                    except Exception:
                                        pass
                                    time.sleep(7)

                                    try:
                                        token_saved = _copy_token_from_popup(email_addr, password, display_name, user_name)
                                        if token_saved:
                                            if not inviteUrlsGlobal and isVpnEnabled():
                                                manageWarp()
                                        else:
                                            print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Token không được lưu"))
                                    except Exception as e:
                                        print(màu(f"Lỗi khi copy token: {e}"))
                                    
                                    try:
                                        global lastToggledAccount
                                        if isVpnEnabled() and lastToggledAccount != account_number:
                                            desired_on = (account_number % 2) == 1
                                            current_status = getWarpStatus()
                                            if desired_on:
                                                if current_status != "connected":
                                                    print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Đang bật 1.1.1.1 WARP..."))
                                                    vpnConnect()
                                                    current_status = getWarpStatus()
                                                if current_status == "connected":
                                                    warpStatus = True
                                                    print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Đã bật 1.1.1.1 WARP thành công!"))
                                            else:
                                                if current_status == "connected":
                                                    print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Đang tắt 1.1.1.1 WARP..."))
                                                    vpnDisconnect()
                                                    current_status = getWarpStatus()
                                                if current_status != "connected":
                                                    warpStatus = False
                                                    print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Đã tắt 1.1.1.1 WARP thành công!"))
                                            lastToggledAccount = account_number
                                    except Exception:
                                        pass
                                    time.sleep(2)
                                    
                                    try:
                                        if not askEach:
                                            result_queue.put("continue")
                                        else:
                                            prompt = f"[ {time.strftime('%H:%M:%S')} ] »» Tiếp tục reg token? (y/n): "
                                            ans = inputWthTimeout(prompt, 300)
                                            if ans is None:
                                                print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Hết thời gian chờ, dừng chương trình."))
                                                result_queue.put("exit")
                                            else:
                                                ans_l = ans.strip().lower()
                                                if ans_l in ['y', 'yes', 'có', 'c']:
                                                    print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Tiếp tục tạo tài khoản mới..."))
                                                    result_queue.put("continue")
                                                else:
                                                    print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Dừng chương trình"))
                                                    result_queue.put("exit")
                                    except Exception:
                                        print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Tiếp tục tạo tài khoản mới..."))
                                        result_queue.put("continue")
                                except Exception as e:
                                    print(màu(f"Failed to open verify link: {e}"))
                                    result_queue.put("error")
                            else:
                                if not verify_url_result:
                                    result_queue.put("continue")
                        except Exception as e:
                            result_queue.put("continue")
                    
                    threading.Thread(target=_monitor_mail_verify, daemon=True).start()
                except Exception:
                    pass

            try:
                now_info = time.strftime("%H:%M:%S")
                details = (
                    f"[ {now_info} ] »» Infomation:\n"
                    f"[ {now_info} ] »» Email: {email_addr}\n"
                    f"[ {now_info} ] »» DisplayName: {display_name}\n"
                    f"[ {now_info} ] »» UserName: {user_name}\n"
                    f"[ {now_info} ] »» Password: {password}"
                )
                print(màu(details))
            except Exception:
                pass

            if pyautogui is None or pyperclip is None:
                if pyperclip is None:
                    print(màu("Thiếu thư viện pyperclip. Vui lòng cài đặt: pip install pyperclip"))
                if pyautogui is None:
                    print(màu("Thiếu thư viện pyautogui. Vui lòng cài đặt: pip install pyautogui"))
            else:
                try:
                    time.sleep(0.00001)
                    pyperclip.copy(email_addr)
                    
                    pyautogui.hotkey("ctrl", "v")
                    pyautogui.press("tab")
                    try:
                        _decorate = decorateDisplayName
                        if rd_icon_enabled and _decorate is None:
                            _decorate = loadEncryptedModule("rdicon")
                        if _decorate and rd_icon_enabled:
                            dn = _decorate(display_name or "", rd_icon_style)
                        else:
                            dn = display_name
                    except Exception:
                        dn = display_name
                    pyperclip.copy(dn)
                    pyautogui.hotkey("ctrl", "v")
                    pyautogui.press("tab")
                    pyautogui.hotkey("ctrl", "a")
                    pyautogui.press("backspace")
                    if pyperclip is not None:
                        pyperclip.copy(user_name)
                        pyautogui.hotkey("ctrl", "v")
                    pyautogui.press("tab")
                    pyperclip.copy(password)
                    pyautogui.hotkey("ctrl", "v")
                    
                    pyautogui.press("tab")
                    import calendar
                    import random
                    current_year = time.localtime().tm_year
                    min_year = 1900
                    max_year = current_year - 18
                    year_val = random.randint(max(1990, min_year), max_year)
                    month_val = random.randint(1, 12)
                    day_val = random.randint(1, 28)
                    month_name = calendar.month_name[month_val]
                    month_abbr = calendar.month_abbr[month_val]
                    pyautogui.press("space")
                    time.sleep(0.00001)
                    try:
                        down_presses = max(0, month_val - 1)
                    except Exception:
                        down_presses = 0
                    pyautogui.press("home")
                    time.sleep(0.00005)
                    if down_presses > 0:
                        pyautogui.press("down", presses=down_presses, interval=0.01)
                    time.sleep(0.00001)
                    pyautogui.press("enter")
                    time.sleep(0.00001)
                    pyautogui.press("tab")
                    pyautogui.typewrite(str(day_val))
                    
                    pyautogui.press("tab")
                    pyautogui.typewrite(str(year_val))
                    time.sleep(0.00001)
                    pyautogui.press("tab")
                    time.sleep(0.00002)
                    pyautogui.press("space")
                    try:
                        now_dob = time.strftime("%H:%M:%S")
                        dob_line = (
                            f"[ {now_dob} ] »» Ngày sinh: {month_abbr} {day_val}, {year_val}"
                        )
                        print(màu(dob_line))
                    except Exception:
                        pass
                    try:
                        time.sleep(0.00001)
                        pyautogui.press("tab", presses=3, interval=0.00001)
                        time.sleep(0.00001)
                        pyautogui.press("enter")
                        try:
                            now_submit = time.strftime("%H:%M:%S")
                            print(màu(f"[ {now_submit} ] »» Click create account"))
                            print(màu(f"[ {now_submit} ] »» Hãy giải hcaptcha!"))
                            time.sleep(15)
                            try:
                                wait_printed_flag = True
                            except Exception:
                                pass
                        except Exception:
                            pass
                    except Exception:
                        pass
                except Exception:
                    print(màu("Không thể tự động điền vào form."))
    except Exception as exc:
        print(màu(f"Không thể khởi chạy chế độ duyệt riêng tư của Firefox: {exc}"))
        return "error"
    try:
        result = result_queue.get(timeout=300)
        return result
    except queue.Empty:
        return "continue"

def _reg_token_flow() -> None:
    total_to_create: int | None = None
    while total_to_create is None:
        try:
            ans = input(màu("[>] Bạn muốn tạo bao nhiêu tokens? (0 = không giới hạn): ")).strip()
        except Exception:
            ans = ""
        if not ans:
            continue
        if ans.isdigit():
            try:
                total_to_create = int(ans)
            except Exception:
                total_to_create = None
        else:
            print(màu("Vui lòng nhập số hợp lệ!"))
            total_to_create = None
    
    global askEach
    askEach = False
    created_count = 0
    
    while True:
        if (isinstance(total_to_create, int) and total_to_create > 0 and created_count >= total_to_create):
            print(màu("Đã đạt số lượng tài khoản yêu cầu. Kết thúc chương trình."))
            return
        
        result = main(created_count + 1)
        if result == "waiting":
            print(màu("Đang chờ quá trình verify email và lưu token..."))
            continue
        elif result == "continue":
            try:
                ts_clear = time.strftime("%H:%M:%S")
                time.sleep(1)
                
                active_threads = threading.enumerate()
                thread_count = 0
                for thread in active_threads:
                    if thread != threading.current_thread() and thread.is_alive():
                        try:
                            thread._stop() 
                            thread_count += 1
                        except Exception:
                            pass

                is_mode_2 = len(inviteUrlsGlobal) > 0
                delay_time = 0.8 if is_mode_2 else 3.0
                
                print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Tạo tài khoản thành công!"))
                _kill_browser_processes()
                try:
                    if getattr(sys, 'frozen', False):
                        scriptDir = Path(sys.executable).parent
                    else:
                        scriptDir = Path(__file__).resolve().parent
                    
                    token_dir = scriptDir / "token"
                    target_name = tokenSaveFilename if tokenSaveFilename else "tokens.txt"
                    token_file = token_dir / target_name
                    
                    if token_file.exists():
                        with token_file.open("r", encoding="utf-8") as f:
                            lines = [line.strip() for line in f.readlines() if line.strip()]
                            if lines:
                                last_line = lines[-1]
                                if "|" in last_line:
                                    token = last_line.split("|")[0]
                                    setTokenBioAndPronouns(token)
                                    checkTokenInfo(token)
                except Exception as e:
                    print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Lỗi khi set bio/pronouns: {e}"))
                try:
                    elapsed = int(time.time() - creation_start_ts)
                    mins, secs = divmod(elapsed, 60)
                    print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Thời gian tạo: {mins} phút {secs} giây"))
                except Exception:
                    pass
                if thread_count > 0:
                    print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Đã dừng {thread_count} threads"))
                print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Đang dọn dẹp để tạo tài khoản mới"))
                time.sleep(delay_time)
                clearScreen()
                _banner()
                created_count += 1
                
            except Exception as e:
                print(màu(f"Lỗi khi chuẩn bị tài khoản mới: {e}"))
            continue
        elif result == "completed":
            print(màu("Hoàn thành tạo tài khoản. Tiếp tục tạo tài khoản mới..."))
            continue
        elif result == "exit":
            print(màu("Kết thúc chương trình."))
            return
        elif result == "error":
            print(màu("Có lỗi xảy ra. Kết thúc chương trình."))
            return

if __name__ == "__main__":
    startUptimeTitle()
    bannerkey()
    verifyKey()
    
    if isVpnEnabled():
        vpnDisconnect()
    else:
        pass
    
    while True:
        choice = showMenu()
        
        if choice == '1':
            selectedBrowser = selectBrowser()
            print(màu(f"\n[ {time.strftime('%H:%M:%S')} ] »» Chuẩn bị reg token, hãy chọn số lượng..."))
            inviteUrlsGlobal = []
            tokenSaveFilename = "tokennew.txt"
            _reg_token_flow()
            
        elif choice == '2':
            inviteUrlsGlobal = []
            print(màu("\n" + "="*70))
            print(màu(" " * 22 + "CHỌN SỐ LƯỢNG SERVER" + " " * 22))
            print(màu("="*70))
            print(màu(""))
            print(màu("  1. 1 Server duy nhất"))
            print(màu("  2. Nhiều Server"))
            print(màu(""))
            print(màu("="*70))
            
            while True:
                try:
                    server_choice = input(màu("[>] Bạn muốn join bao nhiêu server? (1-2): ")).strip()
                    if server_choice in ['1', '2']:
                        break
                    else:
                        print(màu("Vui lòng chọn 1 hoặc 2!"))
                except KeyboardInterrupt:
                    print(màu("\n[>] Hủy chọn server"))
                    break
                except Exception:
                    print(màu("Lỗi nhập liệu, vui lòng thử lại!"))
            if server_choice == '1':
                saved_links = loadSavedInviteLinks()
                single_servers = [link for link in saved_links if link.get('type') == 'single']
                
                if single_servers:
                    print(màu("\n[>] Các server đã lưu trước đó:"))
                    for i, server in enumerate(single_servers, 1):
                        print(màu(f"  {i}. {server.get('server_name', 'Unknown')} - {server.get('link', '')}"))
                    
                    while True:
                        try:
                            use_saved = input(màu("\n[>] Bạn có muốn dùng server đã lưu? (y/n): ")).strip().lower()
                            if use_saved in ['y', 'yes']:
                                while True:
                                    try:
                                        choice = int(input(màu("[>] Chọn server (số thứ tự): ")).strip())
                                        if 1 <= choice <= len(single_servers):
                                            selected_server = single_servers[choice - 1]
                                            inviteUrlsGlobal = [selected_server['link']]
                                            print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Đã chọn: {selected_server.get('server_name', 'Unknown')}"))
                                            break
                                        else:
                                            print(màu("Số thứ tự không hợp lệ!"))
                                    except ValueError:
                                        print(màu("Vui lòng nhập số!"))
                                    except KeyboardInterrupt:
                                        print(màu("\n[>] Hủy chọn server"))
                                        break
                                break
                            elif use_saved in ['n', 'no']:
                                break
                            else:
                                print(màu("Vui lòng chọn y hoặc n!"))
                        except KeyboardInterrupt:
                            print(màu("\n[>] Hủy chọn"))
                            break
                
                if not single_servers or use_saved in ['n', 'no']:
                    while True:
                        try:
                            invite_link = input(màu("[>] Nhập link invite server: ")).strip()
                            if not invite_link:
                                print(màu("Link không được để trống!"))
                                continue
                            if not invite_link.startswith("http"):
                                print(màu("Link phải bắt đầu bằng http hoặc https!"))
                                continue
                            inviteUrlsGlobal = [invite_link]
                            print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Đã lưu link: {invite_link}"))
                            new_link = {
                                "link": invite_link,
                                "server_name": getServerNameFromInvite(invite_link.split('/')[-1]),
                                "invite_code": invite_link.split('/')[-1],
                                "type": "single"
                            }
                            saved_links.append(new_link)
                            saveInviteLinksWithType(saved_links)
                            break
                        except KeyboardInterrupt:
                            print(màu("\n[>] Hủy nhập link"))
                            break
                        except Exception as e:
                            print(màu(f"Lỗi nhập liệu: {e}"))
                        
            else:
                saved_links = loadSavedInviteLinks()
                multi_servers = [link for link in saved_links if link.get('type') == 'multi']
                
                print(màu(f"[DEBUG] Tổng số links đã lưu: {len(saved_links)}"))
                print(màu(f"[DEBUG] Số multi servers: {len(multi_servers)}"))
                
                if multi_servers:
                    print(màu("\n[>] Các nhóm server đã lưu trước đó:"))
                    for i, server_group in enumerate(multi_servers, 1):
                        server_names = server_group.get('server_names', [])
                        print(màu(f"  {i}. {', '.join(server_names)} ({len(server_names)} servers)"))
                    
                    while True:
                        try:
                            use_saved = input(màu("\n[>] Bạn có muốn dùng nhóm server đã lưu? (y/n): ")).strip().lower()
                            if use_saved in ['y', 'yes']:
                                while True:
                                    try:
                                        choice = int(input(màu("[>] Chọn nhóm server (số thứ tự): ")).strip())
                                        if 1 <= choice <= len(multi_servers):
                                            selected_group = multi_servers[choice - 1]
                                            inviteUrlsGlobal = selected_group['links']
                                            print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Đã chọn: {', '.join(selected_group.get('server_names', []))}"))
                                            break
                                        else:
                                            print(màu("Số thứ tự không hợp lệ!"))
                                    except ValueError:
                                        print(màu("Vui lòng nhập số!"))
                                    except KeyboardInterrupt:
                                        print(màu("\n[>] Hủy chọn nhóm server"))
                                        break
                                break
                            elif use_saved in ['n', 'no']:
                                break
                            else:
                                print(màu("Vui lòng chọn y hoặc n!"))
                        except KeyboardInterrupt:
                            print(màu("\n[>] Hủy chọn"))
                            break
                
                if not multi_servers or use_saved in ['n', 'no']:
                    while True:
                        try:
                            num_links = input(màu("[>] Bạn muốn nhập bao nhiêu link invite? ")).strip()
                            if not num_links:
                                print(màu("Số lượng không được để trống!"))
                                continue
                            if not num_links.isdigit():
                                print(màu("Vui lòng nhập số!"))
                                continue
                            num_links = int(num_links)
                            if num_links <= 0:
                                print(màu("Số lượng phải lớn hơn 0!"))
                                continue
                            break
                        except KeyboardInterrupt:
                            print(màu("\n[>] Hủy nhập số lượng"))
                            break
                        except Exception as e:
                            print(màu(f"Lỗi nhập liệu: {e}"))
                    
                    if num_links <= 0:
                        continue
                    
                    print(màu(f"\n[>] Nhập {num_links} link invite:"))
                    invite_links = []
                    
                    for i in range(num_links):
                        while True:
                            try:
                                invite_link = input(màu(f"[>] Link #{i+1}/{num_links}: ")).strip()
                                
                                if not invite_link:
                                    print(màu("Link không được để trống!"))
                                    continue
                                    
                                if not invite_link.startswith("http"):
                                    print(màu("Link phải bắt đầu bằng http hoặc https!"))
                                    continue
                                    
                                invite_links.append(invite_link)
                                print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Đã lưu link #{i+1}: {invite_link}"))
                                break
                                
                            except KeyboardInterrupt:
                                print(màu("\n[>] Hủy nhập link"))
                                break
                            except Exception as e:
                                print(màu(f"Lỗi nhập liệu: {e}"))
                        
                        if len(invite_links) < i + 1:
                            break
                    
                    inviteUrlsGlobal = invite_links
                    print(màu(f"[ {time.strftime('%H:%M:%S')} ] »» Đã lưu tổng cộng {len(invite_links)} link invite"))
                    server_names = []
                    for link in invite_links:
                        server_name = getServerNameFromInvite(link.split('/')[-1])
                        server_names.append(server_name)
                    
                    new_group = {
                        "links": invite_links,
                        "server_names": server_names,
                        "type": "multi"
                    }
                    saved_links.append(new_group)
                    saveInviteLinksWithType(saved_links)
            print(màu(f"\n[ {time.strftime('%H:%M:%S')} ] »» Chọn file lưu token..."))
            tokenSaveFilename = selectTokenFile()
            selectedBrowser = selectBrowser()
            print(màu(f"\n[ {time.strftime('%H:%M:%S')} ] »» Chuẩn bị reg token, hãy chọn số lượng..."))
            _reg_token_flow()
            
        elif choice == '3':
            print(màu(f"\n[ {time.strftime('%H:%M:%S')} ] »» Bắt đầu kiểm tra token..."))
            checkVerification()
            input(màu("\n[>] Nhấn Enter để quay lại menu..."))
            clearScreen()
            ShowMainBanner()
            
        elif choice == '4':
            print(màu(f"\n[ {time.strftime('%H:%M:%S')} ] »» Bắt đầu setup config..."))
            setupConfig()
            input(màu("\n[>] Nhấn Enter để quay lại menu..."))
            clearScreen()
            ShowMainBanner()
            
        elif choice == '5':
            print(màu(f"\n[ {time.strftime('%H:%M:%S')} ] »» Thoát chương trình..."))
            sys.exit(0)