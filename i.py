import hashlib
import base64
import marshal
import zlib
import bz2
import lzma
import binascii

def compute_md5_bytes(text: str) -> bytes:
    return hashlib.md5(text.encode('utf-8')).digest()

def apply_xor_obfuscate(data: bytes, key: bytes) -> bytes:
    return bytes(a ^ b for a, b in zip(data, (key * (len(data) // len(key) + 1))[:len(data)]))

def encode_key_v5(
    keyInput: str,
    a85_layers: int = 6,
    b85_layers: int = 6,
    marshal_layers: int = 5,
    hash_layers: int = 12,
    compress_layers: int = 8
) -> str:
    data = compute_md5_bytes(keyInput)
    hash_sequence = [
        hashlib.sha256, hashlib.sha512, hashlib.sha3_256, hashlib.sha3_512,
        hashlib.blake2b, hashlib.blake2s, hashlib.sha256, hashlib.sha512,
        hashlib.sha3_256, hashlib.sha3_512, hashlib.blake2b, hashlib.blake2s
    ]
    for h in hash_sequence[:hash_layers]:
        data = h(data).digest()
    xor_key = hashlib.sha256(keyInput.encode('utf-8')).digest()
    data = apply_xor_obfuscate(data, xor_key)
    compress_sequence = [
        zlib.compress, bz2.compress, lzma.compress,
        zlib.compress, bz2.compress, lzma.compress,
        zlib.compress, bz2.compress
    ]
    for comp in compress_sequence[:compress_layers]:
        data = comp(data)
    data = base64.b64encode(data)
    for _ in range(a85_layers):
        data = base64.a85encode(data)
    for _ in range(b85_layers):
        data = base64.b85encode(data)
    for _ in range(marshal_layers):
        data = marshal.dumps(data)
        data = base64.b85encode(data)
    data = hashlib.sha3_512(data).digest()
    data = hashlib.blake2b(data).digest()
    hex_data = binascii.hexlify(data).decode('utf-8')
    final_binary = ''.join(format(byte, '08b') for byte in binascii.unhexlify(hex_data))
    
    return final_binary

def encodeKey(
    keyInput,
    a85_layers=6,
    b85_layers=6,
    marshal_layers=5,
    hash_layers=12,
    compress_layers=8
):
    return encode_key_v5(
        keyInput,
        a85_layers=a85_layers,
        b85_layers=b85_layers,
        marshal_layers=marshal_layers,
        hash_layers=hash_layers,
        compress_layers=compress_layers
    )

def main():
    print("enc key uki\n")
    
    while True:
        keyInput = input("Nhập key cần encode (hoặc 'quit' để thoát): ").strip()
        
        if keyInput.lower() == 'quit':
            print("Tạm biệt!")
            break
            
        if not keyInput:
            print("Vui lòng nhập key!")
            continue
            
        try:
            final_key = encodeKey(keyInput)
            
            print(f"Key gốc           : {keyInput}")
            print(f"Độ dài key encode : {len(final_key)} ký tự ")
            print("=" * 80)
            print("Key đã enc:")
            print(final_key)
            print("=" * 80)
        except Exception as e:
            print(f"Lỗi khi encode: {e}")

if __name__ == "__main__":
    main()