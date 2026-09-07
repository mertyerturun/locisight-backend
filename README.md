# Locisight Backend 

Locisight, klasik emlak arama deneyimini Doğal Dil İşleme (NLP) ile dönüştürmeyi hedefleyen yapay zeka destekli bir lokasyon değerlendirme asistanıdır. Bu repo, projenin backend mimarisini barındırıyor. 

Geleneksel emlak platformlarındaki "oda sayısı", "metrekare" gibi kısıtlayıcı filtreleme sistemlerini koduma eklemedim. Bunun yerine, kullanıcının serbest metin (örn: "2 çocuklu aile için deprem riski düşük ev") üzerinden doğrudan **arama** yapmasını sağlayan bir yapı kurguladım.

## Tech Stack
* **Python:** Çekirdek dilimiz.
* **Flask:** API süreçlerini hızlı ve hafif bir şekilde ayağa kaldırmak için tercih ettim.
* **Groq API & Render:** NLP tabanlı yanıt üretimi ve bulut sunucu (deployment) tarafı.

## Mimari Yaklaşım (RAG & NLP)
Kullanıcıdan gelen doğal dildeki karmaşık talepler (Prompt), backend üzerinde işlenerek anlamlandırılıyor. Sistem, veritabanındaki mahalle/lokasyon verilerini tarıyor ve sadece kelime eşleşmesi değil, anlamsal (semantic) bir arama yaparak en uygun sonuçları döndürüyor.

## Kurulum ve Çalıştırma
Projeyi lokalinizde ayağa kaldırmak isterseniz:

1. Repoyu klonlayın:
   `git clone https://github.com/mertyerturun/locisight-backend.git`
2. Gerekli kütüphaneleri yükleyin:
   `pip install -r requirements.txt`
3. Çevresel değişkenleri (API key vb.) `.env` dosyasına ekleyin.
4. Uygulamayı başlatın:
   `python run.py`

*Not: Uygulama şu an Render üzerinde canlıdadır.*
Site: https://mertyerturun.wixstudio.com/locisight
