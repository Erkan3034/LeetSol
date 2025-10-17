# build.py - PyInstaller ile EXE oluşturma script'i

import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_exe():
    """PyInstaller ile EXE dosyası oluştur"""
    
    print("🚀 Universal LeetCode GitHub Sync Tool - EXE Build Script")
    print("=" * 60)
    
    # Gerekli dosyaların varlığını kontrol et
    required_files = [
        'main.py',
        'config_gui.py', 
        'sync_logic.py',
        'leetcode_client.py',
        'github_client.py',
        'gemini_client.py',
        'requirements.txt'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Eksik dosyalar: {', '.join(missing_files)}")
        return False
    
    print("✅ Tüm gerekli dosyalar mevcut")
    
    # PyInstaller komutunu hazırla
    pyinstaller_cmd = [
        'pyinstaller',
        '--onefile',                    # Tek dosya olarak paketle
        '--windowed',                   # GUI uygulaması (konsol penceresi gösterme)
        '--name=LeetCodeSyncTool',      # EXE dosya adı
        '--icon=icon.ico',              # İkon dosyası (varsa)
        '--add-data=env_template.txt;.', # Template dosyasını dahil et
        '--hidden-import=PyQt5.QtCore',
        '--hidden-import=PyQt5.QtGui', 
        '--hidden-import=PyQt5.QtWidgets',
        '--hidden-import=requests',
        '--hidden-import=google.generativeai',
        '--hidden-import=cryptography',
        '--hidden-import=dotenv',
        'main.py'
    ]
    
    # İkon dosyası yoksa kaldır
    if not os.path.exists('icon.ico'):
        pyinstaller_cmd.remove('--icon=icon.ico')
    
    print("🔨 PyInstaller ile EXE oluşturuluyor...")
    print(f"Komut: {' '.join(pyinstaller_cmd)}")
    
    try:
        # PyInstaller'ı çalıştır
        result = subprocess.run(pyinstaller_cmd, check=True, capture_output=True, text=True)
        
        print("✅ EXE dosyası başarıyla oluşturuldu!")
        
        # Dist klasöründeki EXE dosyasını kontrol et
        exe_path = Path('dist/LeetCodeSyncTool.exe')
        if exe_path.exists():
            print(f"📁 EXE dosyası: {exe_path.absolute()}")
            print(f"📊 Dosya boyutu: {exe_path.stat().st_size / (1024*1024):.2f} MB")
        
        # Kullanım talimatları
        print("\n" + "=" * 60)
        print("📋 KULLANIM TALİMATLARI:")
        print("=" * 60)
        print("1. EXE dosyasını istediğiniz klasöre kopyalayın")
        print("2. İlk çalıştırmada ayarları yapılandırın:")
        print("   - GitHub Personal Access Token")
        print("   - LeetCode Session Cookies")
        print("   - Gemini API Key")
        print("3. Senkronizasyonu başlatın")
        print("\n⚠️  ÖNEMLİ:")
        print("- EXE dosyası ile birlikte .env dosyası oluşturulacak")
        print("- Bu dosyayı güvenli tutun ve paylaşmayın")
        print("- İlk çalıştırmada internet bağlantısı gereklidir")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ PyInstaller hatası: {e}")
        print(f"Stderr: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Beklenmeyen hata: {e}")
        return False

def clean_build():
    """Build dosyalarını temizle"""
    print("\n🧹 Build dosyaları temizleniyor...")
    
    dirs_to_remove = ['build', 'dist', '__pycache__']
    files_to_remove = ['LeetCodeSyncTool.spec']
    
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✅ {dir_name} klasörü silindi")
    
    for file_name in files_to_remove:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"✅ {file_name} dosyası silindi")

def main():
    """Ana fonksiyon"""
    
    if len(sys.argv) > 1 and sys.argv[1] == '--clean':
        clean_build()
        return
    
    # PyInstaller'ın yüklü olup olmadığını kontrol et
    try:
        subprocess.run(['pyinstaller', '--version'], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ PyInstaller yüklü değil!")
        print("Yüklemek için: pip install pyinstaller")
        return
    
    # Build işlemini başlat
    success = build_exe()
    
    if success:
        print("\n🎉 Build işlemi tamamlandı!")
        print("EXE dosyasını dist/ klasöründe bulabilirsiniz.")
    else:
        print("\n💥 Build işlemi başarısız!")
        print("Hata detaylarını yukarıda kontrol edin.")

if __name__ == "__main__":
    main()
