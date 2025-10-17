import requests
import base64
import json
from datetime import datetime
from typing import Dict, Optional

class GitHubClient:
    """GitHub REST API istemcisi"""
    
    def __init__(self, token: str, username: str, repo: str):
        self.token = token
        self.username = username
        self.repo = repo
        self.base_url = "https://api.github.com"
        
        # Headers ayarla
        self.headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'LeetCode-Sync-Tool/1.0'
        }
    
    def _make_request(self, method: str, endpoint: str, data: Dict = None) -> Dict:
        """GitHub API isteği gönder"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=self.headers, timeout=30)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=self.headers, json=data, timeout=30)
            elif method.upper() == 'PUT':
                response = requests.put(url, headers=self.headers, json=data, timeout=30)
            elif method.upper() == 'DELETE':
                response = requests.delete(url, headers=self.headers, timeout=30)
            else:
                raise ValueError(f"Desteklenmeyen HTTP metodu: {method}")
            
            response.raise_for_status()
            return response.json() if response.content else {}
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"GitHub API isteği başarısız: {str(e)}")
    
    def test_connection(self) -> bool:
        """GitHub bağlantısını test et"""
        try:
            # Kullanıcı bilgilerini al
            user_data = self._make_request('GET', '/user')
            if user_data.get('login') == self.username:
                return True
            
            # Repository'nin var olup olmadığını kontrol et
            repo_data = self._make_request('GET', f'/repos/{self.username}/{self.repo}')
            return True
            
        except:
            return False
    
    def get_repo_info(self) -> Dict:
        """Repository bilgilerini al"""
        try:
            return self._make_request('GET', f'/repos/{self.username}/{self.repo}')
        except Exception as e:
            raise Exception(f"Repository bilgileri alınamadı: {str(e)}")
    
    def create_directory(self, path: str) -> bool:
        """Yeni bir dizin oluştur (README.md ile)"""
        try:
            readme_content = f"# {path}\n\nBu dizin LeetCode çözümleri için oluşturulmuştur.\n"
            
            # README.md dosyasını oluştur
            self.create_file(f"{path}/README.md", readme_content, f"Create directory: {path}")
            return True
            
        except Exception as e:
            raise Exception(f"Dizin oluşturulamadı: {str(e)}")
    
    def create_file(self, path: str, content: str, commit_message: str) -> bool:
        """Yeni dosya oluştur"""
        try:
            # Base64 ile içeriği kodla
            encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')
            
            data = {
                'message': commit_message,
                'content': encoded_content,
                'branch': 'main'  # Varsayılan branch
            }
            
            self._make_request('PUT', f'/repos/{self.username}/{self.repo}/contents/{path}', data)
            return True
            
        except Exception as e:
            raise Exception(f"Dosya oluşturulamadı: {str(e)}")
    
    def update_file(self, path: str, content: str, commit_message: str, sha: str) -> bool:
        """Mevcut dosyayı güncelle"""
        try:
            # Base64 ile içeriği kodla
            encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')
            
            data = {
                'message': commit_message,
                'content': encoded_content,
                'sha': sha,
                'branch': 'main'
            }
            
            self._make_request('PUT', f'/repos/{self.username}/{self.repo}/contents/{path}', data)
            return True
            
        except Exception as e:
            raise Exception(f"Dosya güncellenemedi: {str(e)}")
    
    def file_exists(self, path: str) -> Optional[Dict]:
        """Dosyanın var olup olmadığını kontrol et"""
        try:
            return self._make_request('GET', f'/repos/{self.username}/{self.repo}/contents/{path}')
        except:
            return None
    
    def get_file_sha(self, path: str) -> Optional[str]:
        """Dosyanın SHA değerini al"""
        file_info = self.file_exists(path)
        if file_info:
            return file_info.get('sha')
        return None
    
    def commit_solution(self, problem_slug: str, code: str, readme_content: str, language: str) -> bool:
        """LeetCode çözümünü GitHub'a commit et"""
        try:
            # Problem slug'ını temizle (özel karakterleri kaldır)
            clean_slug = self._clean_slug(problem_slug)
            
            # Dosya uzantısını belirle
            file_extension = self._get_file_extension(language)
            solution_filename = f"solution{file_extension}"
            
            # Commit mesajı
            commit_message = f"Add solution for {problem_slug}"
            
            # Dizin oluştur (eğer yoksa)
            dir_path = clean_slug
            readme_path = f"{dir_path}/README.md"
            solution_path = f"{dir_path}/{solution_filename}"
            
            # README.md dosyasını oluştur/güncelle
            readme_sha = self.get_file_sha(readme_path)
            if readme_sha:
                self.update_file(readme_path, readme_content, commit_message, readme_sha)
            else:
                self.create_file(readme_path, readme_content, commit_message)
            
            # Solution dosyasını oluştur/güncelle
            solution_sha = self.get_file_sha(solution_path)
            if solution_sha:
                self.update_file(solution_path, code, commit_message, solution_sha)
            else:
                self.create_file(solution_path, code, commit_message)
            
            return True
            
        except Exception as e:
            raise Exception(f"Çözüm commit edilemedi: {str(e)}")
    
    def _clean_slug(self, slug: str) -> str:
        """Problem slug'ını temizle"""
        # Özel karakterleri kaldır ve küçük harfe çevir
        import re
        clean_slug = re.sub(r'[^a-zA-Z0-9\-_]', '', slug)
        return clean_slug.lower()
    
    def _get_file_extension(self, language: str) -> str:
        """Programlama diline göre dosya uzantısını belirle"""
        extension_map = {
            'python': '.py',
            'python3': '.py',
            'java': '.java',
            'javascript': '.js',
            'typescript': '.ts',
            'cpp': '.cpp',
            'c': '.c',
            'csharp': '.cs',
            'go': '.go',
            'rust': '.rs',
            'php': '.php',
            'ruby': '.rb',
            'swift': '.swift',
            'kotlin': '.kt',
            'scala': '.scala',
            'r': '.r',
            'sql': '.sql',
            'bash': '.sh',
            'shell': '.sh'
        }
        
        return extension_map.get(language.lower(), '.txt')
    
    def get_recent_commits(self, limit: int = 10) -> list:
        """Son commit'leri al"""
        try:
            commits = self._make_request('GET', f'/repos/{self.username}/{self.repo}/commits?per_page={limit}')
            return commits
        except Exception as e:
            raise Exception(f"Commit'ler alınamadı: {str(e)}")
    
    def get_repo_contents(self, path: str = '') -> list:
        """Repository içeriğini al"""
        try:
            contents = self._make_request('GET', f'/repos/{self.username}/{self.repo}/contents/{path}')
            return contents if isinstance(contents, list) else [contents]
        except Exception as e:
            raise Exception(f"Repository içeriği alınamadı: {str(e)}")
    
    def create_branch(self, branch_name: str, from_branch: str = 'main') -> bool:
        """Yeni branch oluştur"""
        try:
            # Ana branch'in SHA'sını al
            main_ref = self._make_request('GET', f'/repos/{self.username}/{self.repo}/git/refs/heads/{from_branch}')
            main_sha = main_ref['object']['sha']
            
            # Yeni branch oluştur
            data = {
                'ref': f'refs/heads/{branch_name}',
                'sha': main_sha
            }
            
            self._make_request('POST', f'/repos/{self.username}/{self.repo}/git/refs', data)
            return True
            
        except Exception as e:
            raise Exception(f"Branch oluşturulamadı: {str(e)}")
    
    def delete_file(self, path: str, commit_message: str) -> bool:
        """Dosyayı sil"""
        try:
            # Dosyanın SHA'sını al
            file_info = self.file_exists(path)
            if not file_info:
                return True  # Dosya zaten yok
            
            sha = file_info['sha']
            
            data = {
                'message': commit_message,
                'sha': sha,
                'branch': 'main'
            }
            
            self._make_request('DELETE', f'/repos/{self.username}/{self.repo}/contents/{path}', data)
            return True
            
        except Exception as e:
            raise Exception(f"Dosya silinemedi: {str(e)}")
    
    def get_user_info(self) -> Dict:
        """Kullanıcı bilgilerini al"""
        try:
            return self._make_request('GET', '/user')
        except Exception as e:
            raise Exception(f"Kullanıcı bilgileri alınamadı: {str(e)}")
    
    def search_repositories(self, query: str, limit: int = 10) -> list:
        """Repository ara"""
        try:
            search_url = f"/search/repositories?q={query}&per_page={limit}"
            result = self._make_request('GET', search_url)
            return result.get('items', [])
        except Exception as e:
            raise Exception(f"Repository arama başarısız: {str(e)}")
