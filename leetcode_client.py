import requests
import json
import re
from typing import List, Dict, Optional

class LeetCodeClient:
    """LeetCode GraphQL API istemcisi"""
    
    def __init__(self, session: str, csrf_token: str):
        self.session = session
        self.csrf_token = csrf_token
        self.base_url = "https://leetcode.com"
        self.graphql_url = f"{self.base_url}/graphql"
        
        # Session ve headers ayarla
        self.session_cookies = {
            'LEETCODE_SESSION': session,
            'csrftoken': csrf_token
        }
        
        self.headers = {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token,
            'Referer': self.base_url,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def _make_request(self, query: str, variables: Dict = None) -> Dict:
        """GraphQL isteği gönder"""
        payload = {
            'query': query,
            'variables': variables or {}
        }
        
        try:
            response = requests.post(
                self.graphql_url,
                json=payload,
                headers=self.headers,
                cookies=self.session_cookies,
                timeout=30
            )
            
            # Detaylı hata bilgisi
            if response.status_code != 200:
                error_text = response.text
                raise Exception(f"HTTP {response.status_code}: {error_text}")
            
            data = response.json()
            if 'errors' in data:
                raise Exception(f"GraphQL hatası: {data['errors']}")
            
            return data.get('data', {})
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"LeetCode API isteği başarısız: {str(e)}")
    
    def get_recent_submissions(self, limit: int = 20) -> List[Dict]:
        """Son gönderimleri çek"""
        query = """
        query recentAcSubmissions($username: String!, $limit: Int!) {
            recentAcSubmissionList(username: $username, limit: $limit) {
                id
                title
                titleSlug
                timestamp
                statusDisplay
                lang
                runtime
                memory
                url
                isPending
                hasNotes
                notes
                flagType
            }
        }
        """
        
        # Kullanıcı adını al
        username = self.get_username()
        if not username:
            raise Exception("Kullanıcı adı alınamadı")
        
        variables = {
            'username': username,
            'limit': limit
        }
        
        data = self._make_request(query, variables)
        submissions = data.get('recentAcSubmissionList', [])
        
        # Gönderimleri temizle ve formatla
        formatted_submissions = []
        for submission in submissions:
            if submission.get('statusDisplay') == 'Accepted':  # Sadece kabul edilen çözümler
                formatted_submissions.append({
                    'id': submission.get('id'),
                    'title': submission.get('title'),
                    'titleSlug': submission.get('titleSlug'),
                    'timestamp': submission.get('timestamp'),
                    'language': submission.get('lang'),
                    'runtime': submission.get('runtime'),
                    'memory': submission.get('memory'),
                    'url': submission.get('url')
                })
        
        return formatted_submissions
    
    def get_submission_code(self, submission_id: str) -> Optional[str]:
        """Belirli bir gönderimin kodunu çek"""
        query = """
        query submissionDetails($submissionId: Int!) {
            submissionDetails(submissionId: $submissionId) {
                code
                lang
                langName
                runtime
                memory
                statusDisplay
                timestamp
                url
                isPending
                hasNotes
                notes
                flagType
                question {
                    questionId
                    title
                    titleSlug
                    hasFrontendPreview
                    exampleTestcases
                    exampleExpected
                }
            }
        }
        """
        
        variables = {
            'submissionId': int(submission_id)
        }
        
        data = self._make_request(query, variables)
        submission_details = data.get('submissionDetails', {})
        
        if not submission_details:
            return None
        
        return submission_details.get('code', '')
    
    def get_problem_details(self, problem_slug: str) -> Dict:
        """Problem detaylarını çek"""
        query = """
        query questionContent($titleSlug: String!) {
            question(titleSlug: $titleSlug) {
                content
                mysqlSchemas
                dataSchemas
                questionId
                questionFrontendId
                title
                titleSlug
                difficulty
                likes
                dislikes
                isLiked
                similarQuestions
                contributors {
                    username
                    profileUrl
                    avatarUrl
                    __typename
                }
                topicTags {
                    name
                    slug
                    translatedName
                    __typename
                }
                companyTagStats
                codeSnippets {
                    lang
                    langSlug
                    code
                    __typename
                }
                stats
                hints
                solution {
                    id
                    canSeeDetail
                    paidOnly
                    hasVideoSolution
                    paidOnlyVideo
                    __typename
                }
                status
                sampleTestCase
                metaData
                judgerAvailable
                judgeType
                mysqlSchemas
                enableRunCode
                enableTestMode
                enableDebugger
                envInfo
                libraryUrl
                adminUrl
                challengeQuestion {
                    id
                    date
                    incompleteChallengeCount
                    streakCount
                    type
                    __typename
                }
                __typename
            }
        }
        """
        
        variables = {
            'titleSlug': problem_slug
        }
        
        data = self._make_request(query, variables)
        question = data.get('question', {})
        
        if not question:
            return {}
        
        # HTML içeriğini temizle
        content = question.get('content', '')
        if content:
            # HTML etiketlerini kaldır
            content = re.sub(r'<[^>]+>', '', content)
            # Fazla boşlukları temizle
            content = re.sub(r'\s+', ' ', content).strip()
        
        return {
            'questionId': question.get('questionId'),
            'title': question.get('title'),
            'titleSlug': question.get('titleSlug'),
            'difficulty': question.get('difficulty'),
            'content': content,
            'likes': question.get('likes'),
            'dislikes': question.get('dislikes'),
            'topicTags': question.get('topicTags', []),
            'codeSnippets': question.get('codeSnippets', []),
            'stats': question.get('stats'),
            'hints': question.get('hints', [])
        }
    
    def get_username(self) -> Optional[str]:
        """Mevcut kullanıcı adını al"""
        query = """
        query globalData {
            userStatus {
                isSignedIn
                username
            }
        }
        """
        
        try:
            data = self._make_request(query)
            user_status = data.get('userStatus', {})
            
            if user_status.get('isSignedIn'):
                return user_status.get('username')
            else:
                raise Exception("Kullanıcı giriş yapmamış")
                
        except Exception as e:
            raise Exception(f"Kullanıcı adı alınamadı: {str(e)}")
    
    def test_connection(self) -> bool:
        """Bağlantıyı test et"""
        try:
            # Basit bir GraphQL sorgusu ile test et
            query = """
            query globalData {
                userStatus {
                    isSignedIn
                    username
                }
            }
            """
            
            data = self._make_request(query)
            user_status = data.get('userStatus', {})
            
            if user_status.get('isSignedIn'):
                return True
            else:
                print("LeetCode: Kullanıcı giriş yapmamış")
                return False
                
        except Exception as e:
            print(f"LeetCode test hatası: {str(e)}")
            return False
    
    def get_user_stats(self) -> Dict:
        """Kullanıcı istatistiklerini al"""
        query = """
        query userProfileCalendar($username: String!, $year: Int) {
            matchedUser(username: $username) {
                userCalendar(year: $year) {
                    activeYears
                    streak
                    totalActiveDays
                    dccBadges {
                        timestamp
                        badge {
                            name
                            icon
                        }
                    }
                    submissionCalendar
                }
            }
        }
        """
        
        username = self.get_username()
        if not username:
            return {}
        
        variables = {
            'username': username,
            'year': 2024
        }
        
        try:
            data = self._make_request(query, variables)
            matched_user = data.get('matchedUser', {})
            user_calendar = matched_user.get('userCalendar', {})
            
            return {
                'streak': user_calendar.get('streak'),
                'totalActiveDays': user_calendar.get('totalActiveDays'),
                'activeYears': user_calendar.get('activeYears'),
                'submissionCalendar': user_calendar.get('submissionCalendar')
            }
        except:
            return {}
