class FSM:
    def __init__(self):
        # Mendefinisikan konfigurasi FSM sesuai gambar diagram
        self.start_state = 'S'
        self.accept_states = {'B'}
        self.current_state = self.start_state
       
        # Tabel transisi (Dictionary)
        # Format: 'State_Sekarang': {'Input': 'State_Berikutnya'}
        self.transitions = {
            'S': {'0': 'A', '1': 'B'},
            'A': {'0': 'C', '1': 'B'},
            'B': {'0': 'A', '1': 'B'},
            'C': {'0': 'C', '1': 'C'}
        }


    def reset(self):
        """Mengembalikan mesin ke state awal sebelum memproses string baru."""
        self.current_state = self.start_state


    def process_string(self, input_string):
        """Memproses string dan mengembalikan status diterima/ditolak beserta state akhir."""
        self.reset()
       
        # Cek string kosong
        if not input_string:
            return False, self.current_state
           
        # Cek validitas alfabet (hanya boleh 0 dan 1)
        if not all(char in '01' for char in input_string):
            raise ValueError("Input tidak valid. Gunakan hanya karakter '0' dan '1'.")


        # Jalankan transisi berdasarkan setiap karakter
        for char in input_string:
            self.current_state = self.transitions[self.current_state][char]


        # Cek apakah state akhir merupakan final state
        is_accepted = self.current_state in self.accept_states
       
        return is_accepted, self.current_state


def main():
    mesin_fsm = FSM()
   
    print("="*50)
    print("   PROGRAM FINITE STATE MACHINE (FSM)")
    print("="*50)
    print("Bahasa L = { x ∈ (0+1)* | diakhiri '1' & tidak ada substring '00' }")
    print("Ketik 'keluar' untuk menghentikan program.")
    print("-" * 50)


    # Loop interaktif untuk memudahkan pengujian pengguna
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

