import httpx
import base64
import hashlib
from bs4 import BeautifulSoup
import sys

def verify_key():
    url = "https://anotepad.com/notes/83hr53bq"

    try:
        response = httpx.get(url, timeout=10, verify=False)
        if response.status_code != 200:
            print("Ê bị xóa key hã?  Lh zalo: 0931833420 mua key đê")
            sys.exit(1)
    except Exception:
        print("! Lỗi khi kết nối.")
        sys.exit(1)

    soup = BeautifulSoup(response.text, 'html.parser')
    content_div = soup.find('div', {'class': 'plaintext'})

    if not content_div or not content_div.text.strip():
        print("Ê bị xóa key hã?  Lh zalo: 0831833420 mua key đê")
        sys.exit(1)

    anotepad_key = content_div.text.strip()

    InputKey = input("> Nhập key : ").strip()
    if not InputKey:
        print("> Đéo nhập mà đòi sài hã?.")
        sys.exit(1)

    md5 = hashlib.md5(InputKey.encode()).digest()
    sha256 = hashlib.sha256(md5).digest()
    b64 = base64.b64encode(sha256).decode()
    b85 = base64.b85encode(b64.encode()).decode()
    user_key_encoded = base64.b64encode(b85.encode()).decode()

    if user_key_encoded != anotepad_key:
        print("> Key không đúng ( sài chùa hã mày ? )")
        sys.exit(1)

    print("GOOD LUCK ! KEY HỢP LỆ ")

verify_key()