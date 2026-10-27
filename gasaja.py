
import tkinter as tk
from tkinter import messagebox
import sqlite3

def create_db():
    conn = sqlite3.connect("nilai_siswa.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT NOT NULL,
            biologi INTEGER NOT NULL,
            fisika INTEGER NOT NULL,
            inggris INTEGER NOT NULL,
            prediksi_fakultas TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


create_db()

def perengan_fakultas(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris:
        return "Kedokteran"
    elif fisika > biologi and fisika > inggris:
        return "Teknik"
    elif inggris > biologi and inggris > fisika:
        return "Bahasa"
    else:
        return "Tidak dapat ditentukan"

def submit_nilai():
    nama = entry_nama.get().strip()

    if not nama:
        messagebox.showerror(
            "Error",
            "Nama siswa tidak boleh kosong!"
        )
        entry_nama.focus()
        return

    try:
        bio = int(entry_biologi.get().strip())
        fis = int(entry_fisika.get().strip())
        ingg = int(entry_inggris.get().strip())

    except ValueError:
        messagebox.showerror(
            "Error",
            "Nilai harus berupa angka bulat!"
        )
        return

    if any(n < 0 or n > 100 for n in [bio, fis, ingg]):
        messagebox.showerror(
            "Error",
            "Nilai harus antara 0 sampai 100!"
        )
        return

    hasil_prediksi = perengan_fakultas(bio, fis, ingg)

    try:
        conn = sqlite3.connect("nilai_siswa.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO nilai_siswa
            (nama_siswa, biologi, fisika, inggris,
             prediksi_fakultas)
            VALUES (?, ?, ?, ?, ?)
        """, (nama, bio, fis, ingg, hasil_prediksi))

        conn.commit()
        conn.close()

    except sqlite3.Error as error:
        messagebox.showerror(
            "Database Error",
            f"Gagal menyimpan data:\n{error}"
        )
        return

    messagebox.showinfo(
        "Sukses",
        f"Data berhasil disimpan!\n\n"
        f"Nama: {nama}\n"
        f"Biologi: {bio}\n"
        f"Fisika: {fis}\n"
        f"Inggris: {ingg}\n\n"
        f"Prediksi fakultas: {hasil_prediksi}"
    )

    entry_nama.delete(0, tk.END)
    entry_biologi.delete(0, tk.END)
    entry_fisika.delete(0, tk.END)
    entry_inggris.delete(0, tk.END)

    entry_nama.focus()

def on_enter(event):
    btn_submit.config(
        bg="#dcdcdc",
        fg="black"
    )

def on_leave(event):
    btn_submit.config(
        bg="#eeeeee",
        fg="black"
    )

root = tk.Tk()
root.title("Prediksi Fakultas Siswa")
root.geometry("550x510")
root.resizable(False, False)
root.configure(bg="white")

judul = tk.Label(
    root,
    text="PREDIKSI FAKULTAS",
    font=("Arial", 22, "bold"),
    bg="white",
    fg="black"
)
judul.pack(pady=(35, 5))

subjudul = tk.Label(
    root,
    text="Masukkan data dan nilai siswa",
    font=("Arial", 12),
    bg="white",
    fg="#444444"
)
subjudul.pack(pady=(0, 35))

form = tk.Frame(root, bg="white")
form.pack(fill="x", padx=30)

form.columnconfigure(1, weight=1)


def buat_input(teks, baris):
    label = tk.Label(
        form,
        text=teks,
        font=("Arial", 11, "bold"),
        bg="white",
        fg="black",
        anchor="w"
    )
    label.grid(
        row=baris,
        column=0,
        sticky="w",
        padx=(0, 12),
        pady=10
    )

    entry = tk.Entry(
        form,
        font=("Arial", 12),
        bg="white",
        fg="black",
        insertbackground="black",
        relief="solid",
        bd=1
    )
    entry.grid(
        row=baris,
        column=1,
        sticky="ew",
        ipady=7,
        pady=10
    )

    return entry


entry_nama = buat_input("Nama Siswa", 0)
entry_biologi = buat_input("Biologi (0-100)", 1)
entry_fisika = buat_input("Fisika (0-100)", 2)
entry_inggris = buat_input("Inggris (0-100)", 3)

btn_submit = tk.Button(
    root,
    text="SIMPAN & PREDIKSI",
    font=("Arial", 12, "bold"),
    bg="#eeeeee",
    fg="black",
    activebackground="#dcdcdc",
    activeforeground="black",
    relief="solid",
    bd=1,
    cursor="hand2",
    command=submit_nilai
)
btn_submit.pack(
    fill="x",
    padx=30,
    pady=(25, 20),
    ipady=10
)

btn_submit.bind("<Enter>", on_enter)
btn_submit.bind("<Leave>", on_leave)

entry_nama.focus()

root.mainloop()
