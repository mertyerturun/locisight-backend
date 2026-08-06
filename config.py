import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    SECRET_KEY = os.environ.get('SECRET_KEY', 'varsayilan_anahtar')
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
    
    BUSINESS_CONTEXT = """Sen Locisight'ın yapay zeka destekli akıllı lokasyon değerlendirme asistanısın. 
    Amacın, kullanıcıların yaşam tarzlarına (örn: çocuklu aile) ve çevresel önceliklerine (deprem riski, yeşil alana erişim, suç oranı) göre onlara en uygun ev/bölge eşleşmelerini sunmaktır.
    Empatik, veri odaklı, net ve profesyonel bir dil kullan.
    Kullanıcının önceliklerini ve bütçesini anladıktan sonra, emlak uzmanlarımızın onlara en doğru portföyü sunabilmesi için kibarca isim ve telefon numarası bırakmalarını iste."""