import hashlib
import base64

def encodeKey(keyInput):
    md5 = hashlib.md5(keyInput.encode()).digest()
    sha256 = hashlib.sha256(md5).digest()
    b64 = base64.b64encode(sha256).decode()
    b85 = base64.b85encode(b64.encode()).decode()
    enCode = base64.b64encode(b85.encode()).decode()
    
    return enCode

def main():
    print()
    
    while True:
        keyInput = input("Nhập key cần encode (hoặc 'quit' để thoát): ").strip()
        
        if keyInput.lower() == 'quit':
            print("Tạm biệt!")
            break
            
        if not keyInput:
            print("Vui lòng nhập key!")
            continue
            
        try:
            enCode = encodeKey(keyInput)
            print(f"Key gốc: {keyInput}")
            print(f"Key đã encode: {enCode}")
            print("-" * 50)
        except Exception as e:
            print(f"Lỗi khi encode: {e}")

if __name__ == "__main__":
    main()
