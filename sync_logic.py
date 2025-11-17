import os
import json
import time
from datetime import datetime
from PyQt5.QtCore import QObject, QTimer, pyqtSignal
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from leetcode_client import LeetCodeClient
from github_client import GitHubClient
from gemini_client import GeminiClient

class SyncManager(QObject):
    """Ana senkronizasyon yöneticisi"""
    
    # PyQt5 sinyalleri
    status_changed = pyqtSignal(str)  # Durum değişikliği sinyali
    new_solution_found = pyqtSignal(dict)  # Yeni çözüm bulundu sinyali
    error_occurred = pyqtSignal(str)  # Hata oluştu sinyali
    
    def __init__(self):
        super().__init__()
        
        # Ayarları yükle
        self.load_config()
        
        # API istemcilerini başlat
        self.leetcode_client = None
        self.github_client = None
        self.gemini_client = None
        
        # Senkronizasyon zamanlayıcısı
        self.sync_timer = QTimer()
        self.sync_timer.timeout.connect(self.run_full_sync)
        
        # Son senkronizasyon zamanı
        self.last_sync_time = None
        
        # Yerel veri dosyası
        self.data_file = 'sync_data.json'
        self.load_local_data()
        
    def load_config(self):
        """Ayarları .env dosyasından yükle"""
        if not os.path.exists('.env'):
            raise FileNotFoundError(".env dosyası bulunamadı. Lütfen önce ayarları yapın.")
        
        load_dotenv(override=True)
        
        # Şifreleme anahtarı yükle
        key_file = 'encryption.key'
        if not os.path.exists(key_file):
            raise FileNotFoundError("Şifreleme anahtarı bulunamadı.")
        
        with open(key_file, 'rb') as f:
            key = f.read()
        
        fernet = Fernet(key)
        
        # Şifrelenmiş değerleri çöz
        self.github_token = fernet.decrypt(os.getenv('GITHUB_TOKEN').encode()).decode()
        self.github_username = os.getenv('GITHUB_USERNAME')
        self.github_repo = os.getenv('GITHUB_REPO')
        
        self.leetcode_session = fernet.decrypt(os.getenv('LEETCODE_SESSION').encode()).decode()
        self.csrf_token = fernet.decrypt(os.getenv('CSRF_TOKEN').encode()).decode()
        
        self.gemini_api_key = fernet.decrypt(os.getenv('GEMINI_API_KEY').encode()).decode()
        
        # Senkronizasyon ayarları
        self.sync_interval = os.getenv('SYNC_INTERVAL', '30 dakika')
        self.auto_start = os.getenv('AUTO_START', 'true').lower() == 'true'
        self.notifications = os.getenv('NOTIFICATIONS', 'true').lower() == 'true'
        
    def load_local_data(self):
        """Yerel veri dosyasını yükle"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.local_data = json.load(f)
            except:
                self.local_data = {
                    'last_submission_id': 0,
                    'last_sync_time': None,
                    'processed_submissions': []
                }
        else:
            self.local_data = {
                'last_submission_id': 0,
                'last_sync_time': None,
                'processed_submissions': []
            }
    
    def save_local_data(self):
        """Yerel veri dosyasını kaydet"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.local_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.error_occurred.emit(f"Yerel veri kaydedilemedi: {str(e)}")
    
    def initialize_clients(self):
        """API istemcilerini başlat"""
        try:
            self.status_changed.emit("API istemcileri başlatılıyor...")
            
            # LeetCode istemcisi
            self.leetcode_client = LeetCodeClient(
                session=self.leetcode_session,
                csrf_token=self.csrf_token
            )
            
            # GitHub istemcisi
            self.github_client = GitHubClient(
                token=self.github_token,
                username=self.github_username,
                repo=self.github_repo
            )
            
            # Gemini istemcisi
            self.gemini_client = GeminiClient(api_key=self.gemini_api_key)
            
            self.status_changed.emit("API istemcileri başarıyla başlatıldı")
            return True
            
        except Exception as e:
            self.error_occurred.emit(f"API istemcileri başlatılamadı: {str(e)}")
            return False
    
    def start_sync(self):
        """Senkronizasyonu başlat"""
        if not self.initialize_clients():
            return False
        
        # Senkronizasyon sıklığını dakikaya çevir
        interval_minutes = self.parse_sync_interval()
        interval_ms = interval_minutes * 60 * 1000
        
        # Zamanlayıcıyı başlat
        self.sync_timer.start(interval_ms)
        
        # İlk senkronizasyonu hemen çalıştır
        self.run_full_sync()
        
        self.status_changed.emit(f"Senkronizasyon başlatıldı ({self.sync_interval})")
        return True
    
    def stop_sync(self):
        """Senkronizasyonu durdur"""
        self.sync_timer.stop()
        self.status_changed.emit("Senkronizasyon durduruldu")
    
    def parse_sync_interval(self):
        """Senkronizasyon sıklığını dakikaya çevir"""
        interval_map = {
            "5 dakika": 5,
            "15 dakika": 15,
            "30 dakika": 30,
            "1 saat": 60,
            "2 saat": 120,
            "6 saat": 360,
            "12 saat": 720,
            "24 saat": 1440
        }
        return interval_map.get(self.sync_interval, 30)
    
    def run_full_sync(self):
        """Ana senkronizasyon döngüsü"""
        try:
            self.status_changed.emit("Senkronizasyon başlatılıyor...")
            
            # Yeni gönderimleri kontrol et
            new_submissions = self.check_for_new_submissions()
            
            if new_submissions:
                self.status_changed.emit(f"{len(new_submissions)} yeni çözüm bulundu")
                
                # Her yeni gönderimi işle
                for submission in new_submissions:
                    self.process_new_submission(submission)
            else:
                self.status_changed.emit("Yeni çözüm bulunamadı")
            
            # Son senkronizasyon zamanını güncelle
            self.last_sync_time = datetime.now().isoformat()
            self.local_data['last_sync_time'] = self.last_sync_time
            self.save_local_data()
            
            self.status_changed.emit(f"Senkronizasyon tamamlandı - {datetime.now().strftime('%H:%M:%S')}")
            
        except Exception as e:
            self.error_occurred.emit(f"Senkronizasyon hatası: {str(e)}")
    
    def check_for_new_submissions(self):
        """LeetCode'dan yeni gönderimleri kontrol et"""
        try:
            # LeetCode'dan gönderimleri çek
            submissions = self.leetcode_client.get_recent_submissions()
            
            new_submissions = []
            last_id = self.local_data.get('last_submission_id', 0)
            
            for submission in submissions:
                submission_id = int(submission.get('id', 0))
                
                # Sadece yeni gönderimleri işle
                if submission_id > last_id and submission_id not in self.local_data.get('processed_submissions', []):
                    new_submissions.append(submission)
                    
                    # Son ID'yi güncelle
                    if submission_id > last_id:
                        last_id = submission_id
            
            # Yerel veriyi güncelle
            self.local_data['last_submission_id'] = last_id
            self.save_local_data()
            
            return new_submissions
            
        except Exception as e:
            self.error_occurred.emit(f"Gönderimler kontrol edilemedi: {str(e)}")
            return []
    
    def process_new_submission(self, submission_data):
        """Yeni gönderimi işle"""
        try:
            submission_id = int(submission_data.get('id', 0))
            problem_slug = submission_data.get('titleSlug')
            problem_title = submission_data.get('title')
            language = submission_data.get('lang')
            
            self.status_changed.emit(f"Çözüm işleniyor: {problem_title}")
            
            # Çözüm kodunu çek
            submission_details = self.leetcode_client.get_submission_code(submission_id)
            if not submission_details or not submission_details.get('code'):
                self.error_occurred.emit(f"Çözüm kodu alınamadı: {problem_title}")
                return
            
            solution_code = submission_details.get('code', '')
            language = submission_details.get('language', language)  # Fallback to original lang if needed
            
            # Problem detaylarını çek
            problem_details = self.leetcode_client.get_problem_details(problem_slug)
            
            # Gemini ile README oluştur
            readme_content = self.gemini_client.generate_readme(
                problem_title=problem_title,
                problem_description=problem_details.get('content', ''),
                solution_code=solution_code,
                language=language
            )
            
            # GitHub'a yükle
            success = self.github_client.commit_solution(
                problem_slug=problem_slug,
                code=solution_code,
                readme_content=readme_content,
                language=language
            )
            
            if success:
                # İşlenen gönderimi kaydet
                if 'processed_submissions' not in self.local_data:
                    self.local_data['processed_submissions'] = []
                
                self.local_data['processed_submissions'].append(submission_id)
                self.save_local_data()
                
                # Bildirim gönder
                if self.notifications:
                    self.new_solution_found.emit({
                        'title': problem_title,
                        'slug': problem_slug,
                        'language': language,
                        'timestamp': datetime.now().isoformat()
                    })
                
                self.status_changed.emit(f"Çözüm başarıyla yüklendi: {problem_title}")
            else:
                self.error_occurred.emit(f"Çözüm GitHub'a yüklenemedi: {problem_title}")
                
        except Exception as e:
            self.error_occurred.emit(f"Gönderim işlenemedi: {str(e)}")
    
    def get_status(self):
        """Mevcut durumu döndür"""
        return {
            'is_running': self.sync_timer.isActive(),
            'last_sync': self.last_sync_time,
            'interval': self.sync_interval,
            'processed_count': len(self.local_data.get('processed_submissions', []))
        }
    
    def reset_data(self):
        """Yerel veriyi sıfırla"""
        self.local_data = {
            'last_submission_id': 0,
            'last_sync_time': None,
            'processed_submissions': []
        }
        self.save_local_data()
        self.status_changed.emit("Yerel veri sıfırlandı")
