import google.generativeai as genai
from typing import Dict, Optional
import re

class GeminiClient:
    """Google Gemini API istemcisi"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        genai.configure(api_key=api_key)
        
        # Model ayarları
        self.model = genai.GenerativeModel('gemini-1.5-flash-001')
        
        # Generation config
        self.generation_config = {
            'temperature': 0.7,
            'top_p': 0.8,
            'top_k': 40,
            'max_output_tokens': 2048,
        }
    
    def test_connection(self) -> bool:
        """Gemini API bağlantısını test et"""
        try:
            # Önce mevcut modelleri listele
            models = genai.list_models()
            available_models = [model.name for model in models]
            
            # Uygun bir model bul
            if 'models/gemini-2.5-flash' in available_models:
                model_name = 'gemini-2.5-flash'
            elif 'models/gemini-2.0-flash' in available_models:
                model_name = 'gemini-2.0-flash'
            elif 'models/gemini-1.5-flash' in available_models:
                model_name = 'gemini-1.5-flash'
            elif 'models/gemini-pro' in available_models:
                model_name = 'gemini-pro'
            else:
                print(f"Mevcut modeller: {available_models}")
                return False
            
            # Modeli güncelle
            self.model = genai.GenerativeModel(model_name)
            
            # Basit bir test prompt'u gönder
            test_prompt = "Hello, can you respond with 'Connection successful'?"
            response = self.model.generate_content(test_prompt)
            return "connection successful" in response.text.lower()
        except Exception as e:
            print(f"Gemini API test hatası: {str(e)}")
            return False
    
    def generate_readme(self, problem_title: str, problem_description: str, 
                       solution_code: str, language: str) -> str:
        """LeetCode çözümü için README.md içeriği oluştur"""
        
        try:
            # Prompt template
            prompt = f"""
LeetCode problemi için detaylı bir README.md dosyası oluştur. Aşağıdaki bilgileri kullan:

**Problem Başlığı:** {problem_title}
**Programlama Dili:** {language}
**Problem Açıklaması:** {problem_description[:1000]}...
**Çözüm Kodu:**
```{language}
{solution_code}
```

README.md dosyası şu bölümleri içermeli:

1. **Problem Başlığı** (H1 başlık)
2. **Problem Açıklaması** (Kısa özet)
3. **Çözüm Yaklaşımı** (Algoritma açıklaması)
4. **Karmaşıklık Analizi** (Zaman ve uzay karmaşıklığı)
5. **Kod Açıklaması** (Önemli kısımların açıklaması)
6. **LeetCode Linki** (https://leetcode.com/problems/{problem_title.lower().replace(' ', '-')}/)

README.md formatında, Türkçe olarak ve profesyonel bir şekilde yaz. Markdown formatını kullan.
"""
            
            # Gemini'den yanıt al
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config
            )
            
            # Yanıtı temizle ve formatla
            readme_content = self._format_readme_content(response.text, problem_title, language)
            
            return readme_content
            
        except Exception as e:
            # Hata durumunda basit bir README oluştur
            return self._create_fallback_readme(problem_title, language)
    
    def _format_readme_content(self, content: str, problem_title: str, language: str) -> str:
        """README içeriğini formatla ve temizle"""
        
        # Gereksiz metinleri kaldır
        content = re.sub(r'^.*?```markdown\s*', '', content, flags=re.DOTALL)
        content = re.sub(r'```\s*$', '', content, flags=re.DOTALL)
        
        # Başlık formatını düzelt
        if not content.startswith('#'):
            content = f"# {problem_title}\n\n{content}"
        
        # LeetCode linkini ekle (eğer yoksa)
        if 'leetcode.com' not in content.lower():
            slug = problem_title.lower().replace(' ', '-').replace('(', '').replace(')', '')
            leetcode_link = f"\n\n## LeetCode Linki\n\n[Problem Linki](https://leetcode.com/problems/{slug}/)"
            content += leetcode_link
        
        # Programlama dili bilgisini ekle
        if 'Programlama Dili' not in content:
            language_section = f"\n\n## Programlama Dili\n\n{language}"
            content += language_section
        
        return content.strip()
    
    def _create_fallback_readme(self, problem_title: str, language: str) -> str:
        """API hatası durumunda basit README oluştur"""
        
        slug = problem_title.lower().replace(' ', '-').replace('(', '').replace(')', '')
        
        return f"""# {problem_title}

## Problem Açıklaması

Bu LeetCode problemi için çözüm kodu aşağıda verilmiştir.

## Programlama Dili

{language}

## Çözüm

Çözüm kodu `solution.{self._get_file_extension(language)}` dosyasında bulunmaktadır.

## LeetCode Linki

[Problem Linki](https://leetcode.com/problems/{slug}/)

---

*Bu README dosyası otomatik olarak oluşturulmuştur.*
"""
    
    def _get_file_extension(self, language: str) -> str:
        """Programlama diline göre dosya uzantısını belirle"""
        extension_map = {
            'python': 'py',
            'python3': 'py',
            'java': 'java',
            'javascript': 'js',
            'typescript': 'ts',
            'cpp': 'cpp',
            'c': 'c',
            'csharp': 'cs',
            'go': 'go',
            'rust': 'rs',
            'php': 'php',
            'ruby': 'rb',
            'swift': 'swift',
            'kotlin': 'kt',
            'scala': 'scala',
            'r': 'r',
            'sql': 'sql',
            'bash': 'sh',
            'shell': 'sh'
        }
        
        return extension_map.get(language.lower(), 'txt')
    
    def analyze_code_complexity(self, code: str, language: str) -> Dict[str, str]:
        """Kod karmaşıklığını analiz et"""
        
        try:
            prompt = f"""
Aşağıdaki {language} kodunun zaman ve uzay karmaşıklığını analiz et:

```{language}
{code}
```

Yanıtını şu formatta ver:
- **Zaman Karmaşıklığı:** O(...)
- **Uzay Karmaşıklığı:** O(...)
- **Açıklama:** Kısa açıklama
"""
            
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config
            )
            
            # Yanıttan karmaşıklık bilgilerini çıkar
            complexity_info = self._parse_complexity_response(response.text)
            return complexity_info
            
        except Exception as e:
            return {
                'time_complexity': 'O(n)',
                'space_complexity': 'O(1)',
                'explanation': 'Karmaşıklık analizi yapılamadı.'
            }
    
    def _parse_complexity_response(self, response: str) -> Dict[str, str]:
        """Karmaşıklık yanıtını parse et"""
        
        complexity_info = {
            'time_complexity': 'O(n)',
            'space_complexity': 'O(1)',
            'explanation': 'Analiz yapılamadı.'
        }
        
        # Zaman karmaşıklığını bul
        time_match = re.search(r'zaman karmaşıklığı[:\s]*O\([^)]+\)', response.lower())
        if time_match:
            complexity_info['time_complexity'] = time_match.group(0).split(':')[-1].strip()
        
        # Uzay karmaşıklığını bul
        space_match = re.search(r'uzay karmaşıklığı[:\s]*O\([^)]+\)', response.lower())
        if space_match:
            complexity_info['space_complexity'] = space_match.group(0).split(':')[-1].strip()
        
        # Açıklamayı bul
        explanation_match = re.search(r'açıklama[:\s]*(.+?)(?:\n|$)', response.lower())
        if explanation_match:
            complexity_info['explanation'] = explanation_match.group(1).strip()
        
        return complexity_info
    
    def generate_code_explanation(self, code: str, language: str) -> str:
        """Kod açıklaması oluştur"""
        
        try:
            prompt = f"""
Aşağıdaki {language} kodunu satır satır açıkla:

```{language}
{code}
```

Kodun ne yaptığını, algoritmanın nasıl çalıştığını ve önemli kısımları açıkla.
"""
            
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config
            )
            
            return response.text.strip()
            
        except Exception as e:
            return "Kod açıklaması oluşturulamadı."
    
    def suggest_improvements(self, code: str, language: str) -> str:
        """Kod iyileştirme önerileri"""
        
        try:
            prompt = f"""
Aşağıdaki {language} kodunu incele ve iyileştirme önerileri sun:

```{language}
{code}
```

Performans, okunabilirlik ve best practice'ler açısından öneriler ver.
"""
            
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config
            )
            
            return response.text.strip()
            
        except Exception as e:
            return "İyileştirme önerileri oluşturulamadı."
