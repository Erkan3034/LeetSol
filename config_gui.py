import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QComboBox, QTextEdit, QGroupBox, QMessageBox,
                             QTabWidget, QFormLayout, QCheckBox, QSpinBox)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont, QIcon
from dotenv import load_dotenv
from cryptography.fernet import Fernet
import base64

class ConfigWindow(QMainWindow):
    """Ana ayarlar penceresi"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Universal LeetCode GitHub Sync Tool")
        self.setGeometry(100, 100, 800, 600)
        
        # Ana widget ve layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Tab widget oluştur
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # Tab'ları oluştur
        self.create_github_tab()
        self.create_leetcode_tab()
        self.create_gemini_tab()
        self.create_sync_tab()
        
        # Alt kısımda butonlar
        button_layout = QHBoxLayout()
        
        self.save_button = QPushButton("Ayarları Kaydet")
        self.save_button.clicked.connect(self.save_settings)
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        
        self.test_button = QPushButton("Bağlantıları Test Et")
        self.test_button.clicked.connect(self.test_connections)
        self.test_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        
        self.start_sync_button = QPushButton("Senkronizasyonu Başlat")
        self.start_sync_button.clicked.connect(self.start_sync)
        self.start_sync_button.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
        """)
        
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.test_button)
        button_layout.addWidget(self.start_sync_button)
        button_layout.addStretch()
        
        main_layout.addLayout(button_layout)
        
        # Ayarları yükle
        self.load_settings()
        
    def create_github_tab(self):
        """GitHub ayarları tab'ı"""
        github_widget = QWidget()
        layout = QVBoxLayout(github_widget)
        
        # GitHub bilgileri grubu
        github_group = QGroupBox("GitHub Ayarları")
        github_layout = QFormLayout(github_group)
        
        self.github_token = QLineEdit()
        self.github_token.setEchoMode(QLineEdit.Password)
        self.github_token.setPlaceholderText("GitHub Personal Access Token")
        github_layout.addRow("GitHub Token:", self.github_token)
        
        self.github_username = QLineEdit()
        self.github_username.setPlaceholderText("GitHub kullanıcı adınız")
        github_layout.addRow("GitHub Kullanıcı Adı:", self.github_username)
        
        self.github_repo = QLineEdit()
        self.github_repo.setPlaceholderText("Repository adı")
        github_layout.addRow("Repository Adı:", self.github_repo)
        
        layout.addWidget(github_group)
        
        # Uyarı metni
        warning_text = QLabel("""
        <b>Önemli:</b> GitHub Personal Access Token'ınızda sadece 'repo' yetkisi olmalıdır.
        Token'ınızı GitHub > Settings > Developer settings > Personal access tokens'dan oluşturabilirsiniz.
        """)
        warning_text.setWordWrap(True)
        warning_text.setStyleSheet("color: #FF5722; background-color: #FFF3E0; padding: 10px; border-radius: 5px;")
        layout.addWidget(warning_text)
        
        layout.addStretch()
        self.tab_widget.addTab(github_widget, "GitHub")
        
    def create_leetcode_tab(self):
        """LeetCode ayarları tab'ı"""
        leetcode_widget = QWidget()
        layout = QVBoxLayout(leetcode_widget)
        
        # LeetCode bilgileri grubu
        leetcode_group = QGroupBox("LeetCode Ayarları")
        leetcode_layout = QFormLayout(leetcode_group)
        
        self.leetcode_session = QLineEdit()
        self.leetcode_session.setEchoMode(QLineEdit.Password)
        self.leetcode_session.setPlaceholderText("LEETCODE_SESSION cookie değeri")
        leetcode_layout.addRow("LeetCode Session:", self.leetcode_session)
        
        self.csrf_token = QLineEdit()
        self.csrf_token.setEchoMode(QLineEdit.Password)
        self.csrf_token.setPlaceholderText("csrftoken cookie değeri")
        leetcode_layout.addRow("CSRF Token:", self.csrf_token)
        
        layout.addWidget(leetcode_group)
        
        # Cookie alma talimatları
        instructions_text = QLabel("""
        <b>Cookie'leri Nasıl Alırım?</b><br>
        1. LeetCode'a giriş yapın<br>
        2. F12 tuşuna basarak Developer Tools'u açın<br>
        3. Application/Storage > Cookies > https://leetcode.com<br>
        4. 'LEETCODE_SESSION' ve 'csrftoken' değerlerini kopyalayın
        """)
        instructions_text.setWordWrap(True)
        instructions_text.setStyleSheet("color: #1976D2; background-color: #E3F2FD; padding: 10px; border-radius: 5px;")
        layout.addWidget(instructions_text)
        
        layout.addStretch()
        self.tab_widget.addTab(leetcode_widget, "LeetCode")
        
    def create_gemini_tab(self):
        """Gemini API ayarları tab'ı"""
        gemini_widget = QWidget()
        layout = QVBoxLayout(gemini_widget)
        
        # Gemini bilgileri grubu
        gemini_group = QGroupBox("Gemini API Ayarları")
        gemini_layout = QFormLayout(gemini_group)
        
        self.gemini_api_key = QLineEdit()
        self.gemini_api_key.setEchoMode(QLineEdit.Password)
        self.gemini_api_key.setPlaceholderText("Gemini API anahtarınız")
        gemini_layout.addRow("Gemini API Key:", self.gemini_api_key)
        
        layout.addWidget(gemini_group)
        
        # API anahtarı alma talimatları
        api_instructions = QLabel("""
        <b>Gemini API Anahtarı Nasıl Alırım?</b><br>
        1. https://makersuite.google.com/app/apikey adresine gidin<br>
        2. Google hesabınızla giriş yapın<br>
        3. "Create API Key" butonuna tıklayın<br>
        4. Oluşturulan anahtarı kopyalayın
        """)
        api_instructions.setWordWrap(True)
        api_instructions.setStyleSheet("color: #1976D2; background-color: #E3F2FD; padding: 10px; border-radius: 5px;")
        layout.addWidget(api_instructions)
        
        layout.addStretch()
        self.tab_widget.addTab(gemini_widget, "Gemini API")
        
    def create_sync_tab(self):
        """Senkronizasyon ayarları tab'ı"""
        sync_widget = QWidget()
        layout = QVBoxLayout(sync_widget)
        
        # Senkronizasyon ayarları grubu
        sync_group = QGroupBox("Senkronizasyon Ayarları")
        sync_layout = QFormLayout(sync_group)
        
        self.sync_interval = QComboBox()
        self.sync_interval.addItems([
            "5 dakika",
            "15 dakika", 
            "30 dakika",
            "1 saat",
            "2 saat",
            "6 saat",
            "12 saat",
            "24 saat"
        ])
        self.sync_interval.setCurrentText("30 dakika")
        sync_layout.addRow("Senkronizasyon Sıklığı:", self.sync_interval)
        
        self.auto_start = QCheckBox("Uygulama başladığında otomatik senkronizasyonu başlat")
        self.auto_start.setChecked(True)
        sync_layout.addRow(self.auto_start)
        
        self.notifications = QCheckBox("Yeni çözüm bulunduğunda bildirim göster")
        self.notifications.setChecked(True)
        sync_layout.addRow(self.notifications)
        
        layout.addWidget(sync_group)
        
        # Durum bilgisi
        self.status_label = QLabel("Durum: Ayarlar henüz kaydedilmedi")
        self.status_label.setStyleSheet("color: #666; font-style: italic;")
        layout.addWidget(self.status_label)
        
        layout.addStretch()
        self.tab_widget.addTab(sync_widget, "Senkronizasyon")
        
    def load_settings(self):
        """Kaydedilmiş ayarları yükle"""
        if os.path.exists('.env'):
            load_dotenv()
            
            # GitHub ayarları
            self.github_token.setText(os.getenv('GITHUB_TOKEN', ''))
            self.github_username.setText(os.getenv('GITHUB_USERNAME', ''))
            self.github_repo.setText(os.getenv('GITHUB_REPO', ''))
            
            # LeetCode ayarları
            self.leetcode_session.setText(os.getenv('LEETCODE_SESSION', ''))
            self.csrf_token.setText(os.getenv('CSRF_TOKEN', ''))
            
            # Gemini ayarları
            self.gemini_api_key.setText(os.getenv('GEMINI_API_KEY', ''))
            
            # Senkronizasyon ayarları
            sync_interval = os.getenv('SYNC_INTERVAL', '30 dakika')
            if sync_interval in [self.sync_interval.itemText(i) for i in range(self.sync_interval.count())]:
                self.sync_interval.setCurrentText(sync_interval)
            
            self.auto_start.setChecked(os.getenv('AUTO_START', 'true').lower() == 'true')
            self.notifications.setChecked(os.getenv('NOTIFICATIONS', 'true').lower() == 'true')
            
            self.status_label.setText("Durum: Ayarlar yüklendi")
            
    def save_settings(self):
        """Ayarları .env dosyasına kaydet"""
        try:
            # Boş alanları kontrol et
            if not self.github_token.text().strip():
                QMessageBox.warning(self, "Uyarı", "GitHub Token boş olamaz!")
                return
            if not self.github_username.text().strip():
                QMessageBox.warning(self, "Uyarı", "GitHub kullanıcı adı boş olamaz!")
                return
            if not self.github_repo.text().strip():
                QMessageBox.warning(self, "Uyarı", "GitHub repository adı boş olamaz!")
                return
            if not self.leetcode_session.text().strip():
                QMessageBox.warning(self, "Uyarı", "LeetCode Session boş olamaz!")
                return
            if not self.csrf_token.text().strip():
                QMessageBox.warning(self, "Uyarı", "CSRF Token boş olamaz!")
                return
            if not self.gemini_api_key.text().strip():
                QMessageBox.warning(self, "Uyarı", "Gemini API Key boş olamaz!")
                return
            
            # Şifreleme anahtarı oluştur veya yükle
            key_file = 'encryption.key'
            if os.path.exists(key_file):
                with open(key_file, 'rb') as f:
                    key = f.read()
            else:
                key = Fernet.generate_key()
                with open(key_file, 'wb') as f:
                    f.write(key)
            
            fernet = Fernet(key)
            
            # Şifreleme işlemlerini yap
            encrypted_github_token = fernet.encrypt(self.github_token.text().strip().encode()).decode()
            encrypted_leetcode_session = fernet.encrypt(self.leetcode_session.text().strip().encode()).decode()
            encrypted_csrf_token = fernet.encrypt(self.csrf_token.text().strip().encode()).decode()
            encrypted_gemini_key = fernet.encrypt(self.gemini_api_key.text().strip().encode()).decode()
            
            # .env dosyasına yazılacak içerik
            env_content = f"""# GitHub Ayarları
GITHUB_TOKEN={encrypted_github_token}
GITHUB_USERNAME={self.github_username.text().strip()}
GITHUB_REPO={self.github_repo.text().strip()}

# LeetCode Ayarları
LEETCODE_SESSION={encrypted_leetcode_session}
CSRF_TOKEN={encrypted_csrf_token}

# Gemini API Ayarları
GEMINI_API_KEY={encrypted_gemini_key}

# Senkronizasyon Ayarları
SYNC_INTERVAL={self.sync_interval.currentText()}
AUTO_START={str(self.auto_start.isChecked()).lower()}
NOTIFICATIONS={str(self.notifications.isChecked()).lower()}
"""
            
            with open('.env', 'w', encoding='utf-8') as f:
                f.write(env_content)
            
            self.status_label.setText("Durum: Ayarlar başarıyla kaydedildi")
            QMessageBox.information(self, "Başarılı", "Ayarlar başarıyla kaydedildi!")
            
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Ayarlar kaydedilirken hata oluştu: {str(e)}")
            print(f"Detaylı hata: {e}")  # Debug için
            
    def test_connections(self):
        """Bağlantıları test et"""
        try:
            # Önce .env dosyasından şifrelenmiş verileri oku
            if not os.path.exists('.env'):
                QMessageBox.warning(self, "Uyarı", ".env dosyası bulunamadı!")
                return
            
            # Şifreleme anahtarı yükle
            key_file = 'encryption.key'
            if not os.path.exists(key_file):
                QMessageBox.warning(self, "Uyarı", "Şifreleme anahtarı bulunamadı!")
                return
            
            with open(key_file, 'rb') as f:
                key = f.read()
            
            fernet = Fernet(key)
            
            # .env dosyasından şifrelenmiş verileri oku ve çöz
            from dotenv import load_dotenv
            load_dotenv()
            
            try:
                github_token = fernet.decrypt(os.getenv('GITHUB_TOKEN').encode()).decode()
                github_username = os.getenv('GITHUB_USERNAME')
                github_repo = os.getenv('GITHUB_REPO')
                
                leetcode_session = fernet.decrypt(os.getenv('LEETCODE_SESSION').encode()).decode()
                csrf_token = fernet.decrypt(os.getenv('CSRF_TOKEN').encode()).decode()
                
                gemini_api_key = fernet.decrypt(os.getenv('GEMINI_API_KEY').encode()).decode()
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Şifrelenmiş veriler okunamadı: {str(e)}")
                return
            
            # API istemcilerini oluştur ve test et
            from leetcode_client import LeetCodeClient
            from github_client import GitHubClient
            from gemini_client import GeminiClient
            
            results = []
            
            # GitHub test
            try:
                github_client = GitHubClient(
                    token=github_token,
                    username=github_username,
                    repo=github_repo
                )
                github_ok = github_client.test_connection()
                results.append(f"GitHub: {'✅ Başarılı' if github_ok else '❌ Başarısız'}")
            except Exception as e:
                results.append(f"GitHub: ❌ Başarısız - {str(e)[:50]}...")
            
            # LeetCode test
            try:
                leetcode_client = LeetCodeClient(
                    session=leetcode_session,
                    csrf_token=csrf_token
                )
                leetcode_ok = leetcode_client.test_connection()
                results.append(f"LeetCode: {'✅ Başarılı' if leetcode_ok else '❌ Başarısız'}")
            except Exception as e:
                results.append(f"LeetCode: ❌ Başarısız - {str(e)[:50]}...")
            
            # Gemini test
            try:
                gemini_client = GeminiClient(api_key=gemini_api_key)
                gemini_ok = gemini_client.test_connection()
                results.append(f"Gemini: {'✅ Başarılı' if gemini_ok else '❌ Başarısız'}")
            except Exception as e:
                results.append(f"Gemini: ❌ Başarısız - {str(e)[:50]}...")
            
            # Sonuçları göster
            result_message = "\n".join(results)
            QMessageBox.information(self, "Test Sonuçları", result_message)
            
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Test sırasında hata oluştu: {str(e)}")
        
    def start_sync(self):
        """Senkronizasyonu başlat"""
        try:
            # Ana pencereyi kapat ve senkronizasyonu başlat
            self.close()
            
            # Ana uygulamayı başlat
            from main import MainWindow
            from PyQt5.QtWidgets import QApplication
            import sys
            
            app = QApplication.instance()
            if app is None:
                app = QApplication(sys.argv)
            
            main_window = MainWindow()
            main_window.show()
            
            # Senkronizasyonu başlat
            if main_window.sync_manager:
                main_window.sync_manager.start_sync()
            
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Senkronizasyon başlatılamadı: {str(e)}")

def main():
    app = QApplication(sys.argv)
    window = ConfigWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
