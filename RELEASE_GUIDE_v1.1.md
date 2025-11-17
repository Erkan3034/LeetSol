# 🚀 v1.1 Release Oluşturma Kılavuzu

## Adımlar:

1. **GitHub'a Git**: https://github.com/Erkan3034/LeetSol/releases/new

2. **Release Bilgilerini Doldur**:
   - **Tag**: `v1.1` (zaten oluşturuldu)
   - **Title**: `v1.1 - Cookie Güncelleme Sorunu Düzeltildi`
   - **Description**: Aşağıdaki release notes'u kopyala-yapıştır yap

3. **Release Notes** (Aşağıdaki metni kopyala):

```markdown
# 🚀 LeetCode Sync Tool v1.1 - Release Notes

## ✨ Yeni Özellikler ve İyileştirmeler

### 🔧 **Kritik Hata Düzeltmeleri**

#### 1. **Cookie Güncelleme Sorunu Çözüldü** ✅
- **Sorun**: Ayarlarda cookie'ler güncellendiğinde uygulama eski cookie'leri kullanmaya devam ediyordu
- **Çözüm**: `.env` dosyasındaki değişikliklerin anında yüklenmesi için `load_dotenv(override=True)` eklendi
- **Sonuç**: Cookie'ler güncellendiğinde uygulama yeniden başlatılmadan yeni değerleri kullanıyor

#### 2. **Ayarlar Yükleme İyileştirmesi** 🔄
- Ayarlar penceresinde cookie'ler ve token'lar güncellendiğinde anında yükleniyor
- Bağlantı testi yapılırken güncel ayarlar kullanılıyor
- Daha tutarlı ve güvenilir ayar yönetimi

### 🐛 **Hata Düzeltmeleri**

- **LeetCode Cookie Uyarısı**: Cookie'ler güncellendiğinde artık gereksiz uyarılar gösterilmiyor
- **Ayarlar Senkronizasyonu**: Ayarlar kaydedildikten sonra SyncManager otomatik olarak yeniden başlatılıyor
- **Ortam Değişkenleri**: `.env` dosyasındaki değişikliklerin anında algılanması sağlandı

### 📋 **Teknik İyileştirmeler**

- `sync_logic.py`: `load_dotenv(override=True)` eklendi
- `config_gui.py`: Ayarlar yüklenirken ve test edilirken `override=True` kullanılıyor
- Daha iyi hata yönetimi ve kullanıcı geri bildirimi

## 📦 **Kurulum**

1. [Releases](https://github.com/Erkan3034/LeetSol/releases) sayfasından `LeetCodeSyncTool.exe` dosyasını indirin
2. Dosyayı istediğiniz klasöre kopyalayın
3. EXE dosyasını çift tıklayarak çalıştırın
4. İlk açılışta ayarları yapılandırın

## 🔄 **Güncelleme**

Eğer v1.0 kullanıyorsanız:
1. Yeni `LeetCodeSyncTool.exe` dosyasını indirin
2. Mevcut `.env` dosyanızı koruyun (ayarlarınız kaybolmaz)
3. Eski EXE dosyasını yeni sürümle değiştirin
4. Uygulamayı çalıştırın

## ⚠️ **Önemli Notlar**

- Cookie'lerinizi güncelledikten sonra artık uygulamayı yeniden başlatmanıza gerek yok
- Ayarlar kaydedildikten sonra otomatik olarak yüklenir
- Tüm hassas veriler şifrelenmiş olarak saklanmaya devam ediyor

## 🙏 **Teşekkürler**

Bu sürümdeki iyileştirmeler kullanıcı geri bildirimlerine dayanmaktadır. Lütfen sorun bildirimi ve önerilerinizi [GitHub Issues](https://github.com/Erkan3034/LeetSol/issues) üzerinden paylaşın.

---

**Sürüm**: v1.1  
**Tarih**: 2025-01-27  
**Boyut**: ~145 MB  
**Platform**: Windows 10/11
```

4. **EXE Dosyasını Yükle**:
   - "Attach binaries by dropping them here or selecting them" bölümüne tıkla
   - `distribution/LeetCodeSyncTool.exe` dosyasını seç (veya `dist/LeetCodeSyncTool.exe`)

5. **"Publish release"** butonuna tıkla

## ✅ Hazır!

Release oluşturulduktan sonra kullanıcılar https://github.com/Erkan3034/LeetSol/releases adresinden v1.1'i indirebilecekler.

