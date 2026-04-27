import tkinter as tk
from tkinter import scrolledtext
import re
import keyword

def analyze_code():
    code = text_input.get("1.0", tk.END)
    text_output.delete("1.0", tk.END)
    
    # ---------------------------------------------------------
    # IMPLEMENTASI RECOGNIZER / FINITE AUTOMATA (Berdasarkan PPT 1)
    # Recognizer menelusuri input karakter per karakter [cite: 367, 368]
    # Menggunakan Regular Expression sebagai mesin Automata
    # ---------------------------------------------------------
    
    # Mendefinisikan himpunan Karakter (Alphabet, Digit, Symbol) 
    token_specification = [
        # String/Kata: Kombinasi Alphabet, Digit, atau Symbol dalam tanda kutip
        ('STRING',   r'(?:"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\')'), 
        
        # Digit: Himpunan angka untuk kalimat matematika
        ('NUMBER',   r'\b\d+(\.\d*)?\b'),             
        
        # Symbol: Himpunan simbol untuk operator matematika
        ('MATH_OP',  r'[+\-*/%=<>!&|]+'),             
        
        # Symbol: Himpunan simbol untuk tanda baca program
        ('PUNCT',    r'[\[\]{}():;,\.]'),             
        
        # String (Kata): Kombinasi Alphabet (dan garis bawah) untuk Identifier/Variabel
        ('ID',       r'[A-Za-z_][A-Za-z0-9_]*'),      
        
        ('NEWLINE',  r'\n'),                          
        ('SKIP',     r'[ \t]+'),                      
        ('MISMATCH', r'.'),                           
    ]
    
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    
    # Himpunan Reserve Words (String khusus yang sudah dikenali bahasa)
    reserved_words = set(keyword.kwlist)
    reserved_words.update({'int', 'float', 'double', 'char', 'void', 'public', 'private', 'static', 'String'})
    
    # Struktur penyimpanan hasil (mengelompokkan string sesuai sifatnya)
    results = {
        "Reserve words": [],
        "Simbol dan tanda baca": [],
        "Variabel": [],
        "Kalimat matematika (Operator & Angka)": []
    }
    
    # Proses RECOGNIZER menelusuri teks
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
            
    # Menampilkan output
    for category, items in results.items():
        unique_items = list(dict.fromkeys(items)) 
        
        text_output.insert(tk.END, f"=== {category} ===\n", "header")
        if unique_items:
            text_output.insert(tk.END, ", ".join(unique_items) + "\n\n")
        else:
            text_output.insert(tk.END, "(Tidak ditemukan)\n\n")

# ==========================================
# KONFIGURASI USER INTERFACE (UI) 
# ==========================================
root = tk.Tk()
root.title("Lexical Recognizer - Praktikum Otomata")
root.geometry("800x600")
root.configure(bg="#f4f4f4")

lbl_input = tk.Label(root, text="Masukkan Program / Source Code di bawah ini:", bg="#f4f4f4", font=("Arial", 11, "bold"))
lbl_input.pack(pady=(10, 0), padx=10, anchor="w")

text_input = scrolledtext.ScrolledText(root, height=12, width=90, font=("Consolas", 11))
text_input.pack(pady=5, padx=10)
text_input.insert(tk.END, "# Masukkan contoh kode di sini\nint a = 10;\nint b = 20;\nint total = a + b;\nif (total > 15) {\n    print(total);\n}")

# Mengubah nama tombol agar lebih sesuai dengan istilah teori di PPT 1
btn_analyze = tk.Button(root, text="Jalankan Recognizer", command=analyze_code, bg="#0078D7", fg="white", font=("Arial", 11, "bold"))
btn_analyze.pack(pady=10)

lbl_output = tk.Label(root, text="Hasil Identifikasi String/Token:", bg="#f4f4f4", font=("Arial", 11, "bold"))
lbl_output.pack(pady=(5, 0), padx=10, anchor="w")

text_output = scrolledtext.ScrolledText(root, height=12, width=90, font=("Consolas", 11))
text_output.tag_configure("header", foreground="#0078D7", font=("Consolas", 11, "bold"))
text_output.pack(pady=5, padx=10)

root.mainloop()


