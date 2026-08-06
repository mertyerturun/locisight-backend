import requests
from config import Config

class AIServiceError(Exception):
    """Yapay zeka servisi (Groq) hatalarını yakalamak için özel hata sınıfımız."""
    pass

class AIService:
    def __init__(self):
        self.api_key = Config.GROQ_API_KEY
        self.model = "llama-3.1-8b-instant"
        self.url = "https://api.groq.com/openai/v1/chat/completions"

    def _get_system_prompt(self):
        """Locisight'ın kurumsal kimliğini ve çalışma mantığını döndürür."""
        return Config.BUSINESS_CONTEXT

    def yanit_uret(self, mesaj, gecmis=None):
        """Kullanıcının mesajını ve geçmiş sohbeti alıp yapay zekadan yanıt üretir."""
        
        if not self.api_key:
            return "Demo Modu: API anahtarı bulunamadı. Locisight asistanı şu an test modundadır. Sorunuzu aldım: " + mesaj
            
        if gecmis is None:
            gecmis = []

        messages = [{"role": "system", "content": self._get_system_prompt()}]
        
        for g in gecmis:
            if "mesaj" in g:
                messages.append({"role": "user", "content": g["mesaj"]})
            # Asistanın önceki cevapları
            if "cevap" in g:
                messages.append({"role": "assistant", "content": g["cevap"]})
                
        messages.append({"role": "user", "content": mesaj})

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": messages
        }

        try:
            response = requests.post(self.url, json=payload, headers=headers)
            response.raise_for_status() # HTTP hatası varsa exception fırlatır
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            # Hata durumunda kendi oluşturduğumuz hata sınıfını fırlatıyoruz
            raise AIServiceError(f"Locisight AI servisine ulaşılamadı: {str(e)}")

ai_service = AIService()