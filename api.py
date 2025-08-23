import os
import json
import random
import string
import subprocess
import datetime
from pathlib import Path

try:
    from pystyle import Colors, Colorate, Write, Box
except ImportError:
    print("❌ Thư viện pystyle chưa được cài đặt. Vui lòng cài đặt: pip install pystyle")
    exit(1)

class APIKeyManager:
    def __init__(self, api_dir="apikey/api/key"):
        self.api_dir = api_dir
        self.api_folders = [
            "avatar", "joiner", "nhaydis", "nhayzalo", 
            "rename", "spamdis", "spamzalo", "voice",
            "ig", "spamdiskonen"
        ]
        self.github_repo = "https://github.com/quangthangcoder11/apikey.git"
    
    def print_header(self):
        header_text = """
╔══════════════════════════════════════════════════════════════╗
║                    🔑 API KEY MANAGER 🔑                    ║
║                    Developed by Hoang Gia Kiet              ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(Colorate.Horizontal(Colors.rainbow, header_text, 1))
    
    def print_success(self, message):
        print(Colorate.Horizontal(Colors.green_to_white, f"✅ {message}", 1))
    
    def print_error(self, message):
        print(Colorate.Horizontal(Colors.red_to_white, f"❌ {message}", 1))
    
    def print_warning(self, message):
        print(Colorate.Horizontal(Colors.yellow_to_green, f"⚠️  {message}", 1))
    
    def print_info(self, message):
        print(Colorate.Horizontal(Colors.blue_to_white, f"ℹ️  {message}", 1))
    
    def print_loading(self, message):
        print(Colorate.Horizontal(Colors.cyan_to_blue, f"🔄 {message}", 1))
    
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
        print(Colorate.Horizontal(Colors.purple_to_blue, f"\n📁 Keys trong {folder_name}:", 1))
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
            
            subprocess.run(['git', 'pull', 'origin', 'master'], check=True)
            self.print_success("Đã pull changes từ remote")
            
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
            
            subprocess.run(['git', 'push', 'origin', 'master'], check=True)
            self.print_success("Đã push lên GitHub")
            
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

            subprocess.run(['git', 'push', 'origin', 'master'], check=True)
            self.print_success("Đã push lên GitHub")
            
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
            print(Colorate.Horizontal(Colors.purple_to_blue, f"\n📁 Xử lý folder: {folder}", 1))
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
    
    def print_menu(self):
        menu_text = """
╔══════════════════════════════════════════════════════════════╗
║                        📋 MAIN MENU 📋                      ║
╠══════════════════════════════════════════════════════════════╣
║ 1️⃣   Tạo key mới                                             ║
║ 2️⃣   Xóa key                                                 ║
║ 3️⃣   Xem danh sách keys                                      ║
║ 4️⃣   Tự động tạo keys cho tất cả folders                     ║
║ 5️⃣   Đẩy lên GitHub (chỉ api/)                               ║
║ 6️⃣   Đồng bộ với remote repository                           ║
║ 7️⃣   Tạo backup keys                                         ║
║ 8️⃣   Khôi phục từ backup                                     ║
║ 9️⃣   Đẩy tất cả lên GitHub                                   ║
║ 🔟   Thoát                                                   ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(Colorate.Horizontal(Colors.rainbow, menu_text, 1))
    
    def interactive_menu(self):
        while True:
            self.print_menu()
            
            choice = Write.Input("Chọn chức năng (1-10): ", Colors.cyan_to_blue)
            
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
                print(Colorate.Horizontal(Colors.rainbow, "\n👋 Tạm biệt! Hẹn gặp lại!", 1))
                break
            else:
                self.print_error("Lựa chọn không hợp lệ")
    
    def add_key_menu(self):
        print(Colorate.Horizontal(Colors.purple_to_blue, "\n📁 Các folders có sẵn:", 1))
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
        print(Colorate.Horizontal(Colors.purple_to_blue, "\n📁 Các folders có sẵn:", 1))
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
        print(Colorate.Horizontal(Colors.purple_to_blue, "\n📁 Các folders có sẵn:", 1))
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
    
    print(Colorate.Horizontal(Colors.blue_to_white, "🚀 Khởi động API Key Manager...", 1))
    print(Colorate.Horizontal(Colors.blue_to_white, f"📁 Tìm thấy {len(manager.get_api_folders())} API folders", 1))
    print(Colorate.Horizontal(Colors.blue_to_white, f"🔗 Repository: {manager.github_repo}", 1))

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
