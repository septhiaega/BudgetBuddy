import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
from tkinter import simpledialog
import json

class BudgeBuddyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BudgeBuddy - Aplikasi Keuangan")
        
        # Variabel dan list untuk menyimpan transaksi
        self.transactions = []
        self.current_transaction = {"tanggal": "", "keterangan": "", "jumlah": 0}

        # Frame Utama
        self.frame_utama = tk.Frame(root)
        self.frame_utama.grid(row=0, column=0, rowspan=3, columnspan=2, padx=10, pady=10)

        # Frame Saldo Pemasukan
        self.frame_saldo_pemasukan = tk.Frame(root, borderwidth=2, relief="groove")
        self.frame_saldo_pemasukan.grid(row=0, column=2, padx=10, pady=10)

        tk.Label(self.frame_saldo_pemasukan, text="Saldo Akhir Pemasukan").grid(row=0, column=0, columnspan=2)
        self.saldo_pemasukan_label = tk.Label(self.frame_saldo_pemasukan, text="0")
        self.saldo_pemasukan_label.grid(row=1, column=0, columnspan=2)

        # Frame Saldo Pengeluaran
        self.frame_saldo_pengeluaran = tk.Frame(root, borderwidth=2, relief="groove")
        self.frame_saldo_pengeluaran.grid(row=1, column=2, padx=10, pady=10)

        tk.Label(self.frame_saldo_pengeluaran, text="Saldo Akhir Pengeluaran").grid(row=0, column=0, columnspan=2)
        self.saldo_pengeluaran_label = tk.Label(self.frame_saldo_pengeluaran, text="0")
        self.saldo_pengeluaran_label.grid(row=1, column=0, columnspan=2)

        # Label dan Entry untuk input transaksi
        tk.Label(self.frame_utama, text="Tanggal:").grid(row=0, column=0)
        self.date_entry = tk.Entry(self.frame_utama)
        self.date_entry.grid(row=0, column=1)

        tk.Label(self.frame_utama, text="Keterangan:").grid(row=1, column=0)
        self.description_entry = tk.Entry(self.frame_utama)
        self.description_entry.grid(row=1, column=1)

        tk.Label(self.frame_utama, text="Jumlah:").grid(row=2, column=0)
        self.amount_entry = tk.Entry(self.frame_utama)
        self.amount_entry.grid(row=2, column=1)

        # Tombol untuk menambahkan transaksi
        add_button = tk.Button(self.frame_utama, text="Tambah Transaksi", command=self.add_transaction)
        add_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Treeview untuk menampilkan transaksi
        self.transaction_tree = ttk.Treeview(self.frame_utama, columns=("Tanggal", "Keterangan", "Jumlah"))
        self.transaction_tree.heading("#0", text="ID")
        self.transaction_tree.heading("Tanggal", text="Tanggal")
        self.transaction_tree.heading("Keterangan", text="Keterangan")
        self.transaction_tree.heading("Jumlah", text="Jumlah")
        self.transaction_tree.grid(row=4, column=0, columnspan=3)

        # Tombol untuk menyimpan transaksi
        save_button = tk.Button(self.frame_utama, text="Simpan Transaksi", command=self.save_transaction)
        save_button.grid(row=5, column=0, pady=10)

        # Tombol untuk mencari transaksi
        search_button = tk.Button(self.frame_utama, text="Cari Transaksi", command=self.search_transaction)
        search_button.grid(row=5, column=1, pady=10)

        # Tombol untuk menghapus transaksi
        delete_button = tk.Button(self.frame_utama, text="Hapus Transaksi", command=self.delete_transaction)
        delete_button.grid(row=6, column=0, pady=10)

        # Combobox untuk mengurutkan transaksi
        sort_label = tk.Label(self.frame_utama, text="Urutkan Transaksi:")
        sort_label.grid(row=6, column=1)
        self.sort_options = ttk.Combobox(self.frame_utama, values=["Terbesar", "Terkecil"])
        self.sort_options.grid(row=6, column=2)
        sort_button = tk.Button(self.frame_utama, text="Urutkan", command=self.sort_transaction)
        sort_button.grid(row=7, column=1, pady=10)

        # Saldo awal
        self.saldo_awal = 0
        self.saldo_label = tk.Label(self.frame_utama, text="Saldo Akhir: {}".format(self.saldo_awal))
        self.saldo_label.grid(row=8, column=0, columnspan=2)

    def add_transaction(self):
        # Mendapatkan nilai dari input transaksi
        date = self.date_entry.get()
        description = self.description_entry.get()
        amount = self.amount_entry.get()

        # Validasi input
        if not date or not description or not amount:
            messagebox.showerror("Error", "Mohon isi semua field.")
            return

        # Menentukan apakah transaksi adalah pemasukan atau pengeluaran
        transaction_type = simpledialog.askstring("Jenis Transaksi", "Jenis Transaksi (Pemasukan/Pengeluaran):")
        if not transaction_type or transaction_type.lower() not in ["pemasukan", "pengeluaran"]:
            messagebox.showerror("Error", "Jenis transaksi tidak valid.")
            return

        # Menambahkan transaksi ke list
        transaction_id = len(self.transactions) + 1
        transaction_amount = float(amount) if transaction_type.lower() == "pemasukan" else -float(amount)
        
        # Update saldo akhir
        self.saldo_awal += transaction_amount

        self.current_transaction = {
            "id": transaction_id,
            "tanggal": date,
            "keterangan": description,
            "jumlah": transaction_amount,
            "jenis": transaction_type.lower(),
        }
        self.transactions.append(self.current_transaction)

        # Menampilkan transaksi di Treeview
        self.transaction_tree.insert("", "end", text=str(transaction_id),
                                     values=(date, description, transaction_amount))

        # Mengupdate label saldo akhir
        self.saldo_label.config(text="Saldo Akhir: {}".format(self.saldo_awal))

        # Mengosongkan field input
        self.date_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)

        # Update saldo pemasukan dan pengeluaran
        self.update_saldo_labels()

    def update_saldo_labels(self):
        saldo_pemasukan = sum(transaction["jumlah"] for transaction in self.transactions if transaction["jenis"] == "pemasukan")
        saldo_pengeluaran = sum(transaction["jumlah"] for transaction in self.transactions if transaction["jenis"] == "pengeluaran")

        self.saldo_pemasukan_label.config(text=str(saldo_pemasukan))
        self.saldo_pengeluaran_label.config(text=str(saldo_pengeluaran))

    def save_transaction(self):
        # Menyimpan transaksi ke file JSON
        with open("transactions.json", "w") as file:
            json.dump(self.transactions, file)

        messagebox.showinfo("Info", "Transaksi berhasil disimpan.")

    def search_transaction(self):
        # Mencari transaksi berdasarkan keterangan
        search_query = simpledialog.askstring("Cari Transaksi", "Masukkan keterangan transaksi:")
        if search_query:
            search_results = [transaction for transaction in self.transactions if search_query.lower() in transaction["keterangan"].lower()]
            
            # Menampilkan hasil pencarian di Treeview
            self.display_transactions(search_results)

    def delete_transaction(self):
        # Menghapus transaksi yang dipilih
        selected_item = self.transaction_tree.selection()
        if selected_item:
            transaction_id = int(self.transaction_tree.item(selected_item, "text"))
            deleted_transaction = next(transaction for transaction in self.transactions if transaction["id"] == transaction_id)
            self.transactions.remove(deleted_transaction)
            self.transaction_tree.delete(selected_item)

            # Update saldo akhir setelah menghapus transaksi
            self.saldo_awal -= deleted_transaction["jumlah"]

            # Mengupdate label saldo akhir
            self.saldo_label.config(text="Saldo Akhir: {}".format(self.saldo_awal))

            # Update saldo pemasukan dan pengeluaran
            self.update_saldo_labels()
        else:
            messagebox.showerror("Error", "Pilih transaksi yang akan dihapus.")

    def sort_transaction(self):
        # Mengurutkan transaksi berdasarkan pilihan pengguna
        sort_option = self.sort_options.get()
        if sort_option == "Terbesar":
            self.transactions.sort(key=lambda x: x["jumlah"], reverse=True)
        elif sort_option == "Terkecil":
            self.transactions.sort(key=lambda x: x["jumlah"])

        # Menampilkan transaksi yang sudah diurutkan di Treeview
        self.display_transactions(self.transactions)

        # Update saldo pemasukan dan pengeluaran
        self.update_saldo_labels()

    def display_transactions(self, transactions):
        # Menghapus semua item di Treeview
        for item in self.transaction_tree.get_children():
            self.transaction_tree.delete(item)

        # Menampilkan transaksi di Treeview
        for transaction in transactions:
            self.transaction_tree.insert("", "end", text=str(transaction["id"]),
                                     values=(transaction["tanggal"], transaction["keterangan"], transaction["jumlah"]))


if __name__ == "__main__":
    root = tk.Tk()
    app = BudgeBuddyApp(root)
    root.mainloop()
