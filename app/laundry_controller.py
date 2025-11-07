from . import storage_service
from . import service_controller 
from datetime import datetime

# --- DIUBAH: Tambah parameter 'no_hp' ---
def tambah_pesanan_baru(nama, berat_str, layanan_nama, no_hp):
    print(f"[CONTROLLER] Menerima data: {nama}, {berat_str}, {layanan_nama}, {no_hp}")
    
    # 1. Validasi Input
    # --- DIUBAH: Tambah validasi 'no_hp' ---
    if not nama or not berat_str or not layanan_nama or not no_hp:
        return False, "Semua kolom wajib diisi."
    try:
        berat = float(berat_str)
        if berat <= 0:
            raise ValueError("Berat harus lebih dari 0")
    except ValueError:
        return False, "Berat harus angka positif."
        
    # 2. Hitung Harga (Dinamis)
    layanan_obj = service_controller.get_layanan_by_nama(layanan_nama)
    if not layanan_obj:
        return False, f"Jenis layanan '{layanan_nama}' tidak valid."
        
    harga_per_kg = layanan_obj["harga_per_kg"]
    total_harga = berat * harga_per_kg
    
    # 3. Buat Objek Pesanan
    pesanan_baru = {
        "nama": nama,
        "no_hp": no_hp, # <-- BARU
        "layanan": layanan_nama,
        "berat": berat,
        "total_harga": total_harga,
        "tanggal_masuk": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    
    # 4. Kirim ke Storage
    storage_service.simpan_pesanan_baru(pesanan_baru)
    return True, "Pesanan berhasil ditambahkan."

def get_semua_pesanan():
    return storage_service.muat_semua_pesanan()

def tandai_pesanan_selesai(id_pesanan):
    sukses = storage_service.update_status_pesanan(id_pesanan, "Selesai")
    if sukses:
        return True, "Status pesanan berhasil diubah."
    else:
        return False, "Gagal mengubah status, ID tidak ditemukan."

def hapus_pesanan(id_pesanan):
    sukses = storage_service.hapus_pesanan_by_id(id_pesanan)
    if sukses:
        return True, "Pesanan berhasil dihapus."
    else:
        return False, "Gagal menghapus, ID tidak ditemukan."

def get_laporan_harian():
    """ Menghitung total pesanan dan pendapatan untuk HARI INI """
    print("[CONTROLLER] Membuat laporan harian...")
    
    hari_ini_str = datetime.now().strftime("%Y-%m-%d")
    semua_pesanan = storage_service.muat_semua_pesanan()
    
    total_pesanan_hari_ini = 0
    total_pendapatan_hari_ini = 0.0
    
    for pesanan in semua_pesanan:
        tanggal_pesanan = pesanan["tanggal_masuk"].split(" ")[0]
        
        if tanggal_pesanan == hari_ini_str:
            total_pesanan_hari_ini += 1
            total_pendapatan_hari_ini += pesanan["total_harga"]
            
    return total_pesanan_hari_ini, total_pendapatan_hari_ini