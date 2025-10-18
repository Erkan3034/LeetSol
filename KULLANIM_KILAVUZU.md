# 🚀 Universal LeetCode GitHub Sync Tool - Kullanım Kılavuzu

## 📋 İçindekiler
1. [Genel Bakış](#genel-bakış)
2. [Kurulum](#kurulum)
3. [İlk Kurulum](#ilk-kurulum)
4. [API Anahtarları](#api-anahtarları)
5. [Kullanım](#kullanım)
6. [Sorun Giderme](#sorun-giderme)
7. [Sık Sorulan Sorular](#sık-sorulan-sorular)

## 🎯 Genel Bakış

**Universal LeetCode GitHub Sync Tool**, LeetCode çözümlerinizi otomatik olarak GitHub'a yükleyen ve AI destekli README dosyaları oluşturan profesyonel bir araçtır.

### ✨ Özellikler
- 🔄 **Otomatik Senkronizasyon**: LeetCode çözümlerinizi GitHub'a otomatik yükler
- 🤖 **AI Destekli README**: Gemini AI ile profesyonel dokümantasyon oluşturur
- 🔒 **Güvenli Şifreleme**: Tüm API anahtarları şifrelenmiş olarak saklanır
- ⚙️ **Kolay Yapılandırma**: Kullanıcı dostu arayüz ile basit kurulum
- 📊 **Detaylı Loglar**: Tüm işlemler loglanır ve takip edilir
- 🔔 **Bildirimler**: Hata ve başarı durumları için bildirimler

## 📦 Kurulum

### Gereksinimler
- Windows 10/11
- İnternet bağlantısı
- GitHub hesabı
- LeetCode hesabı
- Google AI Studio hesabı (Gemini API için)

### Kurulum Adımları
1. `LeetCodeSyncTool.exe` dosyasını indirin
2. Dosyayı istediğiniz klasöre kopyalayın
3. EXE dosyasını çift tıklayarak çalıştırın
4. İlk çalıştırmada ayarları yapılandırın

## 🔧 İlk Kurulum

### 1. GitHub Ayarları

#### GitHub Personal Access Token Oluşturma
1. GitHub'a giriş yapın
2. **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)**
3. **Generate new token (classic)** butonuna tıklayın
4. Token ayarları:
   - **Note**: "LeetCode Sync Tool"
   - **Expiration**: İstediğiniz süre (önerilen: 1 yıl)
   - **Scopes**: `repo` (tam erişim) seçin
5. **Generate token** butonuna tıklayın
6. Oluşturulan token'ı kopyalayın ve güvenli bir yerde saklayın

#### GitHub Repository Bilgileri
- **Username**: GitHub kullanıcı adınız
- **Repository**: Çözümlerin yükleneceği repository adı

### 2. LeetCode Ayarları

#### Cookie'leri Alma
1. LeetCode'a giriş yapın (https://leetcode.com)
2. **F12** tuşuna basarak Developer Tools'u açın
3. **Application** (veya **Storage**) sekmesine gidin
4. **Cookies** → **https://leetcode.com** seçin
5. Şu değerleri kopyalayın:
   - `LEETCODE_SESSION`: Çok uzun bir değer (tamamını kopyalayın)
   - `csrftoken`: Kısa bir değer

⚠️ **Önemli**: Cookie'ler sık sık değişir. Hata aldığınızda yenileyin.

### 3. Gemini API Ayarları

#### API Key Alma
1. Google AI Studio'ya gidin (https://aistudio.google.com/)
2. Google hesabınızla giriş yapın
3. **Get API Key** butonuna tıklayın
4. **Create API Key** seçin
5. Oluşturulan API key'i kopyalayın

## 🎮 Kullanım

### Ayarları Yapılandırma
1. Uygulamayı açın
2. **Ayarları Aç** butonuna tıklayın
3. Her sekmede gerekli bilgileri girin:
   - **GitHub**: Token, username, repository
   - **LeetCode**: Session ve CSRF token
   - **Gemini**: API key
   - **Senkronizasyon**: Aralık ve otomatik başlatma
4. **Ayarları Kaydet** butonuna tıklayın
5. **Bağlantıları Test Et** ile kontrol edin

### Senkronizasyon
- **Otomatik**: Belirlenen aralıklarla otomatik çalışır
- **Manuel**: İstediğiniz zaman **Manuel Senkronizasyon** butonuna tıklayın
- **Durdurma**: **Senkronizasyonu Durdur** butonu ile durdurun

### GitHub'da Sonuç
Çözümleriniz şu formatta GitHub'a yüklenir:
```
Repository/
├── longest-substring-without-repeating-characters/
│   ├── solution.py
│   └── README.md
├── two-sum/
│   ├── solution.py
│   └── README.md
└── ...
```

## 🔧 Sorun Giderme

### LeetCode Bağlantı Sorunları
**Hata**: "Kullanıcı giriş yapmamış" veya "Cookie'lerin süresi dolmuş"

**Çözüm**:
1. LeetCode'a giriş yapın
2. F12 → Application → Cookies → https://leetcode.com
3. Yeni `LEETCODE_SESSION` ve `csrftoken` değerlerini kopyalayın
4. Ayarlar → LeetCode sekmesinde güncelleyin

### GitHub Bağlantı Sorunları
**Hata**: "API key not valid" veya "Repository not found"

**Çözüm**:
1. GitHub Personal Access Token'ınızı kontrol edin
2. Token'ın `repo` yetkisi olduğundan emin olun
3. Repository adının doğru olduğunu kontrol edin
4. GitHub username'inizi kontrol edin

### Gemini API Sorunları
**Hata**: "API key not valid"

**Çözüm**:
1. Google AI Studio'dan yeni API key alın
2. API key'in aktif olduğunu kontrol edin
3. Ayarlar → Gemini API sekmesinde güncelleyin

### Genel Sorunlar
- **Uygulama açılmıyor**: Windows Defender'ı kontrol edin
- **Yavaş çalışıyor**: İnternet bağlantınızı kontrol edin
- **Ayarlar kayboluyor**: `.env` dosyasının silinmediğinden emin olun

## ❓ Sık Sorulan Sorular

### Q: Cookie'leri ne sıklıkla yenilemem gerekiyor?
A: LeetCode güvenlik nedeniyle cookie'leri sık yeniler. Hata aldığınızda yenileyin.

### Q: Hangi programlama dilleri destekleniyor?
A: Python, Java, C++, JavaScript, TypeScript ve diğer LeetCode desteklediği diller.

### Q: README dosyaları nasıl oluşturuluyor?
A: Gemini AI ile otomatik oluşturulur. Problem açıklaması, çözüm yaklaşımı, karmaşıklık analizi içerir.

### Q: Uygulama arka planda çalışabilir mi?
A: Evet, sistem tepsisi ikonu ile arka planda çalışabilir.

### Q: Verilerim güvenli mi?
A: Evet, tüm API anahtarları şifrelenmiş olarak saklanır. `.env` dosyasını paylaşmayın.

### Q: Ücretsiz mi?
A: Uygulama ücretsizdir. Sadece GitHub ve Gemini API limitleri geçerlidir.

## 📞 Destek

Sorun yaşıyorsanız:
1. Bu kılavuzu tekrar okuyun
2. Log dosyalarını kontrol edin
3. Ayarları yeniden yapılandırın
4. Cookie'leri yenileyin

## 🔄 Güncellemeler

Uygulama otomatik güncellenmez. Yeni sürümler için GitHub repository'sini kontrol edin.

---

## 👨‍💻 Geliştirici

**Erkan TURGUT**

- **LinkedIn**: [@erkanturgut1205](https://www.linkedin.com/in/erkanturgut1205/)
- **Portfolio**: [erkanturgut.netlify.app](https://erkanturgut.netlify.app/)
- **GitHub**: [@Erkan3034](https://github.com/Erkan3034)

---

**Not**: Bu araç LeetCode, GitHub ve Google Gemini API'lerini kullanır. Bu servislerin kullanım şartlarına uygun olarak kullanın.
