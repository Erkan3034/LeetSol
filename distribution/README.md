# 🚀 Universal LeetCode GitHub Sync Tool v1.0

## 📦 Dağıtım Paketi İçeriği

Bu paket aşağıdaki dosyaları içerir:

- **LeetCodeSyncTool.exe** - Ana uygulama (135 MB)
- **KULLANIM_KILAVUZU.md** - Detaylı kullanım kılavuzu
- **env_template.txt** - Ayarlar şablonu

## 🚀 Hızlı Başlangıç

1. **LeetCodeSyncTool.exe** dosyasını çalıştırın
2. İlk açılışta ayarlar ekranı otomatik açılacak
3. Gerekli API anahtarlarını girin:
   - GitHub Personal Access Token
   - LeetCode Session Cookies
   - Gemini API Key
4. Ayarları kaydedin ve test edin
5. Senkronizasyonu başlatın

## 📋 Gereksinimler

- Windows 10/11
- İnternet bağlantısı
- GitHub hesabı
- LeetCode hesabı
- Google AI Studio hesabı

## 🔧 API Anahtarları

### GitHub
1. GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. `repo` yetkisi verin

### LeetCode
1. LeetCode'a giriş yapın
2. F12 → Application → Cookies → https://leetcode.com
3. `LEETCODE_SESSION` ve `csrftoken` değerlerini kopyalayın

### Gemini
1. Google AI Studio'ya gidin (https://aistudio.google.com/)
2. Get API Key → Create API Key

## ⚠️ Önemli Notlar

- Cookie'ler sık sık değişir, hata aldığınızda yenileyin
- `.env` dosyasını güvenli tutun ve paylaşmayın
- İlk çalıştırmada internet bağlantısı gereklidir
- Windows Defender uyarısı normaldir (güvenilir uygulama)

## 🆘 Sorun Giderme

Detaylı sorun giderme için **KULLANIM_KILAVUZU.md** dosyasını okuyun.

## 📞 Destek

Sorun yaşıyorsanız:
1. Kullanım kılavuzunu okuyun
2. Cookie'leri yenileyin
3. Ayarları yeniden yapılandırın

---

**Versiyon**: 1.0  
**Boyut**: ~135 MB  
**Platform**: Windows 10/11  
**Lisans**: Ücretsiz
