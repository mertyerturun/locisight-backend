from flask import Blueprint, render_template, request, jsonify
from app.database import lead_ekle, tum_leadler
from app.services.ai_service import ai_service, AIServiceError

pages_bp = Blueprint('pages', __name__)

api_bp = Blueprint('api', __name__)

@pages_bp.route('/')
def index():
    """B2C Karşılama sayfasını (Sohbet ekranı) gösterir."""
    return render_template('index.html')

@pages_bp.route('/dashboard')
def dashboard():
    """B2B Yönetim panelini (Gelen leadleri listeleme) gösterir."""
    return render_template('dashboard.html')


@api_bp.route('/sohbet', methods=['POST'])
def sohbet():
    """Kullanıcının yazdığı mesajı alıp Locisight yapay zekasına iletir."""
    veri = request.get_json()
    
    if not veri or 'mesaj' not in veri:
        return jsonify({'basari': False, 'hata': 'Mesaj alanı eksik.'}), 400
        
    mesaj = veri['mesaj']
    gecmis = veri.get('gecmis', [])
    
    try:
        cevap = ai_service.yanit_uret(mesaj, gecmis)
        return jsonify({'basari': True, 'cevap': cevap}), 200
    except AIServiceError as e:
        return jsonify({'basari': False, 'hata': 'Asistan şu an yoğun, lütfen daha sonra tekrar deneyin.'}), 503

@api_bp.route('/leads', methods=['POST'])
def lead_kaydet():
    """Kullanıcının iletişim bilgilerini ve Locisight kriterlerini veritabanına kaydeder."""
    veri = request.get_json()
    
    if not veri or 'isim' not in veri or 'telefon' not in veri:
        return jsonify({'basari': False, 'hata': 'İsim ve telefon alanları zorunludur.'}), 400
        
    isim = veri['isim']
    telefon = veri['telefon']
    mesaj = veri.get('mesaj', '')
    kriter = veri.get('kriter', '')
    
    lead_ekle(isim, telefon, mesaj, kriter)
    
    return jsonify({'basari': True, 'mesaj': 'Talebiniz başarıyla alındı.'}), 201

@api_bp.route('/leads', methods=['GET'])
def lead_listele():
    """B2B paneli için tüm müşteri kayıtlarını getirir."""
    leadler = tum_leadler()
    return jsonify({'basari': True, 'veri': leadler}), 200