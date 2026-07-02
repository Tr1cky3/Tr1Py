from lexer import Token
from parser import Parser
from semantic import SemanticAnalyzer
from tac_generator import TACGenerator

if __name__ == "__main__":
    source_code = """
    skor = 15
    jika :skor < 20; p
        keluaran:skor;
    q selain p
        keluaran:0;
    q
    """
    
    print("=== MEMULAI PROSES KOMPILASI MINI COMPILER ===\n")
    
    print("[Step 1] Menjalankan Analisis Leksikal...")
    tokens = Token.tokenize(source_code)
    print(" -> Sukses. Token berhasil dipecah.\n")
    
    # 2. Tahap Sintaksis
    print("[Step 2] Menjalankan Analisis Sintaksis (Parsing AST)...")
    parser = Parser(tokens)
    ast = parser.parse()
    print(" -> Sukses. Abstract Syntax Tree (AST) terbentuk.\n")
    
    # 3. Tahap Semantik
    print("[Step 3] Menjalankan Analisis Semantik...")
    try:
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        print(" -> Sukses. Validasi variabel aman.\n")
    except NameError as e:
        print(f" -> Gagal! {e}")
        exit(1)
        
    # 4. Tahap Generasi Kode Antara (TAC)
    print("[Step 4] Menghasilkan Kode Tiga Alamat (Three-Address Code)...")
    tac_gen = TACGenerator()
    tac_instructions = tac_gen.generate(ast)
    
    print("\n================ HASIL KODE TAC ================")
    for baris in tac_instructions:
        print(f"  {baris}")
    print("================================================")