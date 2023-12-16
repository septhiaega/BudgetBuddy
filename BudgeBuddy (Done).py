import tkinter as tk
from tkinter import ttk
import csv
from datetime import datetime

class TransaksiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Transaksi")

        # Style
        self.style = ttk.Style()
        self.theme_light()
        
        self.tabControl = ttk.Notebook(self.root)

        # Tab Transaksi Baru
        self.tab_transaksi_baru = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab_transaksi_baru, text="Transaksi Baru")
        self.tabControl.pack(expand=1, fill="both")


        self.label_tanggal = tk.Label(self.tab_transaksi_baru, text="Tanggal:", font=('Helvetica', 12), background="#e0dede")
        self.label_tanggal.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.entry_tanggal = ttk.Combobox(self.tab_transaksi_baru, values=list(range(1, 32)), font=('Helvetica', 12), width=5)
        self.entry_tanggal.grid(row=0, column=1, padx=10, pady=10)

        self.label_bulan = tk.Label(self.tab_transaksi_baru, text="Bulan:", font=('Helvetica', 12), background="#e0dede")
        self.label_bulan.grid(row=0, column=2, padx=10, pady=10, sticky="e")
        self.entry_bulan = ttk.Combobox(self.tab_transaksi_baru, values=["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"], font=('Helvetica', 12))
        self.entry_bulan.grid(row=0, column=3, padx=10, pady=10)

        self.label_tahun = tk.Label(self.tab_transaksi_baru, text="Tahun:", font=('Helvetica', 12), background="#e0dede")
        self.label_tahun.grid(row=0, column=4, padx=10, pady=10, sticky="e")
        self.entry_tahun = ttk.Combobox(self.tab_transaksi_baru, values=list(range(1995, 2100)), font=('Helvetica', 12), width=5)
        self.entry_tahun.grid(row=0, column=5, padx=10, pady=10)

        self.label_jenis_transaksi = tk.Label(self.tab_transaksi_baru, text="Jenis Transaksi:", font=('Helvetica', 12), background="#e0dede")
        self.label_jenis_transaksi.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.entry_jenis_transaksi = ttk.Combobox(self.tab_transaksi_baru, values=["Pemasukkan", "Pengeluaran"], font=('Helvetica', 12))
        self.entry_jenis_transaksi.grid(row=1, column=1, padx=10, pady=10)

        self.label_nilai = tk.Label(self.tab_transaksi_baru, text="Nilai (Rp):", font=('Helvetica', 12), background="#e0dede")
        self.label_nilai.grid(row=1, column=2, padx=10, pady=10, sticky="e")
        self.entry_nilai = tk.Entry(self.tab_transaksi_baru, font=('Helvetica', 12))
        self.entry_nilai.grid(row=1, column=3, padx=10, pady=10)

        self.label_keterangan = tk.Label(self.tab_transaksi_baru, text="Keterangan:", font=('Helvetica', 12), background="#e0dede")
        self.label_keterangan.grid(row=1, column=4, padx=10, pady=10, sticky="e")
        self.entry_keterangan = tk.Entry(self.tab_transaksi_baru, font=('Helvetica', 12))
        self.entry_keterangan.grid(row=1, column=5, padx=10, pady=10)

        self.button_simpan = tk.Button(self.tab_transaksi_baru, text="Simpan", command=self.simpan_transaksi, font=('Helvetica', 12), background="#d0a6a6", foreground="white")
        self.button_simpan.grid(row=2, column=2, padx=10, pady=10)

        # Tab Histori Transaksi
        self.tab_histori = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab_histori, text="Histori Transaksi")
        self.tabControl.pack(expand=1, fill="both", padx=10, pady=10)

        self.listbox_histori = tk.Listbox(self.tab_histori, selectmode=tk.MULTIPLE, font=('Helvetica', 12), background="#f4f1e6")
        self.listbox_histori.pack(expand=1, fill="both", padx=10, pady=10)

        self.button_hapus_semuanya = tk.Button(self.tab_histori, text="Hapus Semua Histori", command=self.hapus_semua_histori, font=('Helvetica', 12), background='#b52b2b', foreground='white')
        self.button_hapus_semuanya.pack(pady=5)

        self.button_hapus_transaksi = tk.Button(self.tab_histori, text="Hapus Transaksi", command=self.hapus_transaksi_terpilih, font=('Helvetica', 12), background='#b52b2b', foreground='white')
        self.button_hapus_transaksi.pack(pady=5)

        self.label_urutkan = tk.Label(self.tab_histori, text="Urutkan Berdasarkan:", font=('Helvetica', 12), background="#e0dede")
        self.label_urutkan.pack(pady=5)

        self.entry_urutkan = ttk.Combobox(self.tab_histori, values=["Waktu Terlama", "Waktu Terbaru", "Jumlah Terbesar", "Jumlah Terkecil"], font=('Helvetica', 12), state="readonly")
        self.entry_urutkan.pack(pady=5)

        self.button_urutkan = tk.Button(self.tab_histori, text="Urutkan", command=self.urutkan_histori, font=('Helvetica', 12), background="#b52b2b", foreground="white")
        self.button_urutkan.pack(pady=5)

        # Label Saldo Akhir
        self.label_saldo_pemasukkan = tk.Label(self.tab_histori, text="Saldo Akhir Pemasukkan: Rp 0", font=('Helvetica', 12), background="#e0dede")
        self.label_saldo_pemasukkan.pack(pady=5)

        self.label_saldo_pengeluaran = tk.Label(self.tab_histori, text="Saldo Akhir Pengeluaran: Rp 0", font=('Helvetica', 12), background="#e0dede")
        self.label_saldo_pengeluaran.pack(pady=5)

        self.label_saldo_akhir = tk.Label(self.tab_histori, text="Saldo Akhir: Rp 0", font=('Helvetica', 12), background="#e0dede")
        self.label_saldo_akhir.pack(pady=5)

         # Tab Cari Transaksi
        self.tab_cari_transaksi = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab_cari_transaksi, text="Cari Transaksi")
        self.tabControl.pack(expand=1, fill="both", padx=10, pady=10)

        self.label_cari = tk.Label(self.tab_cari_transaksi, text="Cari Transaksi:", font=('Helvetica', 12), background="#e0dede")
        self.label_cari.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.entry_cari = tk.Entry(self.tab_cari_transaksi, font=('Helvetica', 12))
        self.entry_cari.grid(row=0, column=1, padx=10, pady=10)

        self.button_cari = tk.Button(self.tab_cari_transaksi, text="Cari", command=self.cari_transaksi, font=('Helvetica', 12), background="#b52b2b", foreground="white")
        self.button_cari.grid(row=0, column=2, padx=10, pady=10)

        self.listbox_hasil_cari = tk.Listbox(self.tab_cari_transaksi, font=('Helvetica', 12), background="#f4f1e6")
        self.listbox_hasil_cari.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        self.button_kembali_cari = tk.Button(self.tab_cari_transaksi, text="Kembali", command=self.kembali_cari, font=('Helvetica', 12), background="#d0a6a6", foreground="white")
        self.button_kembali_cari.grid(row=2, column=1, pady=5)

        # Tema Bright/Dark
        self.button_toggle_theme = tk.Button(self.root, text="Toggle Theme", command=self.toggle_theme, font=('Helvetica', 12), background="#b52b2b", foreground="white")
        self.button_toggle_theme.pack(pady=10)

        # Data
        self.histori_transaksi = []
        self.saldo_pemasukkan = 0
        self.saldo_pengeluaran = 0

        # Load histori dari CSV
        self.load_histori_dari_csv()

    

    def simpan_transaksi(self):
        tanggal = self.entry_tanggal.get()
        bulan = self.entry_bulan.get()
        tahun = self.entry_tahun.get()
        jenis_transaksi = self.entry_jenis_transaksi.get()
        nilai = self.entry_nilai.get()
        keterangan = self.entry_keterangan.get()

        if tanggal and bulan and tahun and jenis_transaksi and nilai and keterangan:
            transaksi = {
                "Tanggal": f"{tanggal} {bulan} {tahun}",
                "Jenis Transaksi": jenis_transaksi,
                "Nilai": f"Rp {nilai}",
                "Keterangan": keterangan
            }
            self.histori_transaksi.append(transaksi)
            self.listbox_histori.insert(tk.END, f"{transaksi['Tanggal']} - {transaksi['Jenis Transaksi']} - {transaksi['Nilai']} - {transaksi['Keterangan']}")
            self.clear_input_transaksi()

            # Update saldo
            self.update_saldo()

            # Simpan histori ke CSV
            self.simpan_ke_csv()

    def clear_input_transaksi(self):
        self.entry_tanggal.set('')
        self.entry_bulan.set('')
        self.entry_tahun.set('')
        self.entry_jenis_transaksi.set('')
        self.entry_nilai.delete(0, tk.END)
        self.entry_keterangan.delete(0, tk.END)

    def hapus_semua_histori(self):
        self.listbox_histori.delete(0, tk.END)
        self.histori_transaksi.clear()
        self.saldo_pemasukkan = 0
        self.saldo_pengeluaran = 0

        # Update label saldo
        self.update_label_saldo()

        # Simpan histori ke CSV
        self.simpan_ke_csv()

    def hapus_transaksi_terpilih(self):
        selected_indices = self.listbox_histori.curselection()
        for i in reversed(selected_indices):
            transaksi = self.histori_transaksi[i]
            nilai = float(transaksi['Nilai'].replace("Rp ", ''))

            if transaksi['Jenis Transaksi'] == 'Pemasukkan':
                self.saldo_pemasukkan -= nilai
            else:
                self.saldo_pengeluaran -= nilai

            # Hapus transaksi
            self.listbox_histori.delete(i)
            del self.histori_transaksi[i]

        # Update saldo
        self.update_saldo()

        # Simpan histori ke CSV
        self.simpan_ke_csv()

    def urutkan_histori(self):
        key = self.entry_urutkan.get()
        if key:
            if key == "Waktu Terlama":
                self.histori_transaksi.sort(key=lambda x: datetime.strptime(x['Tanggal'], '%d %B %Y'))
            elif key == "Waktu Terbaru":
                self.histori_transaksi.sort(key=lambda x: datetime.strptime(x['Tanggal'], '%d %B %Y'), reverse=True)
            elif key == "Jumlah Terbesar":
                self.histori_transaksi.sort(key=lambda x: float(x['Nilai'].replace("Rp ", '')), reverse=True)
            elif key == "Jumlah Terkecil":
                self.histori_transaksi.sort(key=lambda x: float(x['Nilai'].replace("Rp ", '')))

            self.update_listbox_histori()

    def update_listbox_histori(self):
        self.listbox_histori.delete(0, tk.END)
        for transaksi in self.histori_transaksi:
            self.listbox_histori.insert(tk.END, f"{transaksi['Tanggal']} - {transaksi['Jenis Transaksi']} - {transaksi['Nilai']} - {transaksi['Keterangan']}")

    def update_saldo(self):
        self.saldo_pemasukkan = sum([float(transaksi['Nilai'].replace("Rp ", '')) for transaksi in self.histori_transaksi if transaksi['Jenis Transaksi'] == 'Pemasukkan'])
        self.saldo_pengeluaran = sum([float(transaksi['Nilai'].replace("Rp ", '')) for transaksi in self.histori_transaksi if transaksi['Jenis Transaksi'] == 'Pengeluaran'])

        # Update label saldo
        self.update_label_saldo()

    def update_label_saldo(self):
        self.label_saldo_pemasukkan.config(text=f"Saldo Akhir Pemasukkan: Rp {self.saldo_pemasukkan}")
        self.label_saldo_pengeluaran.config(text=f"Saldo Akhir Pengeluaran: Rp {self.saldo_pengeluaran}")
        saldo_akhir = self.saldo_pemasukkan - self.saldo_pengeluaran
        self.label_saldo_akhir.config(text=f"Saldo Akhir: Rp {saldo_akhir}")

    def cari_transaksi(self):
        kata_kunci = self.entry_cari.get().lower()
        hasil_cari = [transaksi for transaksi in self.histori_transaksi if kata_kunci in transaksi['Tanggal'].lower() or kata_kunci in transaksi['Jenis Transaksi'].lower() or kata_kunci in transaksi['Nilai'].lower() or kata_kunci in transaksi['Keterangan'].lower()]

        self.listbox_hasil_cari.delete(0, tk.END)
        for transaksi in hasil_cari:
            self.listbox_hasil_cari.insert(tk.END, f"{transaksi['Tanggal']} - {transaksi['Jenis Transaksi']} - {transaksi['Nilai']} - {transaksi['Keterangan']}")

    def kembali_cari(self):
        self.tabControl.select(1)

    def simpan_ke_csv(self):
        with open('histori_transaksi.csv', 'w', newline='') as csvfile:
            fieldnames = ['Tanggal', 'Jenis Transaksi', 'Nilai', 'Keterangan']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for transaksi in self.histori_transaksi:
                writer.writerow(transaksi)

    def theme_dark(self):
        # Warna untuk tema "gelap"
        self.style.configure("TNotebook", background="#2e2e2e", foreground="white")
        self.style.configure("TFrame", background="#2e2e2e", foreground="white")
        self.style.configure("TButton", background="#333333", foreground="white", padding=(10, 5), font=('Helvetica', 10))
        self.style.configure("TLabel", background="#2e2e2e", foreground="white", font=('Helvetica', 12))
        self.style.configure("TCombobox", background="#444444", foreground="white", font=('Helvetica', 12))
        self.style.configure("TEntry", background="#444444", foreground="white", font=('Helvetica', 12))
    
    def theme_light(self):
        # Warna untuk tema "terang"
        self.style.configure("TNotebook", background="#e0dede", foreground="black")
        self.style.configure("TFrame", background="#e0dede", foreground="black")
        self.style.configure("TButton", background="#d0a6a6", foreground="white", padding=(10, 5), font=('Helvetica', 10))
        self.style.configure("TLabel", background="#e0dede", foreground="black", font=('Helvetica', 12))
        self.style.configure("TCombobox", background="#f4f1e6", foreground="black", font=('Helvetica', 12))
        self.style.configure("TEntry", background="#f4f1e6", foreground="black", font=('Helvetica', 12))

    def toggle_theme(self):
        # Simpan tema saat ini
        current_theme = self.style.theme_use()

        # Toggle antara tema "gelap" dan "terang"
        if current_theme == "clam":
            self.theme_dark()
        else:
            self.theme_light()

        # Ganti tema
        self.style.theme_use("clam" if current_theme != "clam" else "default")  # Memaksa perubahan tema


    def load_histori_dari_csv(self):
        try:
            with open('histori_transaksi.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    self.histori_transaksi.append({
                        "Tanggal": row['Tanggal'],
                        "Jenis Transaksi": row['Jenis Transaksi'],
                        "Nilai": f"Rp {row['Nilai']}",
                        "Keterangan": row['Keterangan']
                    })
                    self.listbox_histori.insert(tk.END, f"{row['Tanggal']} - {row['Jenis Transaksi']} - {row['Nilai']} - {row['Keterangan']}")
        except FileNotFoundError:
            pass

        # Update saldo
        self.update_saldo()

if __name__ == "__main__":
    root = tk.Tk()
    app = TransaksiApp(root)
    root.mainloop()
 
