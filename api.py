import os
import json
import random
import string
import subprocess
import datetime
import base64
import marshal
import hashlib
from pathlib import Path

try:
    from pystyle import Colors, Colorate, Write, Box
except ImportError:
    exit(1)

class APIKeyManager:
    def __init__(self, api_dir="apikey/api/key"):
        self.api_dir = api_dir
        self.api_folders = [
            "avatar", "joiner", "nhaydis", "nhayzalo", 
            "rename", "spamdis", "spamzalo", "voice",
            "ig", "spamdiskonen", "nhaymess", "treomess", "docquyen", "regtoken", "thuereg", "spamv6", "spamv5", "uuid"
        ]
        self.github_repo = "https://github.com/quangthangcoder11/apikey.git"
    
    def print_header(self):
        header_text = """
╔══════════════════════════════════════════════════════════════╗
║                         API KEY MANAGER                      ║
║                    Developed by Hoang Gia Kiet               ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(Colorate.Horizontal(Colors.rainbow, header_text, 1))
    
    def print_success(self, message):
        print(Colorate.Horizontal(Colors.green_to_white, f"{message}", 1))
    
    def print_error(self, message):
        print(Colorate.Horizontal(Colors.red_to_white, f"{message}", 1))
    
    def print_warning(self, message):
        print(Colorate.Horizontal(Colors.yellow_to_green, f"{message}", 1))
    
    def print_info(self, message):
        print(Colorate.Horizontal(Colors.blue_to_white, f"{message}", 1))
    
    def print_loading(self, message):
        print(Colorate.Horizontal(Colors.cyan_to_blue, f"{message}", 1))
    
    def print_rainbow(self, message):
        print(Colorate.Horizontal(Colors.rainbow, message, 1))
    
    def print_purple(self, message):
        print(Colorate.Horizontal(Colors.purple_to_blue, message, 1))
    
    def generate_key(self, length=10):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))
    
    def get_api_folders(self):          
        return [folder for folder in self.api_folders if os.path.exists(os.path.join(self.api_dir, folder))]
    
    def read_keys(self, folder_name):
        key_file = os.path.join(self.api_dir, folder_name, "key.txt")
        if os.path.exists(key_file):
            with open(key_file, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f.readlines() if line.strip()]
        return []
    
    def write_keys(self, folder_name, keys):
        key_file = os.path.join(self.api_dir, folder_name, "key.txt")
        os.makedirs(os.path.dirname(key_file), exist_ok=True)
        with open(key_file, 'w', encoding='utf-8') as f:
            for key in keys:
                f.write(key + '\n')
    
    def add_key(self, folder_name, key=None):
        if key is None:
            key = self.generate_key()
        
        keys = self.read_keys(folder_name)
        if key not in keys:
            keys.append(key)
            self.write_keys(folder_name, keys)
            self.print_success(f"Đã thêm key '{key}' vào {folder_name}")
            return key
        else:
            self.print_error(f"Key '{key}' đã tồn tại trong {folder_name}")
            return None
    
    def remove_key(self, folder_name, key):
        keys = self.read_keys(folder_name)
        if key in keys:
            keys.remove(key)
            self.write_keys(folder_name, keys)
            self.print_success(f"Đã xóa key '{key}' khỏi {folder_name}")
            return True
        else:
            self.print_error(f"Key '{key}' không tồn tại trong {folder_name}")
            return False
    
    def list_keys(self, folder_name):       
        keys = self.read_keys(folder_name)
        print(Colorate.Horizontal(Colors.purple_to_blue, f"\n Keys trong {folder_name}:", 1))
        if keys:
            for i, key in enumerate(keys, 1):
                print(Colorate.Horizontal(Colors.cyan_to_blue, f"  {i:2d}. {key}", 1))
        else:
            print(Colorate.Horizontal(Colors.yellow_to_white, "  Không có keys nào", 1))
        return keys
    
    def update_version(self, folder_name, version=None):        
        version_file = os.path.join(self.api_dir, folder_name, "version.json")
        if os.path.exists(version_file):
            with open(version_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = {
                "version": "1.0",
                "release_date": "",
                "author": "Hoang Gia Kiet",
                "changelog": "update"
            }
        
        if version:
            data["version"] = version
        data["release_date"] = datetime.datetime.now().strftime("%Y-%m-%d")
        
        with open(version_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        self.print_success(f"Đã cập nhật version cho {folder_name}")
    
    def setup_git_repository(self):
        try:
            result = subprocess.run(['git', 'status'], capture_output=True, text=True)
            if result.returncode != 0:
                self.print_loading("Khởi tạo Git repository...")
                subprocess.run(['git', 'init'], check=True)
                subprocess.run(['git', 'remote', 'add', 'origin', self.github_repo], check=True)
                self.print_success("Đã khởi tạo Git repository")
                return True
            else:
                self.print_success("Git repository đã tồn tại")
                return True
        except subprocess.CalledProcessError as e:
            self.print_error(f"Lỗi khi khởi tạo Git repository: {e}")
            return False
        except FileNotFoundError:
            self.print_error("Git không được cài đặt")
            return False
    
    def sync_with_remote(self):
        try:
            self.print_loading("Đang đồng bộ với remote repository...")
            
            subprocess.run(['git', 'fetch', 'origin'], check=True)
            self.print_success("Đã fetch latest changes")
            try:
                subprocess.run(['git', 'pull', 'origin', 'master'], check=True)
                self.print_success("Đã pull changes từ remote")
            except subprocess.CalledProcessError as pull_error:
                if "unrelated histories" in str(pull_error):
                    self.print_warning("Phát hiện unrelated histories, đang xử lý...")
                    subprocess.run(['git', 'pull', 'origin', 'master', '--allow-unrelated-histories'], check=True)
                    self.print_success("Đã merge với unrelated histories")
                else:
                    raise pull_error
            
            return True
        except subprocess.CalledProcessError as e:
            self.print_error(f"Lỗi khi đồng bộ: {e}")
            return False
    
    def git_operations(self):
        try:
            result = subprocess.run(['git', 'status'], capture_output=True, text=True)
            if result.returncode != 0:
                self.print_error("Không phải là Git repository")
                if not self.setup_git_repository():
                    return False
            
            self.sync_with_remote()
            
            status_result = subprocess.run(['git', 'status', '--porcelain', self.api_dir], capture_output=True, text=True)
            if not status_result.stdout.strip():
                self.print_warning(f"Không có thay đổi nào trong thư mục {self.api_dir}")
                return True
            
            subprocess.run(['git', 'add', self.api_dir], check=True)
            self.print_success("Đã add thay đổi từ thư mục api/")
            
            commit_message = f"Update API keys - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            subprocess.run(['git', 'commit', '-m', commit_message], check=True)
            self.print_success("Đã commit thay đổi")
            try:
                subprocess.run(['git', 'push', 'origin', 'master'], check=True)
                self.print_success("Đã push lên GitHub")
            except subprocess.CalledProcessError as push_error:
                if "non-fast-forward" in str(push_error) or "rejected" in str(push_error):
                    self.print_warning("Phát hiện lỗi non-fast-forward, đang đồng bộ...")
                    self.sync_with_remote()
                    subprocess.run(['git', 'push', 'origin', 'master'], check=True)
                    self.print_success("Đã push lên GitHub sau khi đồng bộ")
                else:
                    raise push_error
            
            return True
            
        except subprocess.CalledProcessError as e:
            self.print_error(f"Lỗi Git: {e}")
            return False
        except FileNotFoundError:
            self.print_error("Git không được cài đặt hoặc không có trong PATH")
            return False
    
    def git_operations_all(self):
        try:
            result = subprocess.run(['git', 'status'], capture_output=True, text=True)
            if result.returncode != 0:
                self.print_error("Không phải là Git repository")
                if not self.setup_git_repository():
                    return False
            
            self.sync_with_remote()
            
            subprocess.run(['git', 'add', '.'], check=True)
            self.print_success("Đã add tất cả thay đổi")
            
            commit_message = f"Update all files - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            subprocess.run(['git', 'commit', '-m', commit_message], check=True)
            self.print_success("Đã commit thay đổi")
            try:
                subprocess.run(['git', 'push', 'origin', 'master'], check=True)
                self.print_success("Đã push lên GitHub")
            except subprocess.CalledProcessError as push_error:
                if "non-fast-forward" in str(push_error) or "rejected" in str(push_error):
                    self.print_warning("Phát hiện lỗi non-fast-forward, đang đồng bộ...")
                    self.sync_with_remote()
                    subprocess.run(['git', 'push', 'origin', 'master'], check=True)
                    self.print_success("Đã push lên GitHub sau khi đồng bộ")
                else:
                    raise push_error
            
            return True
            
        except subprocess.CalledProcessError as e:
            self.print_error(f"Lỗi Git: {e}")
            return False
        except FileNotFoundError:
            self.print_error("Git không được cài đặt hoặc không có trong PATH")
            return False
    
    def auto_generate_keys(self, count=1):
        self.print_loading(f"Đang tạo {count} key(s) cho tất cả folders...")
        
        for folder in self.get_api_folders():
            print(Colorate.Horizontal(Colors.purple_to_blue, f"\nXử lý folder: {folder}", 1))
            for i in range(count):
                new_key = self.add_key(folder)
                if new_key:
                    self.update_version(folder)
        
        self.print_success("Hoàn thành tạo keys!")
    
    def backup_keys(self):
        backup_data = {}
        for folder in self.get_api_folders():
            keys = self.read_keys(folder)
            backup_data[folder] = keys
        
        backup_file = f"backup_keys_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, indent=4, ensure_ascii=False)
        
        self.print_success(f"Đã tạo backup: {backup_file}")
        return backup_file
    
    def restore_keys(self, backup_file):
        if not os.path.exists(backup_file):
            self.print_error(f"File backup '{backup_file}' không tồn tại")
            return False
        
        try:
            with open(backup_file, 'r', encoding='utf-8') as f:
                backup_data = json.load(f)
            
            for folder, keys in backup_data.items():
                self.write_keys(folder, keys)
                self.update_version(folder)
                self.print_success(f"Đã khôi phục {len(keys)} keys cho {folder}")
            
            return True
        except Exception as e:
            self.print_error(f"Lỗi khi khôi phục: {e}")
            return False
    
    def read_uuid_data(self):
        uuid_file = os.path.join(self.api_dir, "uuid", "uuid.json")
        if os.path.exists(uuid_file):
            try:
                with open(uuid_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def write_uuid_data(self, data):
        uuid_file = os.path.join(self.api_dir, "uuid", "uuid.json")
        os.makedirs(os.path.dirname(uuid_file), exist_ok=True)
        with open(uuid_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    
    def encode_device_product_id(self, text: str) -> str:
        try:
            
            data = text.encode('utf-8')
            data = base64.b64encode(data)
            data = base64.b64encode(data)
            data = base64.b85encode(data)
            encoded = data.decode()
            return encoded
        except Exception as e:
            self.print_error(f"Lỗi khi mã hóa: {e}")
            return text
    
    def add_uuid_entry(self, key, device_id, product_id):
        entries = self.read_uuid_data()
        encoded_device_id = self.encode_device_product_id(device_id.strip())
        encoded_product_id = self.encode_device_product_id(product_id.strip())
        
        new_entry = {
            "key": key.strip(),
            "device_id": encoded_device_id,
            "product_id": encoded_product_id
        }
        
        entries.append(new_entry)
        self.write_uuid_data(entries)
        self.update_version("uuid")
        self.print_success(f"Đã thêm UUID entry: Key={key}, Device ID={device_id}, Product ID={product_id}")
        return True
    
    def list_uuid_entries(self):
        entries = self.read_uuid_data()
        print(Colorate.Horizontal(Colors.purple_to_blue, f"\nUUID Entries ({len(entries)}):", 1))
        if entries:
            for i, entry in enumerate(entries, 1):
                print(Colorate.Horizontal(Colors.cyan_to_blue, f"\n  {i:2d}. Entry #{i}", 1))
                print(Colorate.Horizontal(Colors.cyan_to_blue, f"      Key: {entry.get('key', 'N/A')}", 1))
                device_id = entry.get('device_id', 'N/A')
                product_id = entry.get('product_id', 'N/A')
                if device_id != 'N/A' and len(device_id) > 50:
                    print(Colorate.Horizontal(Colors.cyan_to_blue, f"      Device ID: {device_id[:50]}... (đã mã hóa)", 1))
                else:
                    print(Colorate.Horizontal(Colors.cyan_to_blue, f"      Device ID: {device_id} (đã mã hóa)", 1))
                if product_id != 'N/A' and len(product_id) > 50:
                    print(Colorate.Horizontal(Colors.cyan_to_blue, f"      Product ID: {product_id[:50]}... (đã mã hóa)", 1))
                else:
                    print(Colorate.Horizontal(Colors.cyan_to_blue, f"      Product ID: {product_id} (đã mã hóa)", 1))
        else:
            print(Colorate.Horizontal(Colors.yellow_to_white, "  Không có entries nào", 1))
        return entries
    
    def remove_uuid_entry(self, index):
        entries = self.read_uuid_data()
        if 0 <= index < len(entries):
            removed = entries.pop(index)
            self.write_uuid_data(entries)
            self.update_version("uuid")
            self.print_success(f"Đã xóa UUID entry: Key={removed.get('key', 'N/A')}")
            return True
        else:
            self.print_error("Index không hợp lệ")
            return False
    
    def uuid_menu(self):
        while True:
            menu_text = """
╔══════════════════════════════════════════════════════════════╗
║                     UUID MANAGER MENU                   ║
╠══════════════════════════════════════════════════════════════╣
║ 1️   Thêm UUID entry mới                                     ║
║ 2️   Xem danh sách UUID entries                              ║
║ 3️   Xóa UUID entry                                          ║
║ 4️   Quay lại menu chính                                     ║
╚══════════════════════════════════════════════════════════════╝
            """
            print(Colorate.Horizontal(Colors.rainbow, menu_text, 1))
            
            choice = Write.Input("Chọn chức năng (1-4): ", Colors.cyan_to_blue)
            
            if choice == "1":
                print(Colorate.Horizontal(Colors.purple_to_blue, "\n📝 Nhập thông tin UUID:", 1))
                key = Write.Input("Key: ", Colors.cyan_to_blue)
                device_id = Write.Input("Device ID: ", Colors.cyan_to_blue)
                product_id = Write.Input("Product ID: ", Colors.cyan_to_blue)
                
                if key and device_id and product_id:
                    self.add_uuid_entry(key, device_id, product_id)
                else:
                    self.print_error("Vui lòng nhập đầy đủ thông tin")
            elif choice == "2":
                self.list_uuid_entries()
            elif choice == "3":
                entries = self.read_uuid_data()
                if entries:
                    self.list_uuid_entries()
                    try:
                        idx = int(Write.Input("Chọn entry để xóa (số): ", Colors.cyan_to_blue)) - 1
                        self.remove_uuid_entry(idx)
                    except ValueError:
                        self.print_error("Vui lòng nhập số hợp lệ")
                else:
                    self.print_error("Không có entries để xóa")
            elif choice == "4":
                break
            else:
                self.print_error("Lựa chọn không hợp lệ")
    
    def print_menu(self):
        menu_text = """
╔══════════════════════════════════════════════════════════════╗
║                         MAIN MENU                       ║
╠══════════════════════════════════════════════════════════════╣
║ 1️   Tạo key mới                                             ║
║ 2️   Xóa key                                                 ║
║ 3️   Xem danh sách keys                                      ║
║ 4️   Tự động tạo keys cho tất cả folders                     ║
║ 5️   Đẩy lên GitHub (chỉ api/)                               ║
║ 6️   Đồng bộ với remote repository                           ║
║ 7️   Tạo backup keys                                         ║
║ 8️   Khôi phục từ backup                                     ║
║ 9️   Đẩy tất cả lên GitHub                                   ║
║ 10  Quản lý UUID                                             ║
║ 11  Thoát                                                   ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(Colorate.Horizontal(Colors.rainbow, menu_text, 1))
    
    def interactive_menu(self):
        while True:
            self.print_menu()
            
            choice = Write.Input("Chọn chức năng (1-11): ", Colors.cyan_to_blue)
            
            if choice == "1":
                self.add_key_menu()
            elif choice == "2":
                self.remove_key_menu()
            elif choice == "3":
                self.list_keys_menu()
            elif choice == "4":
                count = Write.Input("Số lượng keys cần tạo cho mỗi folder: ", Colors.cyan_to_blue)
                try:
                    count = int(count)
                    self.auto_generate_keys(count)
                except ValueError:
                    self.print_error("Vui lòng nhập số hợp lệ")
            elif choice == "5":
                self.git_operations()
            elif choice == "6":
                self.sync_with_remote()
            elif choice == "7":
                self.backup_keys()
            elif choice == "8":
                backup_file = Write.Input("Nhập tên file backup: ", Colors.cyan_to_blue)
                self.restore_keys(backup_file)
            elif choice == "9":
                self.git_operations_all()
            elif choice == "10":
                self.uuid_menu()
            elif choice == "11":
                print(Colorate.Horizontal(Colors.rainbow, "\nTạm biệt! Hẹn gặp lại!", 1))
                break
            else:
                self.print_error("Lựa chọn không hợp lệ")
    
    def add_key_menu(self):
        print(Colorate.Horizontal(Colors.purple_to_blue, "\n Các folders có sẵn:", 1))
        folders = self.get_api_folders()
        for i, folder in enumerate(folders, 1):
            print(Colorate.Horizontal(Colors.cyan_to_blue, f"  {i}. {folder}", 1))
        
        try:
            folder_idx = int(Write.Input("Chọn folder (số): ", Colors.cyan_to_blue)) - 1
            if 0 <= folder_idx < len(folders):
                folder_name = folders[folder_idx]
                custom_key = Write.Input("Nhập key (để trống để tạo tự động): ", Colors.cyan_to_blue)
                key = custom_key if custom_key else None
                self.add_key(folder_name, key)
                self.update_version(folder_name)
            else:
                self.print_error("Lựa chọn không hợp lệ")
        except ValueError:
            self.print_error("Vui lòng nhập số hợp lệ")
    
    def remove_key_menu(self):
        print(Colorate.Horizontal(Colors.purple_to_blue, "\n Các folders có sẵn:", 1))
        folders = self.get_api_folders()
        for i, folder in enumerate(folders, 1):
            print(Colorate.Horizontal(Colors.cyan_to_blue, f"  {i}. {folder}", 1))
        
        try:
            folder_idx = int(Write.Input("Chọn folder (số): ", Colors.cyan_to_blue)) - 1
            if 0 <= folder_idx < len(folders):
                folder_name = folders[folder_idx]
                keys = self.read_keys(folder_name)
                if keys:
                    print(Colorate.Horizontal(Colors.purple_to_blue, f"\nKeys trong {folder_name}:", 1))
                    for i, key in enumerate(keys, 1):
                        print(Colorate.Horizontal(Colors.cyan_to_blue, f"  {i:2d}. {key}", 1))
                    
                    key_idx = int(Write.Input("Chọn key để xóa (số): ", Colors.cyan_to_blue)) - 1
                    if 0 <= key_idx < len(keys):
                        key_to_remove = keys[key_idx]
                        if self.remove_key(folder_name, key_to_remove):
                            self.update_version(folder_name)
                    else:
                        self.print_error("Lựa chọn không hợp lệ")
                else:
                    self.print_error(f"Không có keys trong {folder_name}")
            else:
                self.print_error("Lựa chọn không hợp lệ")
        except ValueError:
            self.print_error("Vui lòng nhập số hợp lệ")
    
    def list_keys_menu(self):
        print(Colorate.Horizontal(Colors.purple_to_blue, "\n Các folders có sẵn:", 1))
        folders = self.get_api_folders()
        for i, folder in enumerate(folders, 1):
            print(Colorate.Horizontal(Colors.cyan_to_blue, f"  {i}. {folder}", 1))
        print(Colorate.Horizontal(Colors.cyan_to_blue, f"  {len(folders) + 1}. Tất cả", 1))
        
        try:
            choice = int(Write.Input("Chọn folder (số): ", Colors.cyan_to_blue))
            if 1 <= choice <= len(folders):
                folder_name = folders[choice - 1]
                self.list_keys(folder_name)
            elif choice == len(folders) + 1:
                for folder in folders:
                    self.list_keys(folder)
            else:
                self.print_error("Lựa chọn không hợp lệ")
        except ValueError:
            self.print_error("Vui lòng nhập số hợp lệ")

def main():
    manager = APIKeyManager()

    os.system('cls' if os.name == 'nt' else 'clear')
    manager.print_header()
    
    print(Colorate.Horizontal(Colors.blue_to_white, "Khởi động API Key Manager...", 1))
    print(Colorate.Horizontal(Colors.blue_to_white, f" Tìm thấy {len(manager.get_api_folders())} API folders", 1))
    print(Colorate.Horizontal(Colors.blue_to_white, f"Repository: {manager.github_repo}", 1))

    try:
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        if result.returncode == 0:
            manager.print_success("Đã kết nối với Git repository")
        else:
            manager.print_warning("Không phải là Git repository hoặc chưa khởi tạo")
    except:
        manager.print_warning("Git không được cài đặt")
    
    manager.interactive_menu()

if __name__ == "__main__":
    main()
