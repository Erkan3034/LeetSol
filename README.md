# 🚀 Universal LeetCode GitHub Sync Tool

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![PyQt5](https://img.shields.io/badge/PyQt5-GUI-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)

**LeetCode çözümlerinizi otomatik olarak GitHub'a senkronize eden ve AI destekli README dosyaları oluşturan profesyonel masaüstü uygulaması**

[📥 İndir](https://github.com/Erkan3034/LeetSol/releases) • [📖 Kılavuz](KULLANIM_KILAVUZU.md) • [🐛 Sorun Bildir](https://github.com/Erkan3034/LeetSol/issues) • [💬 Tartışma](https://github.com/Erkan3034/LeetSol/discussions)

</div>

## ✨ Özellikler

<table>
<tr>
<td width="50%">

### 🔄 **Otomatik Senkronizasyon**
- LeetCode çözümlerinizi belirlediğiniz sıklıkta GitHub'a senkronize eder
- Manuel ve otomatik senkronizasyon seçenekleri
- Arka planda çalışma desteği

### 🤖 **AI Destekli README**
- Gemini AI ile her çözüm için detaylı README.md dosyası oluşturur
- Problem açıklaması, çözüm yaklaşımı, karmaşıklık analizi
- Profesyonel ve akademik format

### 🔒 **Güvenli Saklama**
- Tüm API anahtarları ve token'lar şifrelenmiş olarak saklanır
- Fernet şifreleme ile maksimum güvenlik
- Yerel veri koruması

</td>
<td width="50%">

### 🎨 **Kullanıcı Dostu Arayüz**
- PyQt5 ile modern ve sezgisel masaüstü arayüzü
- Tab'lı ayarlar sistemi
- Gerçek zamanlı log takibi
- Sistem tepsisi desteği

### 🌐 **Çoklu Dil Desteği**
- Python, Java, JavaScript, C++, TypeScript
- LeetCode'un desteklediği tüm diller
- Otomatik dosya uzantısı algılama

### 📊 **Detaylı İzleme**
- Gerçek zamanlı senkronizasyon durumu
- İşlenen çözüm sayısı takibi
- Hata bildirimleri ve çözüm önerileri

</td>
</tr>
</table>

## 🎯 Hızlı Başlangıç

### 📦 **EXE İndirme (Önerilen)**
1. [Releases](https://github.com/Erkan3034/LeetSol/releases) sayfasından `LeetCodeSyncTool.exe` dosyasını indirin
2. Dosyayı istediğiniz klasöre kopyalayın
3. EXE dosyasını çift tıklayarak çalıştırın
4. İlk açılışta ayarları yapılandırın

### 🛠️ **Kaynak Koddan Çalıştırma**

#### Gereksinimler
- Python 3.10+
- Windows 10/11
- LeetCode hesabı
- GitHub hesabı
- Google Gemini API anahtarı

#### Kurulum
```bash
# Projeyi klonlayın
git clone https://github.com/Erkan3034/LeetSol.git
cd LeetSol

# Bağımlılıkları yükleyin
pip install -r requirements.txt

# Uygulamayı çalıştırın
python main.py
```

## 🔧 API Anahtarları ve Token'lar

### 🔑 **GitHub Personal Access Token**
1. GitHub → Settings → Developer settings → Personal access tokens
2. **Generate new token (classic)** tıklayın
3. **Scopes**: `repo` (tam erişim) seçin
4. Token'ı kopyalayın ve güvenli saklayın

### 🍪 **LeetCode Cookies**
1. LeetCode'a giriş yapın (https://leetcode.com)
2. **F12** tuşuna basarak Developer Tools'u açın
3. **Application/Storage** → **Cookies** → **https://leetcode.com**
4. Şu değerleri kopyalayın:
   - `LEETCODE_SESSION` (çok uzun değer)
   - `csrftoken` (kısa değer)

⚠️ **Önemli**: Cookie'ler sık sık değişir. Hata aldığınızda yenileyin.

### 🤖 **Gemini API Key**
1. [Google AI Studio](https://aistudio.google.com/) adresine gidin
2. Google hesabınızla giriş yapın
3. **Get API Key** → **Create API Key** tıklayın
4. Oluşturulan anahtarı kopyalayın

## 🚀 Kullanım

### 1️⃣ **İlk Kurulum**
1. Uygulamayı açın
2. **"Ayarları Aç"** butonuna tıklayın
3. Her sekmede gerekli bilgileri girin:
   - **GitHub**: Token, username, repository
   - **LeetCode**: Session ve CSRF token
   - **Gemini**: API key
   - **Senkronizasyon**: Aralık ve otomatik başlatma
4. **"Ayarları Kaydet"** butonuna tıklayın
5. **"Bağlantıları Test Et"** ile kontrol edin

### 2️⃣ **Senkronizasyon**
- **Otomatik**: Belirlenen aralıklarla otomatik çalışır
- **Manuel**: **"Manuel Senkronizasyon"** butonuna tıklayın
- **Durdurma**: **"Senkronizasyonu Durdur"** butonu ile durdurun

### 3️⃣ **GitHub'da Sonuç**
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

## 📁 Proje Yapısı

```
LeetSol/
├── 📄 main.py                 # Ana uygulama dosyası
├── ⚙️ config_gui.py          # Ayarlar arayüzü
├── 🔄 sync_logic.py          # Senkronizasyon mantığı
├── 🔗 leetcode_client.py      # LeetCode API istemcisi
├── 🐙 github_client.py       # GitHub API istemcisi
├── 🤖 gemini_client.py       # Gemini AI istemcisi
├── 🔨 build.py               # EXE oluşturma script'i
├── 📋 requirements.txt       # Python bağımlılıkları
├── 📝 env_template.txt       # Ortam değişkenleri şablonu
├── 📖 KULLANIM_KILAVUZU.md   # Detaylı kullanım kılavuzu
└── 📄 README.md             # Bu dosya
```

## 🔒 Güvenlik

- ✅ **Şifreli Saklama**: Tüm hassas veriler Fernet şifreleme ile korunur
- ✅ **Git Ignore**: `.env` dosyası Git ile takip edilmez
- ✅ **Minimal Yetkiler**: GitHub token'ında sadece gerekli yetkiler
- ✅ **Yerel Veri**: LeetCode cookie'leri sadece yerel olarak saklanır
- ✅ **Yedekleme**: Ayarlar değiştirilirken otomatik yedekleme

## 🐛 Sorun Giderme

### ❌ **Yaygın Hatalar ve Çözümleri**

<details>
<summary><b>LeetCode Bağlantı Sorunları</b></summary>

**Hata**: "Kullanıcı giriş yapmamış" veya "Cookie'lerin süresi dolmuş"

**Çözüm**:
1. LeetCode'a giriş yapın
2. F12 → Application → Cookies → https://leetcode.com
3. Yeni `LEETCODE_SESSION` ve `csrftoken` değerlerini kopyalayın
4. Ayarlar → LeetCode sekmesinde güncelleyin

</details>

<details>
<summary><b>GitHub Bağlantı Sorunları</b></summary>

**Hata**: "API key not valid" veya "Repository not found"

**Çözüm**:
1. GitHub Personal Access Token'ınızı kontrol edin
2. Token'ın `repo` yetkisi olduğundan emin olun
3. Repository adının doğru olduğunu kontrol edin
4. GitHub username'inizi kontrol edin

</details>

<details>
<summary><b>Gemini API Sorunları</b></summary>

**Hata**: "API key not valid"

**Çözüm**:
1. Google AI Studio'dan yeni API key alın
2. API key'in aktif olduğunu kontrol edin
3. Ayarlar → Gemini API sekmesinde güncelleyin

</details>

### 📊 **Log Takibi**
Uygulama içindeki log alanından tüm işlemleri gerçek zamanlı takip edebilirsiniz.

## 🔄 Güncellemeler

### **EXE Kullanıcıları**
1. [Releases](https://github.com/Erkan3034/LeetSol/releases) sayfasından yeni sürümü indirin
2. Mevcut `.env` dosyanızı koruyun
3. Yeni EXE dosyasıyla değiştirin

### **Kaynak Kodu Kullanıcıları**
```bash
git pull origin main
pip install -r requirements.txt
```

## 📈 Roadmap

- [ ] **v1.1**: Sistem tepsisi bildirimleri
- [ ] **v1.2**: Çoklu repository desteği
- [ ] **v1.3**: Özel README şablonları
- [ ] **v2.0**: Web arayüzü
- [ ] **v2.1**: Çoklu dil desteği (İngilizce)

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! 

1. **Fork** yapın
2. **Feature branch** oluşturun (`git checkout -b feature/amazing-feature`)
3. **Commit** yapın (`git commit -m 'Add amazing feature'`)
4. **Push** yapın (`git push origin feature/amazing-feature`)
5. **Pull Request** oluşturun

### 🐛 **Bug Report**
Sorunları [GitHub Issues](https://github.com/Erkan3034/LeetSol/issues) üzerinden bildirin.

### 💡 **Feature Request**
Yeni özellik önerilerinizi [Discussions](https://github.com/Erkan3034/LeetSol/discussions) bölümünde paylaşın.

## 📄 Lisans

Bu proje [MIT lisansı](LICENSE) altında lisanslanmıştır.

## ⭐ Yıldız Verin!

Bu proje size yardımcı olduysa, lütfen bir ⭐ verin!

## 📞 Destek

- 📧 **Email**: GitHub Issues üzerinden
- 💬 **Discussions**: GitHub Discussions
- 🐛 **Bug Reports**: GitHub Issues
- 📖 **Dokümantasyon**: [KULLANIM_KILAVUZU.md](KULLANIM_KILAVUZU.md)

---

<div align="center">

**⭐ Bu projeyi beğendiyseniz yıldız verin! ⭐**

Made with ❤️ by [Erkan3034](https://github.com/Erkan3034)

</div>
