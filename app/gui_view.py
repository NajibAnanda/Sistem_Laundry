import tkinter as tk
from tkinter import ttk, messagebox
from . import laundry_controller
from . import service_controller

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Manajemen Laundry")
        self.root.geometry("900x550") 

        print("[INFO] GUI View Dimuat...")
        
        self.selected_service_id = None
        
        self.laporan_total_pesanan_var = tk.StringVar(value="Total Pesanan: 0")
        self.laporan_total_pendapatan_var = tk.StringVar(value="Total Pendapatan: Rp 0")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tab1_kasir = ttk.Frame(self.notebook, padding=10)
        self.tab2_admin = ttk.Frame(self.notebook, padding=10)
        
        self.notebook.add(self.tab1_kasir, text="Pesanan")
        self.notebook.add(self.tab2_admin, text="Layanan & Laporan")
        
        self._buat_tab_kasir(self.tab1_kasir)
        self._buat_tab_admin(self.tab2_admin) 

        self._muat_ulang_data_treeview_pesanan() 
        self._muat_layanan_combobox()
        self._muat_ulang_data_treeview_layanan()

    # ===================================================================
    # --- BAGIAN 1: PEMBUATAN TAB KASIR (PESANAN) ---
    # ===================================================================

    def _buat_tab_kasir(self, parent_tab):
        left_frame = ttk.Frame(parent_tab, width=280)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_frame.pack_propagate(False)

        right_frame = ttk.Frame(parent_tab)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self._buat_form_pesanan(left_frame)
        self._buat_aksi_pesanan(left_frame)
        self._buat_list_pesanan(right_frame)

    def _buat_form_pesanan(self, parent):
        form_frame = ttk.LabelFrame(parent, text="Formulir Pesanan")
        form_frame.pack(fill=tk.X, pady=(0, 10)) 
        form_frame.columnconfigure(0, weight=1)
        
        ttk.Label(form_frame, text="Nama Pelanggan:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.entry_nama = ttk.Entry(form_frame) 
        self.entry_nama.grid(row=1, column=0, sticky="we", padx=10, pady=(0,5))

        ttk.Label(form_frame, text="No. HP:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.entry_no_hp = ttk.Entry(form_frame) 
        self.entry_no_hp.grid(row=3, column=0, sticky="we", padx=10, pady=(0,5))
        
        ttk.Label(form_frame, text="Berat (Kg):").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.entry_berat = ttk.Entry(form_frame)
        self.entry_berat.grid(row=5, column=0, sticky="we", padx=10, pady=(0,5))
        
        ttk.Label(form_frame, text="Jenis Layanan:").grid(row=6, column=0, sticky="w", padx=10, pady=5)
        self.layanan_var = tk.StringVar()
        self.combo_layanan = ttk.Combobox(form_frame, textvariable=self.layanan_var, state="readonly") 
        self.combo_layanan.grid(row=7, column=0, sticky="we", padx=10, pady=(0,5))
        
        btn_tambah = ttk.Button(form_frame, text="Tambah Pesanan", command=self._tombol_tambah_pesanan)
        btn_tambah.grid(row=8, column=0, sticky="we", padx=10, pady=10)

    def _buat_aksi_pesanan(self, parent):
        action_frame = ttk.LabelFrame(parent, text="Aksi Pesanan")
        action_frame.pack(fill=tk.X, pady=10)
        
        btn_tandai_selesai = ttk.Button(action_frame, text="Tandai Selesai", command=self._tombol_selesai_pesanan) 
        btn_tandai_selesai.pack(fill=tk.X, padx=10, pady=5)
        
        btn_hapus = ttk.Button(action_frame, text="Hapus Pesanan", command=self._tombol_hapus_pesanan)
        btn_hapus.pack(fill=tk.X, padx=10, pady=5)

    def _buat_list_pesanan(self, parent):
        list_frame = ttk.LabelFrame(parent, text="Daftar Pesanan")
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("id", "nama", "no_hp", "layanan", "berat", "total_harga", "status")
        self.tree_pesanan = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        self.tree_pesanan.heading("id", text="ID")
        self.tree_pesanan.heading("nama", text="Nama Pelanggan")
        self.tree_pesanan.heading("no_hp", text="No. HP") 
        self.tree_pesanan.heading("layanan", text="Layanan")
        self.tree_pesanan.heading("berat", text="Berat (Kg)")
        self.tree_pesanan.heading("total_harga", text="Total Harga")
        self.tree_pesanan.heading("status", text="Status")
        
        self.tree_pesanan.column("id", width=50, anchor=tk.CENTER)
        self.tree_pesanan.column("nama", width=140, anchor=tk.CENTER) 
        self.tree_pesanan.column("no_hp", width=100, anchor=tk.CENTER) 
        self.tree_pesanan.column("layanan", width=80, anchor=tk.CENTER)
        self.tree_pesanan.column("berat", width=60, anchor=tk.CENTER) 
        self.tree_pesanan.column("total_harga", width=100, anchor=tk.CENTER) 
        self.tree_pesanan.column("status", width=80, anchor=tk.CENTER)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree_pesanan.yview)
        self.tree_pesanan.configure(yscroll=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_pesanan.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # ===================================================================
    # --- BAGIAN 2: PEMBUATAN TAB ADMIN (LAYANAN & LAPORAN) ---
    # ===================================================================

    def _buat_tab_admin(self, parent_tab):
        left_frame = ttk.Frame(parent_tab, width=280)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_frame.pack_propagate(False)

        right_frame = ttk.Frame(parent_tab)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self._buat_crud_layanan_form(left_frame)
        self._buat_area_laporan(left_frame)
        self._buat_crud_layanan_list(right_frame)

    def _buat_crud_layanan_form(self, parent):
        form_frame = ttk.LabelFrame(parent, text="Formulir Layanan", padding=10)
        form_frame.pack(fill=tk.X, pady=(0, 10)) 
        form_frame.columnconfigure(0, weight=1)
        
        # --- PERUBAHAN DI SINI: Mengembalikan sticky="w" dan "we" ---
        
        ttk.Label(form_frame, text="Nama Layanan:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_layanan_nama = ttk.Entry(form_frame)
        self.entry_layanan_nama.grid(row=1, column=0, sticky="we", padx=5, pady=5)
        
        ttk.Label(form_frame, text="Harga per Kg:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.entry_layanan_harga = ttk.Entry(form_frame)
        self.entry_layanan_harga.grid(row=3, column=0, sticky="we", padx=5, pady=5)
        
        btn_tambah = ttk.Button(form_frame, text="Tambah", command=self._tombol_layanan_tambah)
        btn_tambah.grid(row=4, column=0, sticky="we", padx=5, pady=10)
        
        btn_update = ttk.Button(form_frame, text="Update", command=self._tombol_layanan_update)
        btn_update.grid(row=5, column=0, sticky="we", padx=5, pady=5)
        
        btn_hapus = ttk.Button(form_frame, text="Hapus", command=self._tombol_layanan_hapus)
        btn_hapus.grid(row=6, column=0, sticky="we", padx=5, pady=5)
        
        btn_clear = ttk.Button(form_frame, text="Clear Form", command=self._clear_form_layanan)
        btn_clear.grid(row=7, column=0, sticky="we", padx=5, pady=10)
        
        # --- AKHIR PERUBAHAN ---

    def _buat_crud_layanan_list(self, parent):
        list_frame = ttk.LabelFrame(parent, text="Daftar Layanan", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("id", "nama", "harga")
        self.tree_layanan = ttk.Treeview(list_frame, columns=columns, show="headings")
        self.tree_layanan.heading("id", text="ID")
        self.tree_layanan.heading("nama", text="Nama Layanan")
        self.tree_layanan.heading("harga", text="Harga per Kg")
        
        # --- TETAP RATA TENGAH (sesuai permintaan) ---
        self.tree_layanan.column("id", width=50, anchor=tk.CENTER)
        self.tree_layanan.column("nama", width=200, anchor=tk.CENTER)
        self.tree_layanan.column("harga", width=100, anchor=tk.CENTER)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree_layanan.yview)
        self.tree_layanan.configure(yscroll=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_layanan.pack(fill=tk.BOTH, expand=True)
        
        self.tree_layanan.bind("<<TreeviewSelect>>", self._saat_layanan_dipilih)

    def _buat_area_laporan(self, parent):
        laporan_frame = ttk.LabelFrame(parent, text="Laporan Harian")
        laporan_frame.pack(fill=tk.X, pady=10) 
        
        btn_laporan = ttk.Button(laporan_frame, text="Tampilkan Laporan Hari Ini", command=self._tombol_tampilkan_laporan)
        btn_laporan.pack(fill=tk.X, padx=10, pady=10)
        
        label_style = "TLabel"
        
        lbl_total_pesanan = ttk.Label(laporan_frame, textvariable=self.laporan_total_pesanan_var, font=("Arial", 12, "bold"), style=label_style)
        lbl_total_pesanan.pack(padx=10, pady=(0,5), anchor="w") 
        
        lbl_total_pendapatan = ttk.Label(laporan_frame, textvariable=self.laporan_total_pendapatan_var, font=("Arial", 12, "bold"), style=label_style)
        lbl_total_pendapatan.pack(padx=10, pady=(0,10), anchor="w") 

    # ===================================================================
    # --- BAGIAN 3: FUNGSI HANDLER UNTUK SEMUA TAB ---
    # ===================================================================

    # --- Handler untuk Tab 1 (Kasir) ---

    def _muat_layanan_combobox(self):
        print("[INFO] Memuat data layanan ke Combobox...")
        try:
            data_layanan = service_controller.get_semua_layanan()
            nama_layanan_list = [layanan["nama_layanan"] for layanan in data_layanan]
            self.combo_layanan['values'] = nama_layanan_list
            if nama_layanan_list:
                self.combo_layanan.current(0)
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memuat data layanan: {e}")
            
    def _get_selected_pesanan_id(self):
        try:
            selected_item = self.tree_pesanan.selection()[0] 
            item_values = self.tree_pesanan.item(selected_item, "values")
            return item_values[0]
        except IndexError:
            messagebox.showwarning("Tidak Ada Pilihan", "Silakan pilih satu pesanan dari tabel terlebih dahulu.")
            return None

    def _tombol_tambah_pesanan(self):
        nama = self.entry_nama.get()
        no_hp = self.entry_no_hp.get()
        berat = self.entry_berat.get()
        layanan = self.combo_layanan.get()
        try:
            sukses, pesan = laundry_controller.tambah_pesanan_baru(nama, berat, layanan, no_hp)
            if sukses:
                messagebox.showinfo("Sukses", pesan)
                self._muat_ulang_data_treeview_pesanan()
                self.entry_nama.delete(0, tk.END)
                self.entry_no_hp.delete(0, tk.END)
                self.entry_berat.delete(0, tk.END)
                self.combo_layanan.current(0)
            else:
                messagebox.showwarning("Gagal", pesan)
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

    def _tombol_selesai_pesanan(self):
        id_pesanan = self._get_selected_pesanan_id()
        if id_pesanan:
            sukses, pesan = laundry_controller.tandai_pesanan_selesai(id_pesanan)
            if sukses:
                messagebox.showinfo("Sukses", pesan)
                self._muat_ulang_data_treeview_pesanan()
            else:
                messagebox.showerror("Gagal", pesan)

    def _tombol_hapus_pesanan(self):
        id_pesanan = self._get_selected_pesanan_id()
        if id_pesanan:
            if messagebox.askyesno("Konfirmasi Hapus", f"Apakah Anda yakin ingin menghapus pesanan {id_pesanan}?"):
                sukses, pesan = laundry_controller.hapus_pesanan(id_pesanan)
                if sukses:
                    messagebox.showinfo("Sukses", pesan)
                    self._muat_ulang_data_treeview_pesanan()
                else:
                    messagebox.showerror("Gagal", pesan)

    def _muat_ulang_data_treeview_pesanan(self):
        for item in self.tree_pesanan.get_children():
            self.tree_pesanan.delete(item)
        daftar_pesanan = laundry_controller.get_semua_pesanan()
        for pesanan in daftar_pesanan:
            self.tree_pesanan.insert("", tk.END, values=(
                pesanan["id"],
                pesanan["nama"],
                pesanan.get("no_hp", "-"), 
                pesanan["layanan"],
                f"{pesanan['berat']:.1f}", 
                f"Rp {pesanan['total_harga']:,.0f}", 
                pesanan["status"]
            ))

    # --- Handler untuk Tab 2 (Admin) ---

    def _muat_ulang_data_treeview_layanan(self):
        for item in self.tree_layanan.get_children():
            self.tree_layanan.delete(item)
            
        daftar_layanan = service_controller.get_semua_layanan()
        for layanan in daftar_layanan:
            self.tree_layanan.insert("", tk.END, values=(
                layanan["id_layanan"],
                layanan["nama_layanan"],
                f"Rp {layanan['harga_per_kg']:,.0f}"
            ))
        self._clear_form_layanan()

    def _saat_layanan_dipilih(self, event):
        try:
            selected_item = self.tree_layanan.selection()[0]
            item_data = self.tree_layanan.item(selected_item, "values")
            
            self.selected_service_id = item_data[0]
            
            self.entry_layanan_nama.delete(0, tk.END)
            self.entry_layanan_nama.insert(0, item_data[1])
            
            harga_str = item_data[2].replace("Rp ", "").replace(",", "")
            self.entry_layanan_harga.delete(0, tk.END)
            self.entry_layanan_harga.insert(0, harga_str)
            
        except IndexError:
            self._clear_form_layanan()

    def _clear_form_layanan(self):
        self.selected_service_id = None
        self.entry_layanan_nama.delete(0, tk.END)
        self.entry_layanan_harga.delete(0, tk.END)
        if self.tree_layanan.selection():
            self.tree_layanan.selection_remove(self.tree_layanan.selection()[0])
            
    def _tombol_layanan_tambah(self):
        nama = self.entry_layanan_nama.get()
        harga_str = self.entry_layanan_harga.get()
        
        sukses, pesan = service_controller.tambah_layanan_baru(nama, harga_str)
        if sukses:
            messagebox.showinfo("Sukses", pesan)
            self._muat_ulang_data_treeview_layanan() 
            self._muat_layanan_combobox()           
        else:
            messagebox.showwarning("Gagal", pesan) 

    def _tombol_layanan_update(self):
        if not self.selected_service_id:
            messagebox.showwarning("Gagal", "Pilih layanan dari tabel untuk di-update.")
            return
            
        nama = self.entry_layanan_nama.get()
        harga_str = self.entry_layanan_harga.get()
        
        sukses, pesan = service_controller.update_layanan(self.selected_service_id, nama, harga_str)
        if sukses:
            messagebox.showinfo("Sukses", pesan)
            self._muat_ulang_data_treeview_layanan() 
            self._muat_layanan_combobox()           
        else:
            messagebox.showwarning("Gagal", pesan) 

    def _tombol_layanan_hapus(self):
        if not self.selected_service_id:
            messagebox.showwarning("Gagal", "Pilih layanan dari tabel untuk dihapus.")
            return
        
        if messagebox.askyesno("Konfirmasi", f"Yakin ingin menghapus layanan {self.selected_service_id}?"):
            sukses, pesan = service_controller.hapus_layanan(self.selected_service_id)
            if sukses:
                messagebox.showinfo("Sukses", pesan)
                self._muat_ulang_data_treeview_layanan() 
                self._muat_layanan_combobox()           
            else:
                messagebox.showwarning("Gagal", pesan)
                
    def _tombol_tampilkan_laporan(self):
        try:
            total_pesanan, total_pendapatan = laundry_controller.get_laporan_harian()
            
            self.laporan_total_pesanan_var.set(f"Total Pesanan: {total_pesanan}")
            self.laporan_total_pendapatan_var.set(f"Total Pendapatan: Rp {total_pendapatan:,.0f}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Gagal membuat laporan: {e}")