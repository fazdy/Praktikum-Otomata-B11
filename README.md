<div align="center">

# ⚙️ Praktikum Otomata

### Kelompok B11 · Otomata Kelas B

**Departemen Teknik Informatika**
**Institut Teknologi Sepuluh Nopember**
**2026**

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-FF6F00?style=for-the-badge)
![License](https://img.shields.io/badge/License-Academic-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen?style=for-the-badge)

---

</div>

## 👥 Anggota Kelompok

<div align="center">

| No | Nama | NRP |
|:--:|------|:---:|
| 1 | **Kemal Tangguh Aji Rajasa** | `5025231263` |
| 2 | **Achmad Najwa M** | `5025231265` |
| 3 | **Faizal Aldy Armiriawan** | `5025231266` |

</div>

---

## 📂 Struktur Repository

```
📦 Praktikum-Otomata-B11
├── 📄 README.md            ← Dokumentasi lengkap
├── 🐍 praktikum1.py        ← Lexical Recognizer (GUI)
├── 🐍 praktikum2.py        ← Finite State Machine (CLI)
└── 📝 .gitignore
```

---

## 🛠️ Prasyarat & Instalasi

```bash
# Pastikan Python 3.x sudah terinstal
python3 --version

# Clone repository ini
git clone https://github.com/fazdy/Praktikum-Otomata-B11.git
cd Praktikum-Otomata-B11
```

> **Note:** Semua library yang digunakan (`tkinter`, `re`, `keyword`) merupakan library bawaan Python — tidak perlu instalasi tambahan.

---

<div align="center">

# 📘 PRAKTIKUM I

## Lexical Recognizer

*Pengenalan Token & Tokenisasi Source Code*

</div>

---

### 🎯 Tujuan Praktikum

1. Memahami **bahasa sebagai himpunan** dan operasi-operasinya, serta cara mengenali anggota-anggota bahasa.
2. Mengenal **grammar** sebagai himpunan sintaksis bahasa beserta cara kerjanya.
3. Mampu merancang dan membuat program **Recognizer** yang membaca input program dan menghasilkan output berupa **pengelompokan token**.

---

### 📖 Landasan Teori

#### Terminologi Bahasa dan Recognizer

Dalam teori otomata, terminologi bahasa dibangun secara **hierarkis**:

```
📝 Bahasa
 └── 📄 Kalimat
      └── 🔤 Kata / String
           └── 🔡 Karakter = Alphabet + Digit + Symbol
```

Sebuah **Recognizer** (Finite Automata) diperlukan untuk menelusuri karakter per karakter dari string input dan menentukan apakah string tersebut merupakan anggota suatu bahasa tertentu.

#### Grammar

Grammar **G** didefinisikan sebagai 4 tupel **(VN, VT, S, θ)**:

| Komponen | Keterangan |
|:--------:|------------|
| **VN** | Himpunan berhingga **non-terminal** |
| **VT** | Himpunan berhingga **terminal** (angka, karakter, simbol) |
| **S** | **Start symbol** (anggota VN) |
| **θ** | Himpunan **production** |

---

### 🏗️ Perancangan Sistem

Program menggunakan **Python 3** dengan **Regular Expression** sebagai mesin Finite Automata, dan **Tkinter** sebagai antarmuka GUI.

Token dikelompokkan ke dalam **4 kategori**:

| # | Kelompok Token | Metode Pengenalan |
|:-:|----------------|-------------------|
| 1 | **Reserve Words** | Kata kunci bawaan Python (`keyword` module) + tambahan (`int`, `float`, `public`, dll.) |
| 2 | **Simbol & Tanda Baca** | Karakter simbolis: `( ) [ ] { } ; , .` |
| 3 | **Variabel** | Kombinasi alfanumerik yang **bukan** reserve words |
| 4 | **Kalimat Matematika** | Digit + operator matematika/logika |

---

### 🚀 Cara Menjalankan

```bash
python3 praktikum1.py
```

Setelah dijalankan, masukkan source code pada area input, lalu klik tombol **"Jalankan Recognizer"**.

---

### 💻 Source Code

<details>
<summary><b>📄 Klik untuk melihat kode praktikum1.py</b></summary>

<br>

```python
import tkinter as tk
from tkinter import scrolledtext
import re
import keyword

def analyze_code():
    code = text_input.get("1.0", tk.END)
    text_output.delete("1.0", tk.END)

    # Mendefinisikan himpunan Karakter (Alphabet, Digit, Symbol)
    token_specification = [
        ('STRING',   r'(?:"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\')'),
        ('NUMBER',   r'\b\d+(\.\d*)?\b'),
        ('MATH_OP',  r'[+\-*/%=<>!&|]+'),
        ('PUNCT',    r'[\[\]{}():;,\.]'),
        ('ID',       r'[A-Za-z_][A-Za-z0-9_]*'),
        ('NEWLINE',  r'\n'),
        ('SKIP',     r'[ \t]+'),
        ('MISMATCH', r'.'),
    ]

    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)

    reserved_words = set(keyword.kwlist)
    reserved_words.update({'int', 'float', 'double', 'char', 'void',
                           'public', 'private', 'static', 'String'})

    results = {
        "Reserve words": [],
        "Simbol dan tanda baca": [],
        "Variabel": [],
        "Kalimat matematika (Operator & Angka)": []
    }

    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()

        if kind == 'ID':
            if value in reserved_words:
                results["Reserve words"].append(value)
            else:
                results["Variabel"].append(value)
        elif kind == 'PUNCT':
            results["Simbol dan tanda baca"].append(value)
        elif kind in ['NUMBER', 'MATH_OP']:
            results["Kalimat matematika (Operator & Angka)"].append(value)
        elif kind in ['NEWLINE', 'SKIP', 'STRING', 'MISMATCH']:
            continue

    for category, items in results.items():
        unique_items = list(dict.fromkeys(items))
        text_output.insert(tk.END, f"=== {category} ===\n", "header")
        if unique_items:
            text_output.insert(tk.END, ", ".join(unique_items) + "\n\n")
        else:
            text_output.insert(tk.END, "(Tidak ditemukan)\n\n")

# === KONFIGURASI USER INTERFACE ===
root = tk.Tk()
root.title("Lexical Recognizer - Praktikum Otomata")
root.geometry("800x600")
root.configure(bg="#f4f4f4")

lbl_input = tk.Label(root, text="Masukkan Program / Source Code di bawah ini:",
                     bg="#f4f4f4", font=("Arial", 11, "bold"))
lbl_input.pack(pady=(10, 0), padx=10, anchor="w")

text_input = scrolledtext.ScrolledText(root, height=12, width=90, font=("Consolas", 11))
text_input.pack(pady=5, padx=10)
text_input.insert(tk.END, "# Masukkan contoh kode di sini\n"
                  "int a = 10;\nint b = 20;\nint total = a + b;\n"
                  "if (total > 15) {\n    print(total);\n}")

btn_analyze = tk.Button(root, text="Jalankan Recognizer", command=analyze_code,
                        bg="#0078D7", fg="white", font=("Arial", 11, "bold"))
btn_analyze.pack(pady=10)

lbl_output = tk.Label(root, text="Hasil Identifikasi String/Token:",
                      bg="#f4f4f4", font=("Arial", 11, "bold"))
lbl_output.pack(pady=(5, 0), padx=10, anchor="w")

text_output = scrolledtext.ScrolledText(root, height=12, width=90, font=("Consolas", 11))
text_output.tag_configure("header", foreground="#0078D7", font=("Consolas", 11, "bold"))
text_output.pack(pady=5, padx=10)

root.mainloop()
```

</details>

---

### 🧪 Hasil Pengujian

#### Skenario 1 — Struktur Data List dan Perulangan

> Menguji kemampuan program mengenali simbol array/list dan reserve words perulangan (`for`, `in`).

```python
data_angka = [10, 20, 30]
total = 0
for x in data_angka:
    total += x
```

#### Skenario 2 — Class dan Exception Handling

> Menguji pengenalan keyword OOP (`class`, `def`) dan penanganan eksepsi (`try`, `except`).

```python
class Kalkulator:
    def bagi(self, a, b):
        try:
            return a / b
        except ZeroDivisionError:
            return 0.0
```

#### Skenario 3 — Pemanggilan Modul dan Akses Properti

> Menguji pemisahan tanda titik (`.`) sebagai simbol saat mengakses properti modul.

```python
import math
jari_jari = 7
luas = math.pi * (jari_jari * jari_jari)
```

#### Skenario 4 — Operasi Logika dan Komparasi Majemuk

> Memastikan program membedakan kata kunci logika Python dengan variabel biasa.

```python
is_valid = True
batas_bawah = -10
while is_valid and (batas_bawah <= 0):
    batas_bawah += 2
```

---

### 📊 Analisis Hasil

| Aspek Pengujian | Hasil |
|-----------------|-------|
| **Pemisahan Entitas Leksikal** | ✅ Reserve Words (`for`, `in`, `class`, `def`) berhasil dipisahkan dari variabel kustom (`data_angka`, `Kalkulator`) |
| **Pengenalan Simbol & Desimal** | ✅ Karakter simbolis (`[`, `:`) → Simbol; operator (`+=`) dan desimal (`0.0`) → Kalimat Matematika |
| **Penanganan Simbol Khusus** | ✅ Titik (`.`) diidentifikasi sebagai Punctuation saat di antara dua identifier (`math.pi`). Bilangan negatif (`-10`) dan komparasi (`<=`) ditangani tepat |

### 📌 Kesimpulan

Program **Lexical Recognizer** berhasil diimplementasikan menggunakan Regular Expression sebagai mesin Finite Automata. Recognizer berjalan **linier dari kiri ke kanan**, menelusuri karakter per karakter, dan mengelompokkan token dengan akurasi sesuai teori **Hirarki Chomsky**.

---

<div align="center">

# 📗 PRAKTIKUM II

## Finite State Machine (FSM)

*Pengenalan Bahasa Formal dengan Mesin State Berhingga*

</div>

---

### 🎯 Tujuan Praktikum

1. Memahami **bahasa sebagai himpunan** dan operasi-operasinya, serta cara mengenali anggota-anggota bahasa.
2. Mengenal **grammar** sebagai himpunan sintaksis bahasa beserta cara kerjanya.
3. Mampu merancang **Recognizer** berbasis FSM yang memvalidasi string terhadap aturan bahasa formal.

---

### 📖 Landasan Teori

#### Bahasa yang Dikenali

```
L = { x ∈ (0+1)* | karakter terakhir x adalah 1 DAN x tidak memiliki substring "00" }
```

FSM berfungsi sebagai **filter** — dari himpunan tak terhingga string biner `(0+1)*`, mesin hanya **menerima** string yang memenuhi **kedua syarat** di atas.

---

### 🏗️ Perancangan Sistem

#### Diagram Transisi State

```
                ┌─────── 1 ───────┐
                │                 ▼
         0    ┌───┐     1      ╔═══╗
  ┌─── [START]│ S │──────────▶║ B ║◀──┐
  │           └───┘            ╚═══╝   │
  │                              │     │ 1
  ▼          1                   │ 0   │
┌───┐  ──────────────────────┘   │     │
│ A │────────────────────────────┘   ──┘
└───┘
  │
  │ 0
  ▼
┌───┐ 0,1
│ C │◀────┐
└───┘─────┘
 TRAP
```

#### Tabel Transisi

<div align="center">

| State | Input `0` | Input `1` | Keterangan |
|:-----:|:---------:|:---------:|------------|
| **S** | A | **B** | 🟢 Start state |
| **A** | C | **B** | Sudah membaca satu `0` |
| **B** | A | **B** | ✅ **Accept state** (final) |
| **C** | C | C | ❌ **Trap state** (jebakan) |

</div>

---

### 🚀 Cara Menjalankan

```bash
python3 praktikum2.py
```

Program berjalan **interaktif di terminal**. Masukkan string biner untuk diuji, ketik `keluar` untuk berhenti.

---

### 💻 Source Code

<details>
<summary><b>📄 Klik untuk melihat kode praktikum2.py</b></summary>

<br>

```python
class FSM:
    def __init__(self):
        self.start_state = 'S'
        self.accept_states = {'B'}
        self.current_state = self.start_state

        self.transitions = {
            'S': {'0': 'A', '1': 'B'},
            'A': {'0': 'C', '1': 'B'},
            'B': {'0': 'A', '1': 'B'},
            'C': {'0': 'C', '1': 'C'}
        }

    def reset(self):
        """Mengembalikan mesin ke state awal."""
        self.current_state = self.start_state

    def process_string(self, input_string):
        """Memproses string dan mengembalikan status diterima/ditolak."""
        self.reset()

        if not input_string:
            return False, self.current_state

        if not all(char in '01' for char in input_string):
            raise ValueError("Input tidak valid. Gunakan hanya karakter '0' dan '1'.")

        for char in input_string:
            self.current_state = self.transitions[self.current_state][char]

        is_accepted = self.current_state in self.accept_states
        return is_accepted, self.current_state


def main():
    mesin_fsm = FSM()

    print("=" * 50)
    print("   PROGRAM FINITE STATE MACHINE (FSM)")
    print("=" * 50)
    print("Bahasa L = { x ∈ (0+1)* | diakhiri '1' & tidak ada substring '00' }")
    print("Ketik 'keluar' untuk menghentikan program.")
    print("-" * 50)

    while True:
        user_input = input("\nMasukkan string untuk diuji : ")

        if user_input.lower() == 'keluar':
            print("Program dihentikan. Terima kasih!")
            break

        try:
            diterima, state_akhir = mesin_fsm.process_string(user_input)

            if diterima:
                print(f"hasil: String Diterima")
            else:
                print(f"hasil: String Ditolak")

            print(f"   (Berhenti di State: {state_akhir})")

        except ValueError as e:
            print(f"ERROR: {e}")


if __name__ == "__main__":
    main()
```

</details>

---

### 🧪 Hasil Pengujian

#### ✅ String Diterima — Berhenti di State B

<div align="center">

| Input | State Akhir | Alasan Diterima |
|:-----:|:-----------:|-----------------|
| `101` | **B** | Tidak ada `00`, diakhiri `1` |
| `11` | **B** | Tidak ada `00`, diakhiri `1` |
| `01` | **B** | Tidak ada `00`, diakhiri `1` |
| `10101101...010101` | **B** | Stress test — stabil meskipun string sangat panjang |

</div>

#### ❌ String Ditolak — Berhenti di State C *(Trap State)*

<div align="center">

| Input | State Akhir | Alasan Ditolak |
|:-----:|:-----------:|----------------|
| `1001` | **C** | Diakhiri `1`, tetapi substring `00` terdeteksi → trap |
| `100001011100101001` | **C** | Urutan `0` berturut langsung mengarahkan ke trap |

</div>

#### ❌ String Ditolak — Berhenti di State A

<div align="center">

| Input | State Akhir | Alasan Ditolak |
|:-----:|:-----------:|----------------|
| `0` | **A** | Tidak ada `00`, tetapi **tidak diakhiri `1`** → bukan accept state |

</div>

---

### 📊 Analisis Hasil

| State Akhir | Evaluasi |
|:-----------:|----------|
| **State B** *(Accept)* | ✅ Semua string yang berhenti di B memenuhi kedua syarat. Stress test membuktikan **stabilitas iterasi transisi** |
| **State C** *(Trap)* | ❌ Berfungsi sebagai jebakan untuk pelanggaran `00`. Setelah masuk C, **semua input selanjutnya diabaikan** |
| **State A** *(Non-accept)* | ❌ String valid tanpa `00` tetapi tidak diakhiri `1` → ditolak karena A **bukan accept state** |

### 📌 Kesimpulan

Program **Finite State Machine** berhasil mengimplementasikan bahasa `L = { x ∈ (0+1)* | diakhiri '1' & tidak ada substring '00' }`. FSM dirancang dengan **4 state** (S, A, B, C) dimana State C sebagai *trap state*. Program terbukti mampu menyaring string dengan **akurasi tinggi** sesuai spesifikasi bahasa formal.

---

<div align="center">

### 📝 Lisensi

Proyek ini dibuat untuk keperluan akademik
**Praktikum Otomata · Departemen Teknik Informatika · ITS 2026**

---

*Made with ❤️ by Kelompok B11*

</div>
