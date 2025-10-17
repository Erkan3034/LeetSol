# Universal LeetCode GitHub Sync Tool

Bu proje, LeetCode çözümlerinizi otomatik olarak GitHub repository'nize senkronize eden bir masaüstü uygulamasıdır. Uygulama, yeni LeetCode çözümlerini algılar, Gemini AI ile detaylı README dosyaları oluşturur ve GitHub'a yükler.

## 🚀 Özellikler

- **Otomatik Senkronizasyon**: LeetCode çözümlerinizi belirlediğiniz sıklıkta GitHub'a senkronize eder
- **AI Destekli README**: Gemini AI ile her çözüm için detaylı README.md dosyası oluşturur
- **Güvenli Saklama**: Tüm API anahtarları ve token'lar şifrelenmiş olarak saklanır
- **Kullanıcı Dostu Arayüz**: PyQt5 ile modern ve sezgisel masaüstü arayüzü
- **Sistem Tepsisi Desteği**: Uygulama arka planda çalışabilir
- **Çoklu Dil Desteği**: Python, Java, JavaScript, C++ ve daha fazlası

## 📋 Gereksinimler

- Python 3.10+
- Windows 10/11
- LeetCode hesabı
- GitHub hesabı
- Google Gemini API anahtarı

## 🛠️ Kurulum

### 1. Projeyi İndirin
```bash
git clone <repository-url>
cd LeetSol
```

### 2. Gerekli Kütüphaneleri Yükleyin
```bash
pip install -r requirements.txt
```

### 3. Ayarları Yapılandırın
1. `env_template.txt` dosyasını `.env` olarak kopyalayın
2. Kendi API anahtarlarınızı ve token'larınızı girin
3. Uygulamayı çalıştırın

## 🔧 API Anahtarları ve Token'lar

### GitHub Personal Access Token
1. GitHub > Settings > Developer settings > Personal access tokens
2. "Generate new token" tıklayın
3. Sadece "repo" yetkisini seçin
4. Token'ı kopyalayın

### LeetCode Cookies
1. LeetCode'a giriş yapın
2. F12 tuşuna basarak Developer Tools'u açın
3. Application/Storage > Cookies > https://leetcode.com
4. `LEETCODE_SESSION` ve `csrftoken` değerlerini kopyalayın

### Gemini API Key
1. https://makersuite.google.com/app/apikey adresine gidin
2. Google hesabınızla giriş yapın
3. "Create API Key" butonuna tıklayın
4. Oluşturulan anahtarı kopyalayın

## 🚀 Kullanım

### Uygulamayı Başlatma
```bash
python main.py
```

### İlk Kurulum
1. Uygulama açıldığında "Ayarları Aç" butonuna tıklayın
2. Tüm API anahtarlarınızı ve token'larınızı girin
3. "Ayarları Kaydet" butonuna tıklayın
4. "Bağlantıları Test Et" ile ayarlarınızı doğrulayın

### Senkronizasyonu Başlatma
1. Ana ekranda "Senkronizasyonu Başlat" butonuna tıklayın
2. Uygulama otomatik olarak yeni çözümleri kontrol etmeye başlar
3. Yeni çözüm bulunduğunda otomatik olarak GitHub'a yüklenir

## 📁 Dosya Yapısı

```
LeetSol/
├── main.py                 # Ana uygulama dosyası
├── config_gui.py          # Ayarlar arayüzü
├── sync_logic.py          # Senkronizasyon mantığı
├── leetcode_client.py      # LeetCode API istemcisi
├── github_client.py       # GitHub API istemcisi
├── gemini_client.py       # Gemini AI istemcisi
├── requirements.txt       # Python bağımlılıkları
├── env_template.txt       # Ortam değişkenleri şablonu
└── README.md             # Bu dosya
```

## 🔒 Güvenlik

- Tüm hassas veriler (token'lar, API anahtarları) şifrelenmiş olarak saklanır
- `.env` dosyası `.gitignore` ile korunur
- GitHub token'ınızda sadece gerekli yetkiler bulunur
- LeetCode cookie'leri sadece yerel olarak saklanır

## 📊 Repository Yapısı

Uygulama, GitHub repository'nizde şu yapıyı oluşturur:

```
your-repo/
├── two-sum/
│   ├── solution.py
│   └── README.md
├── valid-parentheses/
│   ├── solution.js
│   └── README.md
└── ...
```

Her problem için:
- Ayrı bir klasör oluşturulur
- Çözüm kodu `solution.{extension}` olarak kaydedilir
- Gemini AI ile oluşturulan README.md dosyası eklenir

## 🐛 Sorun Giderme

### Yaygın Hatalar

1. **"API istemcileri başlatılamadı"**
   - API anahtarlarınızı kontrol edin
   - İnternet bağlantınızı kontrol edin

2. **"LeetCode bağlantısı başarısız"**
   - Cookie'lerinizi yenileyin
   - LeetCode'a giriş yaptığınızdan emin olun

3. **"GitHub commit başarısız"**
   - Token yetkilerinizi kontrol edin
   - Repository'nin var olduğundan emin olun

### Log Dosyaları
Uygulama içindeki log alanından tüm işlemleri takip edebilirsiniz.

## 🔄 Güncellemeler

Uygulamayı güncellemek için:
1. Yeni sürümü indirin
2. Mevcut `.env` dosyanızı koruyun
3. Yeni dosyalarla değiştirin

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add amazing feature'`)
4. Push yapın (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📞 Destek

Sorunlarınız için GitHub Issues kullanabilirsiniz.

---

**Not**: Bu uygulama eğitim amaçlıdır. LeetCode'un kullanım şartlarına uygun şekilde kullanın.
