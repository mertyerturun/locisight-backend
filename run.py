from app import create_app

# Fabrika fonksiyonumuzdan uygulamayı alıyoruz
app = create_app()

# Sunucuyu sadece bu dosya doğrudan çalıştırıldığında ayağa kaldırıyoruz
if __name__ == '__main__':
    app.run(port=5000, debug=True)