import bpy
import os
import requests
import zipfile
import base64
import shutil
import atexit
import sys
from io import BytesIO

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


class RAHA_OT_InfoPopup(bpy.types.Operator):
    """Menampilkan informasi Raha Tools"""
    bl_idname = "raha.info_popup"
    bl_label = "Info"

    def execute(self, context):
        def draw_popup(self, context):
            layout = self.layout
            
            col = layout.column()
            col.label(text="Tools ini dibuat untuk mempermudah animasi di Blender 3D,")
            col.label(text="meningkatkan efisiensi kerja, dan mendukung kreativitas para animator.")
            col.separator()
            col.label(text="Tools ini gratis untuk latihan, proyek personal, dan komersial.")
            col.label(text="Namun, dilarang menyebarluaskan di luar link resmi serta dilarang")
            col.label(text="memodifikasi tanpa izin dari Raha Realistis Studio sebagai pemilik resmi.")
            col.separator()
            col.label(text="Saat ini, tools ini masih dalam tahap pengembangan dan akan terus diperbarui")
            col.label(text="dengan fitur-fitur baru. Saya juga memiliki banyak daftar tools lain")
            col.label(text="yang akan dibagikan secara gratis.")
            col.separator()
            col.label(text="Namun, agar proyek ini dapat terus berkembang, saya sangat mengharapkan")
            col.label(text="donasi dari semua pengguna sebagai modal pengembangan.")
            col.label(text="Dukungan Anda akan mempercepat pembaruan tools, pembuatan fitur baru,")
            col.label(text="dan program Free Learning di website saya.")
            col.separator()
            col.label(text="Mari bersama membangun ekosistem kreatif ini.")
            col.label(text="Terima kasih atas apresiasi dan kontribusinya!")
            
            col.separator()
            col.operator("raha.pb_tool", text="How to Use")            
            col.operator("raha.pb_tool", text="Report A Bug")          
        
        bpy.context.window_manager.popup_menu(draw_popup, title="Info", icon='INFO')
        return {'FINISHED'}


ADDONS_DIR = os.path.join(bpy.utils.user_resource('SCRIPTS'), 'addons')
PY_FOLDER_V3 = os.path.join(ADDONS_DIR, 's_pyc_', 'data', 'main', 'sytem', 'cache', 'pyc02', 'blok', 'ug', 'go', 'register', 'v3')
PY_FOLDER_V4 = os.path.join(ADDONS_DIR, 's_pyc_', 'register', 'main', 'sytem', 'cache', 'pyc02', 'blok', 'ug', 'go', 'register', 'v4')


VERSION_FOLDERS = {
    "3": PY_FOLDER_V3,
    "4": PY_FOLDER_V4
}


for path in VERSION_FOLDERS.values():
    if path not in sys.path:
        sys.path.append(path)

# URL dalam Base64
VERSIONS_ENCODED = {
    "3": "aHR0cHM6Ly9naXRodWIuY29tL3Jyc3R1ZGlvZGV2ZWxvcG1lbnQvZG93bmxvYWRfYWxsX3NjcmlwdF9SUi1ULUIuMy9hcmNoaXZlL3JlZnMvaGVhZHMvbWFpbi56aXA=",
    "4": "aHR0cHM6Ly9naXRodWIuY29tL3Jyc3R1ZGlvZGV2ZWxvcG1lbnQvZG93bmxvYWRfYWxsX3NjcmlwdF9SUi1ULUIuNC9hcmNoaXZlL3JlZnMvaGVhZHMvbWFpbi56aXA="
}

executed_scripts = set()

def decode_url(encoded_url):
    return base64.b64decode(encoded_url).decode("utf-8")

def delete_version_folder(version):
    target_folder = VERSION_FOLDERS.get(version, "")
    if os.path.exists(target_folder) and os.path.isdir(target_folder):
        shutil.rmtree(target_folder)
        print(f"[INFO] Folder {target_folder} berhasil dihapus.")

import threading
import time

def delayed_cleanup():
    print("[INFO] Menunggu 20 detik sebelum menghapus folder sementara...")
    time.sleep(20)
    delete_rr_t_folders()
    delete_s_pyc_folder()
    print("[INFO] Pembersihan selesai.")

def download_and_extract(version):
    url = decode_url(VERSIONS_ENCODED.get(version, ""))  
    target_folder = VERSION_FOLDERS.get(version, "")
    
    if not url or not target_folder:
        print("[ERROR] Versi tidak valid!")
        return False
    
    os.makedirs(target_folder, exist_ok=True)
    
    try:
        print(f"[INFO] Mengunduh dari: {url}")
        response = requests.get(url)
        if response.status_code == 200:
            with zipfile.ZipFile(BytesIO(response.content), 'r') as zip_ref:
                zip_ref.extractall(target_folder)
            print(f"[INFO] Raha Tools {version} berhasil diunduh dan diekstrak ke {target_folder}")
            execute_all_scripts(version)
            
            # Jalankan penghapusan folder setelah 20 detik
            threading.Thread(target=delayed_cleanup, daemon=True).start()

            return True
        else:
            print(f"[ERROR] Gagal mengunduh Raha tools, status code: {response.status_code}")
    except Exception as e:
        print(f"[ERROR] Saat mengunduh repository: {e}")
    return False

def execute_all_scripts(version):
    target_folder = VERSION_FOLDERS.get(version, "")
    
    if os.path.exists(target_folder):
        for root, _, files in os.walk(target_folder):
            for file in files:
                if file.endswith(".py"):
                    script_path = os.path.join(root, file)
                    execute_script(script_path)

def execute_script(script_path):
    global executed_scripts
    if script_path in executed_scripts:
        return
    if os.path.exists(script_path):
        try:
            bpy.ops.script.python_file_run(filepath=script_path)
            executed_scripts.add(script_path)
        except Exception as e:
            print(f"[ERROR] Gagal menjalankan {script_path}: {e}")

def delete_py_folder():
    for path in VERSION_FOLDERS.values():
        if os.path.exists(path) and os.path.isdir(path):
            shutil.rmtree(path)
            print(f"[INFO] Folder {path} berhasil dihapus saat Blender ditutup.")

atexit.register(delete_py_folder)

class DOWNLOAD_OT_RunScript(bpy.types.Operator):
    bl_idname = "wm.download_run_all_scripts"
    bl_label = "Select version"
    
    version: bpy.props.EnumProperty(
        name="Version",
        items=[("3", "Blender 3+", "Download Raha Tools for Blender 3+"),
               ("4", "Blender 4+", "Download Raha Tools for Blender 4+")],
        default="3"
    )

    def execute(self, context):
        download_and_extract(self.version)
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

class DOWNLOAD_OT_RepairScripts(bpy.types.Operator):
    bl_idname = "wm.repair_scripts"
    bl_label = "Repair Scripts"

    def execute(self, context):
        for version, folder in VERSION_FOLDERS.items():
            if os.path.exists(folder):
                print(f"[INFO] Memperbaiki script untuk versi {version}...")
                delete_version_folder(version)
                download_and_extract(version)
        return {'FINISHED'}

class DOWNLOAD_PT_Panel(bpy.types.Panel):
    bl_label = "Call Script Raha_Tools"
    bl_idname = "DOWNLOAD_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Raha_Tools"

    def draw(self, context):
        layout = self.layout        
        row = layout.row()
        row.alignment = 'RIGHT'
        row.operator("raha.info_popup", text="WARNING", icon='ERROR')
                
        layout = self.layout
        layout.label(text="Make sure there is an internet connection")
        layout.operator("wm.download_run_all_scripts")


def register():
    bpy.utils.register_class(DOWNLOAD_OT_RunScript)
    bpy.utils.register_class(DOWNLOAD_OT_RepairScripts)
    bpy.utils.register_class(DOWNLOAD_PT_Panel)
    bpy.utils.register_class(RAHA_OT_InfoPopup)    
    

def unregister():
    bpy.utils.unregister_class(DOWNLOAD_OT_RunScript)
    bpy.utils.unregister_class(DOWNLOAD_OT_RepairScripts)
    bpy.utils.unregister_class(DOWNLOAD_PT_Panel)
    bpy.utils.unregister_class(RAHA_OT_InfoPopup)     

if __name__ == "__main__":
    register()
