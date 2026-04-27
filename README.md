<![CDATA[# 📘 Praktikum Otomata — Kelompok B11

> **Departemen Teknik Informatika — Institut Teknologi Sepuluh Nopember 2026**

Repository ini berisi kumpulan tugas Praktikum mata kuliah **Otomata Kelas B** yang dikerjakan oleh Kelompok B11.

## 👥 Anggota Kelompok

| Nama | NRP |
|------|-----|
| Kemal Tangguh Aji Rajasa | 5025231263 |
| Achmad Najwa M | 5025231265 |
| Faizal Aldy Armiriawan | 5025231266 |

---

## 📂 Daftar Praktikum

| Praktikum | Topik | File |
|-----------|-------|------|
| [Praktikum I](#-praktikum-i--lexical-recognizer) | Lexical Recognizer | `praktikum1.py` |
| [Praktikum II](#-praktikum-ii--finite-state-machine-fsm) | Finite State Machine (FSM) | `praktikum2.py` |

---

## 🛠️ Prasyarat

- **Python 3.x**
- Library bawaan: `tkinter`, `re`, `keyword`

```bash
# Cek versi Python
python3 --version
```

---

# 🔬 Praktikum I — Lexical Recognizer

## 1. Tujuan

1. Mahasiswa memahami bahasa sebagai himpunan dan operasi-operasinya, serta cara mengenali anggota-anggota bahasa.
2. Mahasiswa mengenal grammar sebagai himpunan sintaksis bahasa beserta cara kerjanya.
3. Mahasiswa mampu merancang dan membuat program komputer (**Recognizer**) yang dapat membaca input program dan menghasilkan output berupa pengelompokan token berdasarkan sifat string tersebut.

## 2. Landasan Teori

### 2.1 Terminologi Bahasa dan Recognizer

Dalam teori otomata, terminologi bahasa dibangun dari struktur yang berhirarki:

```
Bahasa ──▶ Kalimat ──▶ Kata/String ──▶ Karakter (Alphabet + Digit + Symbol)
```

Untuk mengetahui apakah sebuah input string merupakan anggota suatu bahasa tertentu atau tidak, diperlukan sebuah **Recognizer** atau **Finite Automata**. Recognizer akan melakukan penelusuran karakter per karakter dari string yang diinputkan.

### 2.2 Grammar

Grammar adalah sebuah sistem matematis yang digunakan untuk mendefinisikan bahasa. Secara formal, sebuah grammar **G** memiliki 4 tupel **(V<sub>N</sub>, V<sub>T</sub>, S, θ)**:

| Komponen | Keterangan |
|----------|------------|
| **V<sub>N</sub>** | Himpunan berhingga non-terminal |
| **V<sub>T</sub>** | Himpunan berhingga terminal (angka, karakter, simbol, tanda baca) |
| **S** | Start symbol (salah satu anggota V<sub>N</sub>) |
| **θ** | Himpunan production |

## 3. Perancangan Sistem

Program dirancang menggunakan **Python 3** dengan dukungan **Regular Expression (RegEx)** yang merepresentasikan cara kerja Finite Automata. Antarmuka pengguna menggunakan pustaka **tkinter**.

Mesin Recognizer membagi token menjadi **empat kelompok utama**:

| Kelompok | Metode Pengenalan |
|----------|-------------------|
| **Reserve Words** | Kata kunci bawaan Python (`keyword` module) + kata kunci umum (`int`, `float`, `public`, dll.) |
| **Simbol & Tanda Baca** | Karakter simbolis seperti `(`, `)`, `[`, `]`, `;`, `,` |
| **Variabel** | Kombinasi alfanumerik yang bukan reserve words |
| **Kalimat Matematika** | Digit (angka) dan Symbol operasi matematika/logika |

## 4. Cara Menjalankan

```bash
python3 praktikum1.py
```

Setelah dijalankan, akan muncul jendela GUI. Masukkan source code pada area input, lalu klik tombol **"Jalankan Recognizer"**.

## 5. Implementasi Kode

<details>
<summary>📄 Klik untuk melihat source code <code>praktikum1.py</code></summary>

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

# === KONFIGURASI USER INTERFACE (UI) ===
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

## 6. Hasil Pengujian

### Skenario 1 — Struktur Data List dan Perulangan

Menguji pengenalan simbol array/list dan reserve words perulangan (`for`, `in`).

**Input:**
```python
data_angka = [10, 20, 30]
total = 0
for x in data_angka:
    total += x
```

### Skenario 2 — Pendefinisian Class dan Exception Handling

Menguji pengenalan keyword OOP dan penanganan eksepsi.

**Input:**
```python
class Kalkulator:
    def bagi(self, a, b):
        try:
            return a / b
        except ZeroDivisionError:
            return 0.0
```

### Skenario 3 — Pemanggilan Modul dan Akses Properti

Menguji pemisahan tanda titik (`.`) sebagai simbol tanda baca saat mengakses properti modul.

**Input:**
```python
import math
jari_jari = 7
luas = math.pi * (jari_jari * jari_jari)
```

### Skenario 4 — Operasi Logika dan Komparasi Majemuk

Memastikan program membedakan kata kunci logika Python dengan variabel biasa.

**Input:**
```python
is_valid = True
batas_bawah = -10
while is_valid and (batas_bawah <= 0):
    batas_bawah += 2
```

## 7. Analisis Hasil

| Aspek | Hasil |
|-------|-------|
| **Pemisahan Entitas Leksikal** | Program mampu memisahkan Reserve Words bawaan Python 3 (`for`, `in`, `class`, `def`) dari variabel kustom (`data_angka`, `Kalkulator`) |
| **Pengenalan Simbol & Angka Desimal** | Karakter simbolis (`[`, `:`) masuk ke "Simbol dan Tanda Baca"; operator majemuk (`+=`) dan angka desimal (`0.0`) masuk ke "Kalimat Matematika" |
| **Penanganan Simbol Khusus** | Titik (`.`) diidentifikasi sebagai Punctuation (bukan desimal) saat berada di antara dua string (`math.pi`). Bilangan negatif (`-10`) dan komparasi (`<=`) ditangani dengan tepat |

## 8. Kesimpulan

Praktikum ini berhasil mengimplementasikan sebuah **Lexical Recognizer** sederhana. Tahap awal pengenalan bahasa sangat bergantung pada ketepatan pendefinisian simbol terminal. Mesin Recognizer berjalan linier meniru konsep Finite Automata, menelusuri karakter dari kiri ke kanan, dan mengelompokkannya sesuai teori **Hirarki Chomsky**.

---

# 🔬 Praktikum II — Finite State Machine (FSM)

## 1. Tujuan

1. Mahasiswa memahami bahasa sebagai himpunan dan operasi-operasinya, serta cara mengenali anggota-anggota bahasa.
2. Mahasiswa mengenal grammar sebagai himpunan sintaksis bahasa beserta cara kerjanya.
3. Mahasiswa mampu merancang dan membuat program komputer (**Recognizer**) yang dapat membaca input program dan menghasilkan output berupa pengelompokan token berdasarkan sifat string tersebut.

## 2. Landasan Teori

### 2.1 Terminologi Bahasa dan Recognizer

Sama seperti Praktikum I, terminologi bahasa dibangun dari struktur yang berhirarki. Recognizer atau Finite Automata diperlukan untuk menelusuri karakter per karakter dari string input.

### 2.2 Bahasa L = { x ∈ (0+1)* }

Notasi matematis:

```
L = { x ∈ (0+1)* | karakter terakhir x adalah 1 DAN x tidak memiliki substring "00" }
```

FSM yang dirancang berfungsi sebagai **alat penyaring (filter)**. Dari himpunan tak terhingga string `(0+1)*`, FSM akan **menerima** string yang memenuhi kedua syarat dan **menolak** yang tidak memenuhi.

## 3. Perancangan Sistem

### Diagram Transisi State

```
         0           1
  ┌──── [S] ────────[B] ◀──┐
  │      │           ▲  │   │
  ▼      │     1     │  │ 1 │
 [A] ────┘───────────┘  └───┘
  │
  │ 0
  ▼
 [C] ◀──┐
  │  │   │
  │  └───┘  (trap state, 0 dan 1 tetap di C)
```

| State | Input `0` | Input `1` | Keterangan |
|-------|-----------|-----------|------------|
| **S** (start) | A | B | State awal |
| **A** | C | B | Sudah baca satu `0` |
| **B** (accept) | A | B | ✅ Final state |
| **C** (trap) | C | C | ❌ Jebakan (ada `00`) |

## 4. Cara Menjalankan

```bash
python3 praktikum2.py
```

Program berjalan secara interaktif di terminal. Masukkan string biner untuk diuji, ketik `keluar` untuk menghentikan.

## 5. Implementasi Kode

<details>
<summary>📄 Klik untuk melihat source code <code>praktikum2.py</code></summary>

```python
class FSM:
    def __init__(self):
        self.start_state = 'S'
        self.accept_states = {'B'}
        self.current_state = self.start_state

        # Tabel transisi (Dictionary)
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

## 6. Hasil Pengujian

### ✅ String Diterima (Berhenti di State B)

| Input | State Akhir | Keterangan |
|-------|-------------|------------|
| `101` | B | Kasus dasar valid |
| `11` | B | Kasus dasar valid |
| `01` | B | Kasus dasar valid |
| `10101101010101111010101010101010101` | B | Stress test — stabil meskipun string sangat panjang |

### ❌ String Ditolak (Berhenti di State C — Trap State)

| Input | State Akhir | Keterangan |
|-------|-------------|------------|
| `1001` | C | Meskipun diakhiri `1`, substring `00` terdeteksi → langsung ke trap state |
| `100001011100101001` | C | Urutan panjang `0` berturut-turut langsung mengarahkan ke State C |

### ❌ String Ditolak (Berhenti di State A)

| Input | State Akhir | Keterangan |
|-------|-------------|------------|
| `0` | A | Tidak mengandung `00`, tetapi tidak diakhiri `1` → bukan accept state |

## 7. Analisis Hasil

- **State B (Accept):** Semua input yang berhenti di State B terbukti memenuhi kedua syarat — tidak ada `00` dan diakhiri `1`. Stress test dengan string panjang membuktikan stabilitas iterasi transisi.
- **State C (Trap):** Berfungsi sebagai jebakan untuk pelanggaran substring `00`. Setelah masuk State C, semua input selanjutnya diabaikan dan status dikunci pada **Ditolak**.
- **State A (Non-accept):** String yang valid dari segi aturan pertama (tidak ada `00`) tetapi tidak memenuhi aturan akhiran `1` akan ditolak karena State A bukan accept state.

## 8. Kesimpulan

Praktikum ini berhasil mengimplementasikan sebuah **Finite State Machine (FSM)** untuk bahasa `L = { x ∈ (0+1)* | diakhiri '1' & tidak ada substring '00' }`. FSM dirancang dengan 4 state (S, A, B, C) dimana State C berfungsi sebagai trap state. Program terbukti mampu menyaring string dengan akurasi tinggi sesuai spesifikasi bahasa formal yang diberikan.

---

## 📝 Lisensi

Proyek ini dibuat untuk keperluan akademik Praktikum Otomata — Departemen Teknik Informatika ITS 2026.
]]>
