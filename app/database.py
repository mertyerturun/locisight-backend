import sqlite3

# Veritabanı dosyamızın adı (bu dosya otomatik olarak oluşturulacak)
DB_NAME = 'locisight_leads.db'

def get_db():
    """Veritabanına bağlanır ve sütun isimleriyle verilere erişmemizi sağlar."""
    conn = sqlite3.connect(DB_NAME)
    # Verileri bir sözlük (dictionary) formatında, sütun isimleriyle almamızı sağlar
    conn.row_factory = sqlite3.Row  
    return conn

def init_db(app=None):
    """Sistem ilk çalıştığında 'leads' tablosunu oluşturur (eğer yoksa)."""
    conn = get_db()
    cursor = conn.cursor()
    
    # Güvenli tablo oluşturma işlemi.
    # Yönergeye uygun olarak id, isim, telefon, mesaj ve tarih sütunları tanımlandı.
    # Locisight vizyonuna uygun olarak (deprem riski, aile yapısı vb.) 'kriter' sütunu eklendi.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            isim TEXT NOT NULL,
            telefon TEXT NOT NULL,
            mesaj TEXT,
            kriter TEXT,
            tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def lead_ekle(isim, telefon, mesaj="", kriter=""):
    """Yapay zeka asistanının topladığı yeni bir müşteri adayını (lead) kaydeder."""
    conn = get_db()
    cursor = conn.cursor()
    
    # GÜVENLİK ZORUNLULUĞU: Veriler SQL'e doğrudan eklenmedi, '?' yer tutucusu kullanıldı.
    cursor.execute('''
        INSERT INTO leads (isim, telefon, mesaj, kriter)
        VALUES (?, ?, ?, ?)
    ''', (isim, telefon, mesaj, kriter))
    
    conn.commit()
    conn.close()

def tum_leadler():
    """Tüm müşteri kayıtlarını en yeniden eskiye doğru (tarihe göre azalan) getirir."""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM leads ORDER BY tarih DESC')
    rows = cursor.fetchall()
    conn.close()
    
    # Veritabanından gelen satırları standart Python sözlük listesine çeviriyoruz
    return [dict(row) for row in rows]