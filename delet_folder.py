import os
import shutil
import getpass
import time
import threading
import subprocess
import uuid

try:
    import win32file
    import win32con
except ImportError:
    print("pywin32 tidak terinstal, coba install dengan `pip install pywin32`.")

def close_open_handles(folder_path):
    """Menutup semua handle terbuka pada folder yang dikunci oleh sistem."""
    try:
        folder_handle = win32file.CreateFile(
            folder_path,
            win32con.GENERIC_READ | win32con.GENERIC_WRITE,
            win32con.FILE_SHARE_DELETE | win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE,
            None,
            win32con.OPEN_EXISTING,
            win32con.FILE_FLAG_BACKUP_SEMANTICS,
            None
        )
        win32file.CloseHandle(folder_handle)
        print(f"Handle folder {folder_path} berhasil ditutup.")
    except Exception as e:
        print(f"Gagal menutup handle folder {folder_path}: {e}")

def rename_folder_randomly(folder_path):
    """Merename folder dengan nama acak sebelum dihapus."""
    if os.path.exists(folder_path):
        new_name = f"{folder_path}_del_{uuid.uuid4().hex}"  # Buat nama random
        try:
            os.rename(folder_path, new_name)
            print(f"Folder di-rename: {folder_path} → {new_name}")
            return new_name  # Kembalikan nama baru agar bisa dihapus nanti
        except Exception as e:
            print(f"Gagal merename {folder_path}: {e}")
    return folder_path  # Jika gagal rename, tetap gunakan nama asli

def force_delete_folder(folder_path):
    """Menghapus folder secara paksa setelah direname."""
    if os.path.exists(folder_path):
        try:
            folder_path = rename_folder_randomly(folder_path)  # Rename dulu
            close_open_handles(folder_path)  # Coba lepas handle jika masih ada
            subprocess.run(f'rmdir /s /q "{folder_path}"', shell=True, check=True)
            print(f"Folder dihapus: {folder_path}")
        except Exception as e:
            print(f"Gagal menghapus {folder_path}: {e}")

def delete_rr_t_folders():
    """Menghapus semua folder dengan prefix 's_pyc_' di folder temp pengguna."""
    username = getpass.getuser()
    temp_path = os.path.join("C:\\Users", username, "AppData", "Local", "Temp")
    
    if os.path.exists(temp_path):
        for folder_name in os.listdir(temp_path):
            folder_path = os.path.join(temp_path, folder_name)
            if folder_name.startswith("s_pyc_") and os.path.isdir(folder_path):                
                force_delete_folder(folder_path)

def delete_after_delay(folder_path, delay=5):
    """Menghapus folder setelah jeda tanpa membekukan UI."""
    def delayed_delete():
        print(f"Menunggu {delay} detik sebelum menghapus {folder_path}...")
        time.sleep(delay)
        force_delete_folder(folder_path)
    
    threading.Thread(target=delayed_delete, daemon=True).start()

# Eksekusi penghapusan folder
delete_rr_t_folders()
