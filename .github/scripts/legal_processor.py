import os
import re
import json
import pdfplumber

REG_DIR = "data-regulasi"
INDEX_FILE = os.path.join(REG_DIR, "index_pustaka.json")

def extract_text_from_pdf(pdf_path):
    """Mengekstrak teks penuh dari PDF (Semua Halaman)."""
    full_text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            # Baca semua halaman
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
    return full_text

def detect_identity(text):
    """Mencari Judul Resmi di 2000 karakter pertama (Halaman awal)."""
    # Pola: NOMOR [ANGKA] TAHUN [ANGKA]
    # Mencakup: UU, PP, PERPRES, PERMEN, KEPPRES
    pattern = r"(UNDANG-UNDANG|PERATURAN|KEPUTUSAN|INSTRUKSI)(?:[\s\S]{0,100}?)(NOMOR\s+\d+\s+TAHUN\s+\d+)"
    match = re.search(pattern, text[:5000], re.IGNORECASE | re.MULTILINE)
    
    if match:
        # Contoh: PERATURAN PEMERINTAH NOMOR 35 TAHUN 2021
        clean_title = re.sub(r'\s+', ' ', match.group(0)).strip().upper()
        return clean_title
    return "UNKNOWN_TITLE"

def detect_revocation(text):
    """Mencari pola 'Mencabut' di bagian akhir dokumen (Ketentuan Penutup)."""
    # Ambil 5000 karakter terakhir
    footer_text = text[-5000:] 
    
    revoked_titles = []
    
    # Pola kalimat pencabutan: "... dicabut dan dinyatakan tidak berlaku"
    revocation_pattern = r"(?:Mencabut|menarik kembali)\s+(.*?)(?:\n|\.|;)"
    matches = re.findall(revocation_pattern, footer_text, re.IGNORECASE)
    
    for m in matches:
        # Bersihkan hasil temuan
        clean_ref = re.sub(r'\s+', ' ', m).strip().upper()
        revoked_titles.append(clean_ref)
        
    return revoked_titles

def main():
    # 1. Load Index Lama (jika ada)
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, 'r') as f:
            index_data = json.load(f)
    else:
        index_data = {}

    files_processed = 0

    # 2. Loop semua file di folder regulasi
    for filename in os.listdir(REG_DIR):
        if filename.lower().endswith('.pdf'):
            file_path = os.path.join(REG_DIR, filename)
            txt_filename = filename.replace('.pdf', '.txt')
            txt_path = os.path.join(REG_DIR, txt_filename)
            
            # Cek apakah sudah diproses (ada .txt dan ada di index)
            if os.path.exists(txt_path) and filename in index_data:
                continue # Skip biar cepat (Incremental)

            print(f"Processing: {filename}...")
            
            # A. Ekstrak Teks
            raw_text = extract_text_from_pdf(file_path)
            
            # Simpan versi .txt (Cache)
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(raw_text)
            
            # B. Deteksi Identitas & Pencabutan
            official_title = detect_identity(raw_text)
            killed_list = detect_revocation(raw_text)
            
            # C. Update Index Diri Sendiri
            index_data[filename] = {
                "official_title": official_title,
                "status": "ACTIVE", # Default aktif sampai dibunuh file lain
                "killed_by": None,
                "revokes": killed_list # Daftar siapa yang dia bunuh
            }
            
            # D. Update Status File Lain (KILL SWITCH)
            # Jika file ini mencabut aturan lama, cari aturan lama itu di index & update statusnya
            if killed_list:
                for killed_title in killed_list:
                    # Cari file mana yang punya judul ini
                    for other_file, info in index_data.items():
                        # Pencocokan sederhana (fuzzy logic bisa ditambahkan nanti)
                        if killed_title in info['official_title']:
                            index_data[other_file]['status'] = "REVOKED"
                            index_data[other_file]['killed_by'] = official_title
                            print(f"  -> KILL SWITCH: {official_title} killed {info['official_title']}")

            files_processed += 1

    # 3. Simpan Index Baru
    if files_processed > 0:
        with open(INDEX_FILE, 'w') as f:
            json.dump(index_data, f, indent=2)
        print(f"Selesai. {files_processed} file baru diproses.")
    else:
        print("Tidak ada file baru.")

if __name__ == "__main__":
    main()