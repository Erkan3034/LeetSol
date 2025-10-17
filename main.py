import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QTextEdit, 
                             QGroupBox, QMessageBox, QSystemTrayIcon, QMenu,
                             QStatusBar, QProgressBar)
from PyQt5.QtCore import Qt, QTimer, pyqtSlot
from PyQt5.QtGui import QIcon, QFont
from config_gui import ConfigWindow
from sync_logic import SyncManager

class MainWindow(QMainWindow):
    """Ana uygulama penceresi"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Universal LeetCode GitHub Sync Tool")
        self.setGeometry(200, 200, 900, 700)
        
        # Sync manager'ı başlat (hata durumunda None olacak)
        self.sync_manager = None
        try:
            self.sync_manager = SyncManager()
            self.sync_manager.status_changed.connect(self.update_status)
            self.sync_manager.new_solution_found.connect(self.show_new_solution_notification)
            self.sync_manager.error_occurred.connect(self.show_error)
        except FileNotFoundError:
            # Ayarlar henüz yapılmamış, ayarlar penceresini aç
            self.log_message("Ayarlar henüz yapılmamış. Lütfen önce ayarları yapılandırın.")
            self.open_settings()
        
        # Ana widget ve layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Başlık
        title_label = QLabel("Universal LeetCode GitHub Sync Tool")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #2E7D32; margin: 10px;")
        main_layout.addWidget(title_label)
        
        # Durum bilgisi grubu
        self.create_status_group(main_layout)
        
        # Kontrol butonları grubu
        self.create_control_group(main_layout)
        
        # Log alanı
        self.create_log_group(main_layout)
        
        # Status bar
        self.create_status_bar()
        
        # System tray icon
        self.create_system_tray()
        
        # Otomatik başlatma kontrolü
        self.check_auto_start()
        
    def create_status_group(self, layout):
        """Durum bilgisi grubu oluştur"""
        status_group = QGroupBox("Senkronizasyon Durumu")
        status_layout = QVBoxLayout(status_group)
        
        # Durum etiketi
        self.status_label = QLabel("Durum: Başlatılmadı")
        self.status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #666;")
        status_layout.addWidget(self.status_label)
        
        # Son senkronizasyon zamanı
        self.last_sync_label = QLabel("Son Senkronizasyon: Hiç")
        self.last_sync_label.setStyleSheet("color: #666;")
        status_layout.addWidget(self.last_sync_label)
        
        # İşlenen çözüm sayısı
        self.processed_count_label = QLabel("İşlenen Çözüm: 0")
        self.processed_count_label.setStyleSheet("color: #666;")
        status_layout.addWidget(self.processed_count_label)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        status_layout.addWidget(self.progress_bar)
        
        layout.addWidget(status_group)
    
    def create_control_group(self, layout):
        """Kontrol butonları grubu oluştur"""
        control_group = QGroupBox("Kontrol")
        control_layout = QHBoxLayout(control_group)
        
        # Ayarlar butonu
        self.settings_button = QPushButton("Ayarları Aç")
        self.settings_button.clicked.connect(self.open_settings)
        self.settings_button.setStyleSheet("""
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
        
        # Başlat/Durdur butonu
        self.start_stop_button = QPushButton("Senkronizasyonu Başlat")
        self.start_stop_button.clicked.connect(self.toggle_sync)
        self.start_stop_button.setStyleSheet("""
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
        
        # Manuel senkronizasyon butonu
        self.manual_sync_button = QPushButton("Manuel Senkronizasyon")
        self.manual_sync_button.clicked.connect(self.manual_sync)
        self.manual_sync_button.setStyleSheet("""
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
        
        # Test butonu
        self.test_button = QPushButton("Bağlantıları Test Et")
        self.test_button.clicked.connect(self.test_connections)
        self.test_button.setStyleSheet("""
            QPushButton {
                background-color: #9C27B0;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #7B1FA2;
            }
        """)
        
        control_layout.addWidget(self.settings_button)
        control_layout.addWidget(self.start_stop_button)
        control_layout.addWidget(self.manual_sync_button)
        control_layout.addWidget(self.test_button)
        
        layout.addWidget(control_group)
    
    def create_log_group(self, layout):
        """Log alanı oluştur"""
        log_group = QGroupBox("Log Kayıtları")
        log_layout = QVBoxLayout(log_group)
        
        # Log text area
        self.log_text = QTextEdit()
        self.log_text.setMaximumHeight(200)
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 5px;
                font-family: 'Courier New', monospace;
                font-size: 12px;
            }
        """)
        
        # Log temizleme butonu
        clear_log_button = QPushButton("Log'u Temizle")
        clear_log_button.clicked.connect(self.clear_log)
        clear_log_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 5px 15px;
                font-size: 12px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        
        log_layout.addWidget(self.log_text)
        log_layout.addWidget(clear_log_button)
        
        layout.addWidget(log_group)
    
    def create_status_bar(self):
        """Status bar oluştur"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Durum mesajı
        self.status_bar.showMessage("Hazır")
        
        # Saat
        self.time_label = QLabel()
        self.status_bar.addPermanentWidget(self.time_label)
        
        # Saat güncelleme zamanlayıcısı
        self.time_timer = QTimer()
        self.time_timer.timeout.connect(self.update_time)
        self.time_timer.start(1000)  # Her saniye güncelle
        self.update_time()
    
    def create_system_tray(self):
        """System tray icon oluştur"""
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.tray_icon = QSystemTrayIcon(self)
            self.tray_icon.setIcon(self.style().standardIcon(self.style().SP_ComputerIcon))
            
            # Tray menu
            tray_menu = QMenu()
            
            show_action = tray_menu.addAction("Göster")
            show_action.triggered.connect(self.show)
            
            tray_menu.addSeparator()
            
            quit_action = tray_menu.addAction("Çıkış")
            quit_action.triggered.connect(self.close)
            
            self.tray_icon.setContextMenu(tray_menu)
            self.tray_icon.activated.connect(self.tray_icon_activated)
            self.tray_icon.show()
    
    def check_auto_start(self):
        """Otomatik başlatma kontrolü"""
        try:
            if self.sync_manager and self.sync_manager.auto_start:
                self.log_message("Otomatik senkronizasyon başlatılıyor...")
                self.start_sync()
        except Exception as e:
            self.log_message(f"Otomatik başlatma hatası: {str(e)}")
    
    @pyqtSlot(str)
    def update_status(self, message):
        """Durum mesajını güncelle"""
        self.status_label.setText(f"Durum: {message}")
        self.status_bar.showMessage(message)
        self.log_message(message)
    
    @pyqtSlot(dict)
    def show_new_solution_notification(self, solution_data):
        """Yeni çözüm bildirimi göster"""
        title = solution_data.get('title', 'Yeni Çözüm')
        language = solution_data.get('language', '')
        
        message = f"Yeni çözüm bulundu: {title} ({language})"
        
        # System tray bildirimi
        if hasattr(self, 'tray_icon'):
            self.tray_icon.showMessage(
                "LeetCode Sync Tool",
                message,
                QSystemTrayIcon.Information,
                5000
            )
        
        # Log'a ekle
        self.log_message(f"✅ {message}")
        
        # Status güncelle
        status = self.sync_manager.get_status()
        self.processed_count_label.setText(f"İşlenen Çözüm: {status['processed_count']}")
    
    @pyqtSlot(str)
    def show_error(self, error_message):
        """Hata mesajını göster"""
        self.log_message(f"❌ HATA: {error_message}")
        
        # System tray bildirimi
        if hasattr(self, 'tray_icon'):
            self.tray_icon.showMessage(
                "LeetCode Sync Tool - Hata",
                error_message,
                QSystemTrayIcon.Critical,
                5000
            )
    
    def open_settings(self):
        """Ayarlar penceresini aç"""
        self.settings_window = ConfigWindow()
        self.settings_window.show()
    
    def toggle_sync(self):
        """Senkronizasyonu başlat/durdur"""
        if not self.sync_manager:
            self.log_message("Önce ayarları yapılandırın!")
            self.open_settings()
            return
            
        status = self.sync_manager.get_status()
        
        if status['is_running']:
            self.sync_manager.stop_sync()
            self.start_stop_button.setText("Senkronizasyonu Başlat")
            self.start_stop_button.setStyleSheet("""
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
        else:
            self.start_sync()
    
    def start_sync(self):
        """Senkronizasyonu başlat"""
        if not self.sync_manager:
            self.log_message("Önce ayarları yapılandırın!")
            self.open_settings()
            return
            
        try:
            success = self.sync_manager.start_sync()
            if success:
                self.start_stop_button.setText("Senkronizasyonu Durdur")
                self.start_stop_button.setStyleSheet("""
                    QPushButton {
                        background-color: #f44336;
                        color: white;
                        border: none;
                        padding: 10px 20px;
                        font-size: 14px;
                        border-radius: 5px;
                    }
                    QPushButton:hover {
                        background-color: #d32f2f;
                    }
                """)
                self.log_message("Senkronizasyon başlatıldı")
            else:
                self.log_message("Senkronizasyon başlatılamadı")
        except Exception as e:
            self.show_error(f"Senkronizasyon başlatma hatası: {str(e)}")
    
    def manual_sync(self):
        """Manuel senkronizasyon çalıştır"""
        if not self.sync_manager:
            self.log_message("Önce ayarları yapılandırın!")
            self.open_settings()
            return
            
        try:
            self.log_message("Manuel senkronizasyon başlatılıyor...")
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 0)  # Indeterminate progress
            
            # Senkronizasyonu çalıştır
            self.sync_manager.run_full_sync()
            
            self.progress_bar.setVisible(False)
            self.log_message("Manuel senkronizasyon tamamlandı")
            
        except Exception as e:
            self.progress_bar.setVisible(False)
            self.show_error(f"Manuel senkronizasyon hatası: {str(e)}")
    
    def test_connections(self):
        """Bağlantıları test et"""
        if not self.sync_manager:
            self.log_message("Önce ayarları yapılandırın!")
            self.open_settings()
            return
            
        try:
            self.log_message("Bağlantılar test ediliyor...")
            
            # Test sonuçları
            results = []
            
            # LeetCode test
            try:
                leetcode_ok = self.sync_manager.leetcode_client.test_connection()
                results.append(f"LeetCode: {'✅ Başarılı' if leetcode_ok else '❌ Başarısız'}")
            except:
                results.append("LeetCode: ❌ Başarısız")
            
            # GitHub test
            try:
                github_ok = self.sync_manager.github_client.test_connection()
                results.append(f"GitHub: {'✅ Başarılı' if github_ok else '❌ Başarısız'}")
            except:
                results.append("GitHub: ❌ Başarısız")
            
            # Gemini test
            try:
                gemini_ok = self.sync_manager.gemini_client.test_connection()
                results.append(f"Gemini: {'✅ Başarılı' if gemini_ok else '❌ Başarısız'}")
            except:
                results.append("Gemini: ❌ Başarısız")
            
            # Sonuçları göster
            result_message = "\n".join(results)
            self.log_message(f"Test Sonuçları:\n{result_message}")
            
            QMessageBox.information(self, "Test Sonuçları", result_message)
            
        except Exception as e:
            self.show_error(f"Bağlantı testi hatası: {str(e)}")
    
    def clear_log(self):
        """Log'u temizle"""
        self.log_text.clear()
        self.log_message("Log temizlendi")
    
    def log_message(self, message):
        """Log mesajı ekle"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"
        
        # log_text henüz oluşturulmamışsa sadece print et
        if hasattr(self, 'log_text'):
            self.log_text.append(formatted_message)
            # Scroll to bottom
            scrollbar = self.log_text.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())
        else:
            print(formatted_message)
    
    def update_time(self):
        """Saati güncelle"""
        from datetime import datetime
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.setText(current_time)
    
    def tray_icon_activated(self, reason):
        """Tray icon'a tıklandığında"""
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()
            self.raise_()
            self.activateWindow()
    
    def closeEvent(self, event):
        """Uygulama kapatılırken"""
        if hasattr(self, 'tray_icon') and self.tray_icon.isVisible():
            QMessageBox.information(
                self,
                "Sistem Tepsisi",
                "Uygulama sistem tepsisinde çalışmaya devam edecek. "
                "Tamamen kapatmak için sistem tepsisindeki ikona sağ tıklayın."
            )
            self.hide()
            event.ignore()
        else:
            # Senkronizasyonu durdur
            if hasattr(self, 'sync_manager') and self.sync_manager:
                self.sync_manager.stop_sync()
            event.accept()

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("LeetCode Sync Tool")
    app.setApplicationVersion("1.0")
    
    # Ana pencereyi oluştur
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
