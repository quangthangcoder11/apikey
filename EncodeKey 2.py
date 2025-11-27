import hashlib
import base64
import marshal

def compute_md5_bytes(text: str) -> bytes:
    return hashlib.md5(text.encode()).digest()
def hash_sha256_layers(data: bytes, layers: int) -> bytes:
    result = data
    for _ in range(int(layers)):
        result = hashlib.sha256(result).digest()
    return result
def apply_a85_layers(data: bytes, layers: int) -> bytes:
    result = data
    for _ in range(int(layers)):
        result = base64.a85encode(result)
    return result
def apply_b85_layers(data: bytes, layers: int) -> bytes:
    result = data
    for _ in range(int(layers)):
        result = base64.b85encode(result)
    return result
def apply_marshal_layers(data: bytes, layers: int) -> bytes:
    result = data
    for _ in range(int(layers)):
        result = marshal.dumps(result)
        result = base64.b85encode(result)
    return result
def encode_key_v1(keyInput: str, a85_layers: int = 3, b85_layers: int = 3, marshal_layers: int = 2, sha256_layers: int = 3) -> str:
    md5_bytes = compute_md5_bytes(keyInput)
    sha_bytes = hash_sha256_layers(md5_bytes, sha256_layers)
    ascii_safe = base64.b64encode(sha_bytes)
    ascii_safe = apply_a85_layers(ascii_safe, a85_layers)
    ascii_safe = apply_b85_layers(ascii_safe, b85_layers)
    ascii_safe = apply_marshal_layers(ascii_safe, marshal_layers)
    final_text = base64.b64encode(ascii_safe).decode()
    return final_text
def encodeKey(keyInput, a85_layers=3, b85_layers=3, marshal_layers=2):
    return encode_key_v1(
        keyInput,
        a85_layers=a85_layers,
        b85_layers=b85_layers,
        marshal_layers=marshal_layers,
        sha256_layers=3,
    )

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
