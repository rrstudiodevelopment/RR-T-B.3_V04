import bpy
import os
import shutil
import getpass
import stat
import time
import threading

def remove_readonly(func, path, exc_info):
    """Menghapus atribut read-only lalu mencoba hapus ulang."""
    os.chmod(path, stat.S_IWRITE)
    func(path)

def delete_folder(folder_path):
    """Menghapus folder jika ada dan bypass folder read-only."""
    if os.path.exists(folder_path):
        try:
            shutil.rmtree(folder_path, onerror=remove_readonly)
            print(f"Folder dihapus: {folder_path}")
        except Exception as e:
            print(f"Gagal menghapus {folder_path}: {e}")

def delete_rr_t_folders():
    username = getpass.getuser()
    temp_path = os.path.join("C:\\Users", username, "AppData", "Local", "Temp")
    
    if os.path.exists(temp_path):
        for folder_name in os.listdir(temp_path):
            folder_path = os.path.join(temp_path, folder_name)
            if folder_name.startswith("RR-T") and os.path.isdir(folder_path):
                delete_folder(folder_path)

def delete_s_pyc_folder():
    """Menghapus folder mulai dari 'main' di direktori addons Blender."""
    username = getpass.getuser()
    blender_version = f"{bpy.app.version[0]}.{bpy.app.version[1]}"
    addons_path = os.path.join(
        "C:\\Users", username, "AppData", "Roaming", "Blender Foundation", "Blender", blender_version,
        "scripts", "addons", "s_pyc_", "data", "main")
    delete_folder(addons_path)

def delete_after_delay(folder_path, delay=5):
    """Menghapus folder setelah jeda tanpa membekukan UI."""
    def delayed_delete():
        print(f"Menunggu {delay} detik sebelum menghapus {folder_path}...")
        time.sleep(delay)
        delete_folder(folder_path)
    
    threading.Thread(target=delayed_delete, daemon=True).start()

# Eksekusi fungsi penghapusan folder
delete_rr_t_folders()
delete_s_pyc_folder()
