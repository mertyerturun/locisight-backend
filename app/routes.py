import hmac
from functools import wraps

from flask import Blueprint, request, jsonify, current_app
from app.database import lead_ekle, tum_leadler
from app.services.ai_service import ai_service, AIServiceError

api_bp = Blueprint('api', __name__)

def admin_gerekli(f):
    """Endpoint'i 'Authorization: Bearer <ADMIN_API_KEY>' başlığıyla korur."""
    @wraps(f)
    def sarmalayici(*args, **kwargs):
        beklenen = current_app.config.get('ADMIN_API_KEY')
        # Anahtar tanımlı değilse endpoint tamamen kapalı kalır (fail closed)
        if not beklenen:
            return jsonify({'basari': False, 'hata': 'Bu endpoint yapılandırılmamış.'}), 503

        baslik = request.headers.get('Authorization', '')
        gelen = baslik[7:] if baslik.startswith('Bearer ') else ''
        # Zamanlama saldırılarına karşı sabit süreli karşılaştırma
        if not hmac.compare_digest(gelen.encode(), beklenen.encode()):
            return jsonify({'basari': False, 'hata': 'Yetkisiz erişim.'}), 401

        return f(*args, **kwargs)
    return sarmalayici

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Sunucunun ayakta olup olmadığını kontrol eder."""
    return jsonify({'durum': 'aktif', 'mesaj': 'Locisight sunucusu başarıyla çalışıyor.'}), 200

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
@admin_gerekli
def lead_listele():
    """B2B paneli için tüm müşteri kayıtlarını getirir."""
    leadler = tum_leadler()
    return jsonify({'basari': True, 'veri': leadler}), 200